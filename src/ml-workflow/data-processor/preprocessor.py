import pandas as pd
import os
import glob
import json
import gcsfs

from helper import get_ingr_freq_dict, generate_answer_question_pairs

from sklearn.model_selection import train_test_split
from google.cloud import storage

GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
PROJECT_NAME = os.environ["GCP_PROJECT"]

RAW_URI = "ml-workflow/raw/"
CLEAN_URI = "ml-workflow/clean/"
READY_URI = "ml-workflow/ready_for_training/"
RAW_DATASET_PATH = f"{GCS_BUCKET_NAME}/{RAW_URI}"
CLEAN_DATASET_PATH = f"{GCS_BUCKET_NAME}/{CLEAN_URI}"
CLEAN_DATASET = "instruct-dataset.csv"


def generate(raw_dataset_folder):
    """
    Generates a question-answer dataset for LLM training from a .csv file.
    This is only necessary if this is the first run or if new data has been added (i.e. new question-answer
    training and test data needs to be created).
    """

    # These .csv's files only contain recipes with ingredients that occur at least 500 times
    # Gets .csv's from GCS Bucket
    fs = gcsfs.GCSFileSystem(project=PROJECT_NAME)

    print("Downloading from GCP...")
    all_files_in_raw = fs.ls(RAW_DATASET_PATH)
    csv_files = [file for file in all_files_in_raw if file.endswith(".csv")]

    print("Generating Dataframes...")
    # Read and combine all CSV files into one DataFrame
    dataframes = []
    for file in csv_files:
        with fs.open(file) as f:
            df = pd.read_csv(f)
            dataframes.append(df)

    # Combine all dataframes into a single clean one (remove duplicates and NAs)
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df.drop_duplicates().dropna()

    # Get ingredient frequencties
    print("Perform preliminary data analysis for effect QA data generation...")
    ingr_freq_dict = get_ingr_freq_dict(df)

    NUM_ITERATIONS = 3  # INCREASE TO CREATE A LARGE DATASET (1 iteration is 1214 tokens; trained for 3 epochs that's about 3 cents; 34 iterations is $1)

    print("Generating QA.txt files...")
    # Loop to generate and save the content to .txt files in OUTPUT_FOLDER
    for i in range(0, NUM_ITERATIONS):
        if i % 2 == 0:
            print(f"Generating batch: {i}")

        question, answer = generate_answer_question_pairs(df, ingr_freq_dict)
        json_format = f"""[{{"question": "{question}", "answer": "{answer}"}}]"""

        # Create a unique filename for each iteration
        file_name = f"{raw_dataset_folder}/recipe_qa_{i}.txt"
        # Save
        with open(file_name, "w") as file:
            file.write(json_format)


def prepare_and_upload(raw_dataset_folder, clean_dataset_folder):
    """
    Converts the generated .txt files into a .csv file ready for training and uploads to GCS Bucket
    """

    # Get the generated files
    output_files = glob.glob(os.path.join(raw_dataset_folder, "recipe_qa_*.txt"))
    output_files.sort()

    # Quality-check the data
    output_pairs = []
    errors = []
    for i, output_file in enumerate(output_files):
        if i % 5 == 0:
            print("Processing file:", output_file)

        with open(output_file, "r") as read_file:
            text_response = read_file.read()

        try:
            json_responses = json.loads(text_response)
            output_pairs.extend(json_responses)
        except Exception as e:
            errors.append({"file": output_file, "error": str(e)})

    print("Number of errors:", len(errors))
    print(errors[:5])

    # Save the dataset
    output_pairs_df = pd.DataFrame(output_pairs)
    output_pairs_df.drop_duplicates(subset=["question"], inplace=True)
    output_pairs_df = output_pairs_df.dropna()

    # Instruct-Dataset.csv is the clean dataset
    path_to_file = os.path.join(clean_dataset_folder, CLEAN_DATASET)
    output_pairs_df.to_csv(path_to_file, index=False)

    # Get ready to upload instruct-dataset.csv to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    timeout = 300

    # Upload instruct-dataset.csv to GCS bucket (/clean)
    destination_blob_name = os.path.join(CLEAN_URI, CLEAN_DATASET)
    blob = bucket.blob(destination_blob_name)
    print("Uploading file:", path_to_file, destination_blob_name)
    blob.upload_from_filename(path_to_file, timeout=timeout)


def train_test_split_from_clean_data(ready_dataset_folder):
    """
    gets instruct-dataset.csv from GCS Bucket and makes training data from it
    """

    fs = gcsfs.GCSFileSystem(project=PROJECT_NAME)
    with fs.open(CLEAN_DATASET_PATH + CLEAN_DATASET) as f:
        instruct_df = pd.read_csv(f)

    # Build training formats
    instruct_df["text"] = "human: " + instruct_df["question"] + "\n" + "bot: " + instruct_df["answer"]

    # Gemini Data prep: https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-supervised-tuning-prepare
    # {"contents":[{"role":"user","parts":[{"text":"..."}]},{"role":"model","parts":[{"text":"..."}]}]}
    instruct_df["contents"] = instruct_df.apply(
        lambda row: [
            {"role": "user", "parts": [{"text": row["question"]}]},
            {"role": "model", "parts": [{"text": row["answer"]}]},
        ],
        axis=1,
    )

    # Test train split
    df_train, df_test = train_test_split(instruct_df, test_size=0.15, random_state=42)
    df_train[["text"]].to_csv(os.path.join(ready_dataset_folder, "train.csv"), index=False)
    df_test[["text"]].to_csv(os.path.join(ready_dataset_folder, "test.csv"), index=False)

    # Gemini : Max numbers of examples in validation dataset: 256
    df_test = df_test[:256]

    # JSONL
    with open(os.path.join(ready_dataset_folder, "train.jsonl"), "w") as json_file:
        json_file.write(df_train[["contents"]].to_json(orient="records", lines=True))
    with open(os.path.join(ready_dataset_folder, "test.jsonl"), "w") as json_file:
        json_file.write(df_test[["contents"]].to_json(orient="records", lines=True))


def upload_train_test_data(ready_dataset_folder):
    """
    Uploads train,test data to GCS Bucket
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    timeout = 300

    data_files = glob.glob(os.path.join(ready_dataset_folder, "*.jsonl")) + glob.glob(os.path.join(ready_dataset_folder, "*.csv"))
    data_files.sort()

    # Upload
    for data_file in data_files:
        filename = os.path.basename(data_file)
        destination_blob_name = os.path.join(READY_URI, filename)
        blob = bucket.blob(destination_blob_name)
        print("Uploading file:", data_file, destination_blob_name)
        blob.upload_from_filename(data_file, timeout=timeout)
