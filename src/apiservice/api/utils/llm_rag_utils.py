import os
import numpy as np
from typing import Dict
from fastapi import HTTPException
import traceback
import chromadb
import vertexai
from sentence_transformers import SentenceTransformer
from vertexai.generative_models import GenerativeModel
from google.cloud import aiplatform


# Setup Global Variables
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_REGION = os.environ["GCP_REGION"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
CHROMADB_HOST = os.environ["CHROMADB_HOST"]
CHROMADB_PORT = os.environ["CHROMADB_PORT"]

GENERATIVE_MODEL = "gemini-1.5-flash-002"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256

MODEL_ENDPOINT = "projects/639023682337/locations/us-east1/endpoints/1030677801830711296"  # Finetuned model


# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 6000,  # Maximum number of tokens for output
    "temperature": 0.1,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}

# Define Embedding Model
embedding_model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")

client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
method = "entire_recipe"
collection_name = f"{method}_collection"
collection = client.get_collection(name=collection_name)


# -------------------- Functions ------------------------
def get_most_recent_endpoint(project, location):

    aiplatform.init(project=project, location=location)
    endpoints = aiplatform.Endpoint.list()

    # If no endpoints exist, return None
    if not endpoints:
        print("No endpoints found.")
        return None

    # Sort endpoints by create_time (newest first)
    most_recent_endpoint = max(endpoints, key=lambda ep: ep.create_time)

    return most_recent_endpoint


def generate_query_embedding(query):
    return embedding_model.encode(query)


def generate_recommendation_list(content_dict: Dict):
    pantry = content_dict["pantry"]
    ingredients = content_dict["ingredients"]
    ingredients_query = f"I want to use {ingredients} to cook a recipe."
    print("GENERATING RECOMMENDATIONS...")

    try:
        # Create embeddings for the message content
        query_embedding = generate_query_embedding(ingredients_query)
        if isinstance(query_embedding, np.ndarray):
            query_embedding = query_embedding.tolist()

        # Retrieve chunks based on embedding value
        results = collection.query(query_embeddings=[query_embedding], n_results=6)
        possible_recipes = "Possible Recipes:\n" + "\n".join(results["documents"][0])

        print("Items in pantry: ", pantry)
        INPUT_PROMPT = f"""
            {ingredients_query}\n
            Here are the ingredients I have available in my pantry: {pantry}\n
            {possible_recipes}
            \n\nBased on the items in my pantry, how would you rank these recipes? I want to use as many ingredients from my pantry as possible.
        """

        # Initialize the GenerativeModel (uncomment below)
        vertexai.init(project=GCP_PROJECT, location=GCP_REGION)
        # most_recent_endpoint = get_most_recent_endpoint(GCP_PROJECT, GCP_REGION)
        generative_model = GenerativeModel(MODEL_ENDPOINT)

        # Generate Recipe Recommendation List
        response = generative_model.generate_content(
            INPUT_PROMPT,
            generation_config=generation_config,
            safety_settings=None,
        )

        recipe_recommendations = response.text
        return {"ranking": recipe_recommendations, "possible_recipes": possible_recipes}

    except Exception as e:
        print(f"Error generating response: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")


def get_recipe_measurements(title: str, servings: str, time: str, ingredients: str, calories: str, instructions: str):

    SYSTEM_INSTRUCTIONS = """
        You are a recipe assistant. Your task is to add appropriate measurements (e.g., teaspoons, cups, ounces, etc.) to the provided list of ingredients in a recipe.
        The measurements should be contextually appropriate based on typical recipes. Do not add or remove any ingredients, and do not modify any other part of the recipe,
        such as the title, cooking time, or instructions. Do not change the number that indicates the quantity of the ingredient. Just add the measurement.
        Maintain the original order of the ingredients in the list. If the context is unclear, make a reasonable assumption and proceed with a plausible measurement.

        Here is an example of the expected format:
        ```3 tbsp cornstarch, 1/2 cup water, 2 tbsp water, 1/2 tsp garlic powder, 1 cup boneless round steak, 2 cups broccoli florets, 4 onion,
        1 tbsp reduced sodium soy sauce, 1/3 tbsp brown sugar, 2 tsp ground ginger, 1 cup cooked rice```

    """
    prompt = f"""
        You are a recipe assistant. Your task is to add appropriate measurements (e.g., teaspoons, cups, ounces, etc.) to the provided list of ingredients in a recipe.
        The measurements should be contextually appropriate based on typical recipes. Do not add or remove any ingredients, and do not modify any other part of the recipe,
        such as the title, cooking time, calories, serving sizes, or cooking instructions. Maintain the original order of the ingredients in the list. If the context is unclear,
        make a reasonable assumption and proceed with a plausible measurement.

        Here is the information you will work with:
        Title: {title}
        Calories: {calories}
        Serving Size: {servings}
        Cooking Time: {time}
        Cooking Instructions: {instructions}

        Ingredients (to be adjusted with appropriate measurements):
        {ingredients}

        Please return just the list of ingredients with appropriate measurements added. Do not alter anything else.
    """

    vertexai.init(project=GCP_PROJECT, location=GCP_REGION)
    gen_model = GenerativeModel(GENERATIVE_MODEL, system_instruction=[SYSTEM_INSTRUCTIONS])
    responses = gen_model.generate_content([prompt], generation_config=generation_config)
    generated_text = responses.text

    return generated_text


def update_pantry_with_llm(pantry: dict, used_ingredients: list):

    pantry_str = [f"{key}: {value}" for key, value in pantry.items()]
    pantry_str = ", ".join(pantry_str)
    # used_ingredients_str = ", ".join(used_ingredients)

    SYSTEM_INSTRUCTIONS = """
        You are given two inputs:

        Pantry: A string representing ingredient names and their quantities, formatted as: "salt: 1, bell pepper: 15, potato: 3".
        Used Ingredients: A string describing the ingredients used in a recipe, formatted as: "1 tbsp butter, 1 tsp salt, 3 medium bell peppers".

        Task:
        Parse the pantry string into a dictionary where keys are ingredient names and values are their quantities.
        Parse the used ingredients to determine which ingredients were used.
        Match used ingredients to pantry items and update the quantities in the pantry. Use your best judgment to match closely related items (e.g., "bell pepper" matches "bell peppers").
        Do not update staple pantry ingredients, such as:
        - Water
        - Spices (e.g., salt, pepper, oregano, cinnamon, red pepper flakes)
        - Oils (e.g., olive oil, vegetable oil)
        - Condiments (e.g., soy sauce, vinegar)
        Only update perishables like fruits, vegetables, dairy, bread, and meat. Reduce the quantity for matched items by 1 for each occurrence.
        Ensure quantities do not become negative.
        Output the updated pantry in the same string format as the input (e.g., "salt: 1, bell pepper: 12, potato: 3").
        Example:
        Input:
        Pantry: "salt: 1, bell pepper: 15, potato: 3"

        Used Ingredients: "1 tbsp butter, 1 tsp salt, 3 medium bell peppers"

        Output:
        "salt: 1, bell pepper: 12, potato: 3"

        DO NOT OUTPUT PYTHON CODE.

    """

    prompt = f"""
        Here is my pantry: {pantry}
        Here are the ingredients I used: {used_ingredients}

        Please give me the updated pantry.
    """

    vertexai.init(project=GCP_PROJECT, location=GCP_REGION)
    gen_model = GenerativeModel(GENERATIVE_MODEL, system_instruction=[SYSTEM_INSTRUCTIONS])
    responses = gen_model.generate_content([prompt], generation_config=generation_config)
    generated_text = responses.text

    try:
        items = generated_text.split(", ")
        updated_pantry_dict = {}
        for item in items:
            ingr, quantity = item.split(": ")
            updated_pantry_dict[ingr] = int(quantity)
    except Exception as e:
        print("ERROR", e)
        print("Not updating pantry...")
        updated_pantry_dict = pantry

    print("\n\n\n")
    print("Checking Pantry Update...")
    print("Pantry", pantry)
    print("Used Ingredients", used_ingredients)
    print("teehee", updated_pantry_dict)
    print("\n\n\n")

    return updated_pantry_dict
