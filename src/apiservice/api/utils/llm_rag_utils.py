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
from google.oauth2 import service_account


# Setup Global Variables
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_REGION = os.environ["GCP_REGION"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
CHROMADB_HOST = os.environ["CHROMADB_HOST"]
CHROMADB_PORT = os.environ["CHROMADB_PORT"]

EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256

MODEL_ENDPOINT = "projects/582280928569/locations/us-central1/endpoints/3898306381651902464"  # Finetuned model


# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.75,  # Control randomness in output
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

    try:
        # Create embeddings for the message content
        query_embedding = generate_query_embedding(ingredients_query)
        if isinstance(query_embedding, np.ndarray):
            query_embedding = query_embedding.tolist()

        # Retrieve chunks based on embedding value
        results = collection.query(query_embeddings=[query_embedding], n_results=5)
        possible_recipes = f"""
        Possible Recipes:\n
        {"\n".join(results["documents"][0])}
        """

        INPUT_PROMPT = f"""
        {ingredients_query}\n
        Here are the ingredients I have available in my pantry: {pantry}\n
        {possible_recipes}
        \n\nBased on the items in my pantry, how would you rank these recipes? I want to use as many ingredients from my pantry as possible.
        """

        # # Load the fine-tuning credentials 
        fine_tuning_key_path = os.getenv("MODEL_ENDPOINT_GOOGLE_APPLICATION_CREDENTIALS")
        credentials = service_account.Credentials.from_service_account_file(fine_tuning_key_path)
        vertexai.init(project=GCP_PROJECT, location=GCP_REGION, credentials=credentials)
        generative_model = GenerativeModel(MODEL_ENDPOINT)

        # Initialize the GenerativeModel (uncomment below)
        # credentials = GOOGLE_APPLICATION_CREDENTIALS
        # vertexai.init(project=GCP_PROJECT, location=GCP_REGION, credentials=credentials)
        # most_recent_endpoint = get_most_recent_endpoint(GCP_PROJECT, GCP_REGION)
        # generative_model = GenerativeModel(most_recent_endpoint)

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
