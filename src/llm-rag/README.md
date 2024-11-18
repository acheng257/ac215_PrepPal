## Building a RAG system with Vector DB and LLM

This is the part of the application where we build a Retrieval-Augmented Generation (RAG) system using a vector database. The system will clean the dataset, chunk text documents, create embeddings, and store them in a vector database. The vector database embeddings will be used by the LLM to enhance its response and provide recipes that align with user preferences.

**Data** <br>
We utilized a dataset containing 522,517 recipes from 312 different categories, sourced from the [Food.com - Recipes dataset](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews) on Kaggle. This dataset includes details such as cooking times, servings, ingredients, nutritional information, and step-by-step instructions for each recipe. The raw dataset was stored in a Google Cloud Platform (GCP) private bucket.

**Data Pipeline Containers** <br>
1. <b> llm-rag container </b> <br>
   This container handles the preparation of data for the RAG model, including data cleaning, chunking, embedding, and populating the vector database. It also integrates the fine-tuned LLM with the vector database and implements the chat functionality, allowing seamless interaction between the model and the data.
2. <b> llm-rag-chromadb container </b> <br>
   This container hosts the ChromaDB vector database for storing and retrieving embeddings in the RAG pipeline. It ensures persistent data storage and serves the database on port 8000 for real-time access.

## Data Pipeline Overview

1. **`src/llm-rag/preprocess_recipes.py`** <br>
   This script performs data cleaning on a dataset of recipes by processing and formatting key fields. It converts ISO 8601 duration fields like cook time, prep time, and total time into human-readable formats and calculates their equivalent in minutes. Ingredient quantities and parts are combined into a single string, while recipe instructions are cleaned and formatted into numbered steps. After cleaning, unnecessary columns are dropped, missing values are removed, and the final dataset is prepared for further use.

2. **`src/llm-rag/preprocess_rag.py`** <br>
   This script prepares data for our vector database, handling both the knowledge base of 300,000 recipes and user-uploaded recipes. It performs two types of chunking: entire recipe chunking to preserve complete information, and sliding window chunking (500 characters with 100-character overlap) to ensure continuity across chunks. The script then embeds the data and loads it into ChromaDB, creating two separate collections for each chunking method. Metadata is also stored to distinguish between knowledge base recipes and user-uploaded ones, along with the corresponding user number.

3. **`src/llm-rag/model_rag.py`** <br>
   This script integrates the LLM model with the vector database, embedding user queries and using cosine similarity to retrieve the most relevant recipes from the database.

4. **`src/llm-rag/cli.py`** <br>
   This script provides a command-line interface for the data pipeline, allowing users to clean, chunk, embed, and load recipe data into the vector database, with options to specify chunking methods and enable downloading or uploading of data to and from the GCP bucket.

5. **`src/llm-rag/Pipfile`** <br>
   We used the following packages to help with preprocessing: `numpy`, `pandas`, `isodate`, `sentence-transformers`, `langchain`

6. **`src/llm-rag/Dockerfile`** <br>
   Our Dockerfiles follow standard conventions.

7. **`src/llm-rag/docker-compose.yml`** <br>
   This Docker Compose configuration sets up the llm-rag service and the ChromaDB container, enabling the integration of the RAG model with ChromaDB. It defines network settings, mounts volumes for secrets and application data, and configures environment variables for Google Cloud credentials, while allowing optional GPU access for the llm-rag container.

## Steps to run the RAG system

### Prerequisites
   * Download the recipes dataset from [Kaggle](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews)
   * Create the folder `/rag_data/knowledge_base` inside the GCP bucket you previosuly created
   * Store the dataset in the `/rag_data/knowledge_base` folder

### Running the containers
   * Make sure you are inside the llm-rag folder
   * Run `sh docker-shell.sh`

### Clean Dataset
   Run the cli.py script with the --clean_dataset flag to preprocess the recipes in a format ready for the RAG setup. You will need to have the raw dataset in the environmnet you are running these commands. For that you can use the --download flag. If you also want to store the preprocessed dataset in the GCP bucket, you the --upload flag.

   `python cli.py --clean_dataset --download --upload`

### Chunk Documents
   Run the cli.py script with the --chunk flag to split and store your input recipes into chunks. Use the --download and --upload flags as needed.

   <b> Perform entire recipe splitting: </b>

   `python cli.py --chunk --chunk_type entire_recipe --dowload --upload`

   <b> Perform sliding window splitting: </b>

   `python cli.py --chunk --chunk_type sliding_window --dowload --upload`

   This will: <br>
   * Read the `processed_recipes.csv` dataset in the /rag_data/knowledge_base directory
   * Split the text into chunks using the specified method (entire_recipe or sliding_window)
   * Save the chunks and the recipes associated with them as JSONL files in the outputs directory

### Generate Embeddings
   Generate embeddings for the text chunks:

   `python cli.py --embed --chunk_type entire_recipe --dowload --upload`

   `python cli.py --embed --chunk_type sliding_window --dowload --upload`

   This will: <br>
   * Reads the chunk files created in the previous section
   * Uses SentenceTransformer multi-qa-MiniLM-L6-cos-v1 text embedding model to generate embeddings for each chunk
   * Saves the chunks with their embeddings as new JSONL files

### Load Embeddings into Vector Database
   Load the generated embeddings into ChromaDB:

   `python cli.py --load --chunk_type entire_recipe --dowload`

   `python cli.py --load --chunk_type sliding_window --dowload`

   This will: <br>
   * Connect to your ChromaDB instance
   * Create a new collection (or clears an existing one)
   * Load the embeddings and associated metadata into the collection

### Chat with LLM
   Chat with the LLM using the RAG system:

   `python cli.py --chat --chunk_type entire_recipe`

   `python cli.py --chat --chunk_type sliding_window`

   This will: <br>
   * Takes a sample query
   * Retrieves relevant context from the vector database
   * Sends the query and context to the LLM
   * Displays the LLM's response
