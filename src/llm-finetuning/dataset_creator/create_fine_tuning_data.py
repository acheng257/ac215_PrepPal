import pandas as pd
import random
import argparse
import re
import os
import glob
import json

from sklearn.model_selection import train_test_split
from google.cloud import storage


OUTPUT_FOLDER = "fine_tuning_data_small"
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]


# --------------- Helper Functions --------------------
def get_cleaned_ingredient(ingredient):
    bad_starts = "()[]{}$><\\'*+,_-./:@#"

    lower_ingr = ingredient.lower()
    result = re.search(r"\W?\w?\s", lower_ingr)
    if result and result.start() == 0:
        lower_ingr = lower_ingr[result.end():]

    while lower_ingr and lower_ingr[0] in bad_starts:
        lower_ingr = lower_ingr[1:]

    return lower_ingr


def get_ingr_freq_dict(recipe_data):
    # gets all the ingredients for all the recipes
    all_recipes = recipe_data["NER"].values

    # builds an ingredient frequency dictionary
    ingr_dict = {}
    for recipe in all_recipes:

        # gives a list of ingredients:str
        ingredients = recipe[2:-2].strip("[]").split('", "')

        # add ingredients to dictionary
        for ingredient in ingredients:
            ingredient = get_cleaned_ingredient(ingredient)
            if ingredient:
                if ingredient not in ingr_dict:
                    ingr_dict[ingredient] = 1
                else:
                    ingr_dict[ingredient] += 1

    return ingr_dict

def get_random_weighted_pantry(items_with_frequencies, sample_size=35):

    # This is custom-defined
    available_ingredients = ["salt", "sugar", "water", "olive oil", "pepper"]
    items, frequencies = zip(*items_with_frequencies)

    while len(available_ingredients) < sample_size:

        # sample a random ingredient and add to pantry if it's not in there yet
        sampled_item = random.choices(items, weights=frequencies, k=1)[0]
        if sampled_item not in available_ingredients:
            available_ingredients.append(sampled_item)

    return available_ingredients


# gets row of df as input
def format_recipe(recipe):
    title = recipe["title"]
    # this gets all ingredients in a nicely structured list
    ingredients = recipe["ingredients"][2:-2].strip("[]").split('", "')
    directions = recipe["directions"][2:-2].strip("[]").split('", "')

    base_ingredients = recipe["NER"][2:-2].strip("[]").split('", "')
    base_ingredients = [get_cleaned_ingredient(ingredient) for ingredient in base_ingredients]

    formatted_output = f"- TITLE OF RECIPE: {title}. "
    formatted_output += "INGREDIENTS AND THEIR QUANTITIES: "
    for ingredient in ingredients:
        formatted_output += f"{ingredient}, "
    formatted_output = formatted_output[:-2] + ". "

    formatted_output += "DIRECTIONS: "
    for i, direction in enumerate(directions):
        formatted_output += f"Step {i + 1}. {direction} "

    formatted_output += f"END OF RECIPE.    "
    return formatted_output, base_ingredients


# gets df of recipes and number of desired recipes as input
def get_formatted_recipes(all_recipes, sample_size):
    formatted_outputs = []

    if sample_size > len(all_recipes):
        print("Invalid Sample Size")
        return None

    # get random recipes
    random_idcs = random.sample(range(len(all_recipes)), sample_size)
    random_recipes = all_recipes.iloc[random_idcs]

    # format recipes and append to list
    for row_idx in range(len(random_recipes)):
        recipe = random_recipes.iloc[row_idx]
        formatted_recipe, required_ingredients = format_recipe(recipe)

        formatted_outputs.append((formatted_recipe, required_ingredients))

    return formatted_outputs


def get_intersection(pantry, recipe_ingredients):
    return set(pantry).intersection(set(recipe_ingredients))


def sort_recipes(formatted_output, pantry, sorting="balanced"):
    # there are multiple types of sorting that make sense
    # "relative" -> sorts based on how many ingredients you have from the recipe. The higher the percentage, the higher the rating. This
    #               prioritizes using ingredients you already have
    # "absolute" -> sorts based on how many ingredients you are still missing. The fewer missing ingredients, the higher the rating. This
    #               prioritizes having to buy as few additional ingredients as possible
    # Future Work: it could be nice to balance this? i.e. to not see this as two completely separate options, but to have a trade-off?

    def weighted_score(recipe_ingredients):
        total_ingredients = len(recipe_ingredients)
        available_ingredients = len(get_intersection(pantry, recipe_ingredients))
        missing_ingredients = total_ingredients - available_ingredients

        # Relative proportion of ingredients you have
        relative_score = available_ingredients / total_ingredients

        # Penalize recipes with more missing ingredients, but allow some trade-off
        penalty = missing_ingredients / total_ingredients

        # Combine relative score and penalty (you can tweak the weights)
        return relative_score - 1 * penalty


    if sorting == "relative":
        key = lambda x: len(get_intersection(pantry, x[1])) / len(x[1])
        sorted_recipes = sorted(formatted_output, key=key, reverse=True)
    elif sorting == "absolute":
        key = lambda x: len(x[1]) - len(get_intersection(pantry, x[1]))
        sorted_recipes = sorted(formatted_output, key=key)
    elif sorting == "balanced":
        key = lambda x: weighted_score(x[1])
        sorted_recipes = sorted(formatted_output, key=key, reverse=True)
    else:
        sorted_recipes = None

    return sorted_recipes


def get_question_as_string(list_of_recipe_tuples, pantry):
    string_output = "Here are the ingredients you have available in your pantry: "
    for ingredient in pantry:
        string_output += f"{ingredient}, "
    string_output = string_output[:-2] + ". "

    string_output += "Here are the suggested recipes: "
    for (whole_recipe, _) in list_of_recipe_tuples:
        string_output += f"{whole_recipe}"

    string_output += ". Based on the items in my pantry, how would you rank these recipes? I want to use as many ingredients from my pantry as possible."

    return string_output


def get_answer_as_string(list_of_recipe_tuples, pantry, sorting="balanced"):
    # First sort the recipe_tuples
    list_of_recipe_tuples = sort_recipes(list_of_recipe_tuples, pantry, sorting=sorting)

    # Now construct the string
    string_output = ""

    for rank, (whole_recipe, recipe_ingredients) in enumerate(list_of_recipe_tuples):
        
        recipe_title = whole_recipe.split(". INGREDIENTS AND THEIR QUANTITIES")[0].split("TITLE OF RECIPE: ")[-1]

        intersection = get_intersection(pantry, recipe_ingredients)
        string_output += f"Rank {rank + 1}: {recipe_title}. "
        string_output += f"Rank {rank + 1} has been chosen for this recipe "

        if sorting == "relative" or sorting == "balanced":
            string_output += f"because you have {len(intersection)} out of {len(recipe_ingredients)} ingredients in your pantry! "
        elif sorting == "absolute":
            string_output += f"because you only need {len(recipe_ingredients) - len(intersection)} ingredients more! "

        # If some ingredients are missing
        if len(recipe_ingredients) - len(intersection) > 0:
            string_output += "Here are the ingredients you still need: "

            for ingredient in recipe_ingredients:
                if ingredient not in intersection:
                    string_output += f"{ingredient}, "
            string_output = string_output[:-2] + ". "

    return string_output


def generate_answer_question_pairs(recipe_data, ingr_dict):

    RECIPES_TO_RANK = 5

    # get a list of ingredient-frequency tuples
    ingr_with_freqs = list(ingr_dict.items())

    # randomly assort a pantry based on usually occurring ingredients
    pantry = get_random_weighted_pantry(ingr_with_freqs)
    # randomly select recipes from dataset
    random_recipes = get_formatted_recipes(recipe_data, sample_size=RECIPES_TO_RANK)

    question = get_question_as_string(random_recipes, pantry)
    answer = get_answer_as_string(random_recipes, pantry)

    return question, answer


# -------------- Main -------------------
def generate():
    print("generate()")

    # This CSV only contains recipes with ingredients that occur at least 500 times in 2 million+ recipes
    df = pd.read_csv("data/reduced_original_dataset.csv")

    ingr_freq_dict = get_ingr_freq_dict(df)

    # Make dataset folders
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    NUM_ITERATIONS = 34  # INCREASE TO CREATE A LARGE DATASET (1 iteration is 1214 tokens; trained for 3 epochs that's about 3 cents; 34 iterations is $1)

    # Loop to generate and save the content
    for i in range(0, NUM_ITERATIONS):
        if i % 1000 == 0:
            print(f"Generating batch: {i}")

        question, answer = generate_answer_question_pairs(df, ingr_freq_dict)
        json_format = f"""[{{"question": "{question}", "answer": "{answer}"}}]"""

        # Create a unique filename for each iteration
        file_name = f"{OUTPUT_FOLDER}/recipe_qa_{i}.txt"
        # Save
        with open(file_name, "w") as file:
            file.write(json_format)


def prepare():
    print("prepare()")

    # Get the generated files
    output_files = glob.glob(os.path.join(OUTPUT_FOLDER, "recipe_qa_*.txt"))
    output_files.sort()

    # Consolidate the data
    output_pairs = []
    errors = []
    for i, output_file in enumerate(output_files):
        
        if i % 1000 == 0:
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
    output_pairs_df.drop_duplicates(subset=['question'], inplace=True)
    output_pairs_df = output_pairs_df.dropna()
    print("Shape:", output_pairs_df.shape)
    print(output_pairs_df.head())
    filename = os.path.join(OUTPUT_FOLDER, "instruct-dataset.csv")
    output_pairs_df.to_csv(filename, index=False)

    # Build training formats
    output_pairs_df['text'] = "human: " + output_pairs_df['question'] + "\n" + "bot: " + output_pairs_df['answer']

    # Gemini Data prep: https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-supervised-tuning-prepare
    # {"contents":[{"role":"user","parts":[{"text":"..."}]},{"role":"model","parts":[{"text":"..."}]}]}
    output_pairs_df["contents"] = output_pairs_df.apply(
        lambda row: [{"role": "user", "parts": [{"text": row["question"]}]},
                     {"role": "model", "parts": [{"text": row["answer"]}]}], axis=1)

    # Test train split
    df_train, df_test = train_test_split(output_pairs_df, test_size=0.15, random_state=42)
    df_train[["text"]].to_csv(os.path.join(OUTPUT_FOLDER, "train.csv"), index=False)
    df_test[["text"]].to_csv(os.path.join(OUTPUT_FOLDER, "test.csv"), index=False)

    # Gemini : Max numbers of examples in validation dataset: 256
    df_test = df_test[:256]

    # JSONL
    with open(os.path.join(OUTPUT_FOLDER, "train.jsonl"), "w") as json_file:
        json_file.write(df_train[["contents"]].to_json(orient='records', lines=True))
    with open(os.path.join(OUTPUT_FOLDER, "test.jsonl"), "w") as json_file:
        json_file.write(df_test[["contents"]].to_json(orient='records', lines=True))


def upload():
    print("upload()")

    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    timeout = 300

    data_files = glob.glob(os.path.join(OUTPUT_FOLDER, "*.jsonl")) + glob.glob(os.path.join(OUTPUT_FOLDER, "*.csv"))
    data_files.sort()

    # Upload
    for index, data_file in enumerate(data_files):
        filename = os.path.basename(data_file)
        destination_blob_name = os.path.join("llm-finetune-dataset-small", filename)
        blob = bucket.blob(destination_blob_name)
        print("Uploading file:", data_file, destination_blob_name)
        blob.upload_from_filename(data_file, timeout=timeout)



def main(args=None):
    print("CLI Arguments:", args)

    if args.generate:
        generate()

    if args.prepare:
        prepare()

    if args.upload:
        upload()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate data",
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Prepare data",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload data to bucket",
    )

    args = parser.parse_args()

    main(args)