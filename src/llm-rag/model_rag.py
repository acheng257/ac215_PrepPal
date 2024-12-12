import chromadb
import os

from preprocess_rag import generate_query_embedding
from vertexai.generative_models import GenerativeModel

CHROMADB_HOST = "llm-rag-chromadb"
CHROMADB_PORT = 8000


# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 3000,  # Maximum number of tokens for output
    "temperature": 0.75,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}


def chat(method="entire_recipe"):
    print("chat()")

    # Connect to chroma DB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    # Get a collection object from an existing collection, by name. If it doesn't exist, create it.
    collection_name = f"{method}_collection"

    pantry = """Here are the ingredients I have available in my pantry: beef, mushrooms, butter, salt, pepper,
    garlic, onion, olive oil, flour, sugar, soy sauce, tomato paste, oregano, thyme, basil, parsley, paprika, cumin,
    cinnamon, baking powder, baking soda, eggs, milk, pasta, rice, canned tomatoes, chicken broth, vinegar, honey, mustard,
    chili powder, cornstarch, brown sugar, bread crumbs, parmesan cheese, bay leaves, lemon, carrots, potatoes, bell peppers,
    spinach, zucchini, celery, broccoli, cauliflower, peas, green beans, kale.
    """
    query = "I want to use beef, butter, and mushrooms to cook a recipe."
    query_embedding = generate_query_embedding(query)
    print("Query:", query)
    print("Embedding values:", query_embedding)
    # Get the collection

    collection = client.get_collection(name=collection_name)

    # Query based on embedding value
    results = collection.query(query_embeddings=[query_embedding], n_results=10)
    print("\n\nResults:", results)

    print(len(results["documents"][0]))

    INPUT_PROMPT = f"""
    {query}\n
    {pantry}\nPossible Recipes: \n
    {"\n".join(results["documents"][0])}
    \n\nBased on the items in my pantry, how would you rank these recipes? I want to use as many ingredients from my pantry as possible.
    """

    # INPUT_PROMPT = f"""
    # {query}\n
    # {pantry}\n
    # """

    print("INPUT_PROMPT: ", INPUT_PROMPT)

    # CHANGE GOOGLE CREDENTIAL SECRET FOR A BRIEF WHILE
    original_key_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    fine_tuning_key_path = os.getenv("FINETUNING_GOOGLE_APPLICATION_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = fine_tuning_key_path

    MODEL_ENDPOINT = "projects/582280928569/locations/us-central1/endpoints/3898306381651902464"  # Finetuned model
    generative_model = GenerativeModel(MODEL_ENDPOINT)
    # generative_model = GenerativeModel("gemini-1.5-flash-001")

    response = generative_model.generate_content(
        [INPUT_PROMPT],  # Input prompt
        generation_config=generation_config,  # Configuration settings
        stream=False,  # Enable streaming for responses
    )
    generated_text = response.text
    print("LLM Response:", generated_text)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = original_key_path
