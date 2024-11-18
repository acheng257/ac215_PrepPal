import glob
import hashlib
import os
import shutil
from google.cloud import storage
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter
from preprocess_recipes import data_cleaning

CHROMADB_HOST = "llm-rag-chromadb"
CHROMADB_PORT = 8000

# Load the SentenceTransformers model
model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
tokenizer = model.tokenizer


gcp_project = "preppal-438123"
bucket_name = "preppal-data"
parent_folder = "rag_data"

child_folder_1 = "knowledge_base"
child_folder_2 = "users"

unprocessed_recipes = "unprocessed_recipes_data"
processed_recipes = "processed_recipes_data"
chunked_recipes = "chunked_recipes"
embedded_recipes = "embedded_recipes"

user_recipe_text = "recipe_text"
user_recipe_chunk = "recipe_chunk"
user_recipe_embed = "recipe_embed"


"""
    HELPER FUNCTIONS
"""


def makedir(file_path):
    os.makedirs(file_path, exist_ok=True)


def clear_env():
    shutil.rmtree(parent_folder, ignore_errors=True, onerror=None)


def download_to_disk(file_path, file):
    makedir(file_path)

    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(f"{file_path}/{file}")
    blob.download_to_filename(blob.name)


def upload_to_gcs(file_path, file):
    makedir(file_path)
    local_file_path = os.path.join(file_path, file)

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    destination_blob_name = os.path.join(file_path, file)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path, timeout=3600)


def download_all_files_in_folder_to_disk(files_path):
    makedir(files_path)
    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(match_glob=f"{files_path}/embedding_*.jsonl")
    for blob in blobs:
        blob.download_to_filename(blob.name)


def upload_all_files_in_folder_to_gcs(folder):
    # List all files in the folder
    files = os.listdir(folder)

    # Upload each file in the folder to GCS
    for file_name in files:
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            upload_to_gcs(folder, file_name)
            print(f"Uploaded {file_name} to GCS.")


"""
    PREPARE DATA FOR RAG
"""


def clean_dataset(download=True, upload=True):
    print("Prepare dataset for RAG")
    folder = os.path.join(parent_folder, child_folder_1)

    # Download
    if download:
        print("download")
        download_to_disk(folder, f"{unprocessed_recipes}.csv")

    # Clean dataset
    local_file_path = os.path.join(folder, f"{unprocessed_recipes}.csv")
    df = pd.read_csv(local_file_path)
    df = data_cleaning(df)

    print(df.head())

    # Save clean DataFrame to a CSV file
    clean_file_path = os.path.join(folder, f"{processed_recipes}.csv")
    df.to_csv(clean_file_path, index=False)

    # Upload
    if upload:
        print("upload")
        upload_to_gcs(folder, f"{processed_recipes}.csv")


"""
    CHUNK DATA
"""


def chunk_user(text, method="entire_recipe"):
    new_df = pd.DataFrame()

    text_chunk = []
    text_document = []

    if method == "entire_recipe":
        text_chunk.append(text)
        text_document.append(text)

    elif method == "sliding_window":
        # Use LangChain's CharacterTextSplitter for sliding window chunking
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100, separator="", strip_whitespace=False)

        # Perform the splitting
        chunked_texts = text_splitter.create_documents([text])

        # Convert the chunked texts into the DataFrame
        for doc in chunked_texts:
            text_chunk.append(doc.page_content)
            text_document.append(text)

    new_df["chunk"] = text_chunk
    new_df["document"] = text_document

    return new_df


def chunk_knowledge_base(df, method="entire_recipe"):
    new_df = pd.DataFrame()
    print("Method:", method)

    text_chunk = []
    text_document = []

    for index, row in df.iterrows():
        # Ensure all fields are converted to strings and handle missing values
        name = str(row["Name"])
        servings = str(row["RecipeServings"])
        total_time = str(row["TotalTime"])
        ingredients = str(row["Ingredients"])
        calories = str(row["Calories"])
        sugar_content = str(row["SugarContent"])
        protein_content = str(row["ProteinContent"])
        instructions = str(row["FormattedRecipeInstructions"])

        # Combine the recipe data into a single text string
        text = (
            f"Recipe: {name}\n"
            f"Recipe Servings: {servings}\n"
            f"Total Time: {total_time}\n"
            f"Ingredients: {ingredients}\n"
            f"Calories: {calories}\n"
            f"Sugar Content: {sugar_content}\n"
            f"Protein Content: {protein_content}\n"
            f"Instructions: {instructions}"
        )

        if index % 10000 == 0:
            print("Reached index", index)

        if method == "entire_recipe":
            # Tokenize the text and count the number of tokens
            tokenized = tokenizer([text], return_tensors="pt")
            num_tokens = len(tokenized["input_ids"][0])

            if num_tokens <= 512:
                text_chunk.append(text)
                text_document.append(text)

        elif method == "sliding_window":
            # Use LangChain's CharacterTextSplitter for sliding window chunking
            text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100, separator="", strip_whitespace=False)

            # Perform the splitting
            chunked_texts = text_splitter.create_documents([text])

            # Convert the chunked texts into the DataFrame
            for doc in chunked_texts:
                text_chunk.append(doc.page_content)
                text_document.append(text)

    new_df["chunk"] = text_chunk
    new_df["document"] = text_document

    return new_df


# For knowledge base: parent_folder = "rag_data"; child_folder = "knowledge_base"; user_id=None; recipe_id=None; user_saved=False
# For users: parent_folder = "rag_data"; child_folder = "users"; user_id=# (string); recipe_id=# (string); user_saved=True
def chunk(
    method="entire_recipe",
    user_id=None,
    recipe_id=None,
    user_saved=False,
    download=True,
    upload=True,
):
    print("Chunk recipes")

    # Knowledge base data
    if user_id is None:
        folder = os.path.join(parent_folder, child_folder_1)

        # Downlaod
        if download:
            print("download")
            download_to_disk(folder, f"{processed_recipes}.csv")
        local_file_path = os.path.join(folder, f"{processed_recipes}.csv")

        # Chunk
        df = pd.read_csv(local_file_path)
        df = chunk_knowledge_base(df, method)
        df["user_id"] = user_id
        df["user_saved"] = user_saved
        print(df.head())

        chunked_file_path = os.path.join(folder, f"{chunked_recipes}_{method}.jsonl")

        with open(chunked_file_path, "w") as json_file:
            for _, row in df.iterrows():
                json_file.write(row.to_json() + "\n")

        # Upload
        if upload:
            print("upload")
            upload_to_gcs(folder, f"{chunked_recipes}_{method}.jsonl")

    # User data
    else:
        folder = os.path.join(parent_folder, child_folder_2, user_id, user_recipe_text)
        file_path = os.path.join(folder, f"{recipe_id}.txt")

        # Download
        if download:
            print("download")
            download_to_disk(folder, f"{recipe_id}.txt")

        with open(file_path, "r") as file:
            file_contents = file.read()

        # Chunk
        df = chunk_user(file_contents, method)
        df["user_id"] = user_id
        df["user_saved"] = user_saved

        folder = os.path.join(parent_folder, child_folder_2, user_id, user_recipe_chunk, method)
        os.makedirs(folder, exist_ok=True)
        chunked_file_path = os.path.join(folder, f"{recipe_id}.jsonl")

        with open(chunked_file_path, "w") as json_file:
            json_file.write(df.to_json(orient="records", lines=True))

        if upload:
            print("upload")
            upload_to_gcs(folder, f"{recipe_id}.jsonl")


"""
    EMBED DATA
"""


def generate_query_embedding(query):
    query_embedding = model.encode(query)
    return query_embedding


def embed(
    method="entire_recipe",
    user_id=None,
    recipe_id=None,
    batch_size=100,
    download=True,
    upload=True,
):
    print("Embed recipes")
    if user_id is None:
        folder = os.path.join(parent_folder, child_folder_1)

        if download:
            print("download")
            download_to_disk(folder, f"{chunked_recipes}_{method}.jsonl")
        local_file_path = os.path.join(folder, f"{chunked_recipes}_{method}.jsonl")

        df = pd.read_json(local_file_path, lines=True)

        # Split the chunks into batches
        chunks = df["chunk"].values

        embeddings = model.encode(chunks, batch_size=batch_size)
        embeddings_list = embeddings.tolist()

        embedded_file_path = os.path.join(folder, f"{embedded_recipes}_{method}.jsonl")
        # Folder to save embeddings
        output_folder = os.path.join(parent_folder, child_folder_1, f"{embedded_recipes}_{method}")
        os.makedirs(output_folder, exist_ok=True)

        num_recipes = 30000
        for batch_num, i in enumerate(range(0, len(chunks), num_recipes)):
            # Get the range of indices for the current file
            start_idx = i
            end_idx = min(i + num_recipes, len(chunks))
            df_chunk = df.iloc[start_idx:end_idx]

            embeddings_chunk = embeddings_list[start_idx:end_idx]
            df_chunk = df_chunk.assign(embedding=embeddings_chunk)

            # Save each chunk as a separate file
            embedded_file_path = os.path.join(output_folder, f"embedding_{batch_num}.jsonl")
            with open(embedded_file_path, "w") as json_file:
                json_file.write(df_chunk.to_json(orient="records", lines=True))

        # Upload to GCS
        if upload:
            print("upload")
            upload_all_files_in_folder_to_gcs(output_folder)

    else:
        folder = os.path.join(parent_folder, child_folder_2, user_id, user_recipe_chunk, method)

        if download:
            print("download")
            download_to_disk(folder, f"{recipe_id}.jsonl")

        local_file_path = os.path.join(folder, f"{recipe_id}.jsonl")
        df = pd.read_json(local_file_path, lines=True)

        chunks = df["chunk"].values

        embeddings = model.encode(chunks, batch_size=batch_size)
        embeddings_list = embeddings.tolist()
        df["embedding"] = embeddings_list

        # Upload or save the updated DataFrame if needed
        output_folder = os.path.join(parent_folder, child_folder_2, user_id, user_recipe_embed, method)
        os.makedirs(output_folder, exist_ok=True)
        embedded_file_path = os.path.join(output_folder, f"{recipe_id}.jsonl")

        with open(embedded_file_path, "w") as json_file:
            json_file.write(df.to_json(orient="records", lines=True))

        if upload:
            print("upload")
            upload_to_gcs(folder, f"{recipe_id}.jsonl")


"""
    LOAD DATA IN DATABASE
"""


def generate_unique_id(row, source_type, index):
    """
    Generate a unique ID for each entry based on the source type, user_id, and recipe_id or hash of the document.
    """
    if source_type == "user":
        # Use user_id and recipe_id to generate unique IDs for user data
        hash_val = hashlib.sha256(row["chunk"].encode()).hexdigest()[:16]
        unique_id = f"user-{row['user_id']}-{index}-{hash_val}"
    else:
        # For knowledge base, use a consistent hash from the document text
        hash_val = hashlib.sha256(row["chunk"].encode()).hexdigest()[:16]
        unique_id = f"kb-{index}-{hash_val}"
    return unique_id


def load_text_embeddings(df, collection, source_type, batch_size=500, index=None):
    # Generate consistent unique IDs
    df["id"] = df.apply(generate_unique_id, source_type=source_type, index=index, axis=1)

    # Metadata is already in the dataframe
    total_inserted = 0
    error_counter = 0

    # Process data in batches
    for i in range(0, df.shape[0], batch_size):
        try:
            batch = df.iloc[i : i + batch_size].copy().reset_index(drop=True)

            # Extract IDs, documents, embeddings, and metadata
            ids = batch["id"].tolist()
            documents = batch["document"].tolist()
            embeddings = batch["embedding"].tolist()
            metadatas = batch[["user_id", "user_saved"]].to_dict(orient="records")

            # Insert into the collection
            collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

            total_inserted += len(batch)
            print(f"Inserted {total_inserted} items...")
        except Exception as e:
            print("Error:", e)
            error_counter += 1

    print(f"Finished inserting {total_inserted} items into collection '{collection.name}'")
    print(f"There have been {error_counter} errors.")


def load(method="entire_recipe", user_id=None, recipe_id=None, download=True):
    print("Load recipes in database")
    # Connect to chroma DB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

    # Get a collection object from an existing collection, by name. If it doesn't exist, create it.
    collection_name = f"{method}_collection"
    print("Acessing collection:", collection_name)

    if user_id is None:
        folder = os.path.join(parent_folder, child_folder_1, f"{embedded_recipes}_{method}")
        # Download
        if download:
            print("download")
            download_all_files_in_folder_to_disk(folder)

        # If collection doesn't exist, create it.
        try:
            # Clear out any existing items in the collection
            client.delete_collection(name=collection_name)
            print(f"Deleted existing collection '{collection_name}'")
        except Exception:
            print(f"Collection '{collection_name}' did not exist. Creating new.")

        collection = client.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
        print(f"Created new empty collection '{collection_name}'")
        print("Collection:", collection)

        # Get the list of embedding files
        jsonl_files = glob.glob(os.path.join(folder, "embedding_*.jsonl"))
        print("Number of files to process:", len(jsonl_files))

        # Process
        # UPDATE HERE
        for index, jsonl_file in enumerate(jsonl_files[1:3]):
            print("Processing file:", jsonl_file)

            data_df = pd.read_json(jsonl_file, lines=True)
            print("Shape:", data_df.shape)
            print(data_df.head())

            # Load data
            load_text_embeddings(data_df, collection, source_type="knowledge_base", index=index)

    else:
        # If user_id is provided, process single user-specific file
        folder = os.path.join(parent_folder, child_folder_2, user_id, user_recipe_embed, method)

        if download:
            print("download")
            download_to_disk(folder, f"{recipe_id}.jsonl")

        collection = client.get_collection(name=collection_name)

        local_file_path = os.path.join(folder, f"{recipe_id}.jsonl")
        print(f"Processing user-specific file: {local_file_path}")

        # Load user data
        data_df = pd.read_json(local_file_path, lines=True)
        print(data_df.head())
        load_text_embeddings(data_df, collection, source_type="user", index=recipe_id)
