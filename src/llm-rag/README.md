## Building a RAG system with Vector DB

This is the part of the application where we build a Retrieval-Augmented Generation (RAG) system using a vector database. The system will clean the dataset, chunk text documents, create embeddings, and store them in a vector database. The vector database embeddings will be used by the LLM to enhance its response and provide recipes that allign with user preferences. 

**Data**
We utilized a dataset containing 522,517 recipes from 312 different categories, sourced from the [Food.com - Recipes dataset](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews) on Kaggle. This dataset includes details such as cooking times, servings, ingredients, nutritional information, and step-by-step instructions for each recipe. The raw dataset was stored in Google Cloud Platform, and after data cleaning, we worked with approximately 300,000 recipes.

**Data Pipeline Containers**

1. One container processes the 100GB dataset by resizing the images and storing them back to Google Cloud Storage (GCS).

   **Input:** Source and destination GCS locations, resizing parameters, and required secrets (provided via Docker).

   **Output:** Resized images stored in the specified GCS location.

2. Another container prepares data for the RAG model, including tasks such as chunking, embedding, and populating the vector database.

1. llm-rag: in this container we prepare the data for the RAG model, including tasks such as data cleaning, chunking, embedding, and populating the vector database.
2. llm-rag-chromadb:  

## Data Pipeline Overview

1. **`src/datapipeline/preprocess_recipes.py`**
   This script handles preprocessing on our 100GB dataset. It reduces the image sizes to 128x128 (a parameter that can be changed later) to enable faster iteration during processing. The preprocessed dataset is now reduced to 10GB and stored on GCS.

2. **`src/datapipeline/preprocess_rag.py`**
   This script prepares the necessary data for setting up our vector database. It performs chunking, embedding, and loads the data into a vector database (ChromaDB).

3. **`src/datapipeline/cli.py`**

4. **`src/datapipeline/Pipfile`**
   We used the following packages to help with preprocessing:

   - `special cheese package`

5. **`src/preprocessing/Dockerfile`**
   Our Dockerfiles follow standard conventions, with the exception of some specific modifications described in the Dockerfile/described below.

6. **`src/preprocessing/docker-compose.yml`**


## Running Dockerfile

Instructions for running the Dockerfile can be added here.
To run Dockerfile - `Instructions here`