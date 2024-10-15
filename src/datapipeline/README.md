**Data**
We gathered a dataset of 100,000 cheese images representing approximately 1,500 different varieties. The dataset, approximately 100GB in size, was collected from the following sources: (1), (2), (3). We have stored it in a private Google Cloud Bucket.
Additionally, we compiled 250 bibliographical sources on cheese, including books and reports, from sources such as (4) and (5).

**Data Pipeline Containers**

1. One container processes the 100GB dataset by resizing the images and storing them back to Google Cloud Storage (GCS).

   **Input:** Source and destination GCS locations, resizing parameters, and required secrets (provided via Docker).

   **Output:** Resized images stored in the specified GCS location.

2. Another container prepares data for the RAG model, including tasks such as chunking, embedding, and populating the vector database.

## Data Pipeline Overview

1. **`src/datapipeline/preprocess_cv.py`**
   This script handles preprocessing on our 100GB dataset. It reduces the image sizes to 128x128 (a parameter that can be changed later) to enable faster iteration during processing. The preprocessed dataset is now reduced to 10GB and stored on GCS.

2. **`src/datapipeline/preprocess_rag.py`**
   This script prepares the necessary data for setting up our vector database. It performs chunking, embedding, and loads the data into a vector database (ChromaDB).

3. **`src/datapipeline/Pipfile`**
   We used the following packages to help with preprocessing:

   - `special cheese package`

4. **`src/preprocessing/Dockerfile(s)`**
   Our Dockerfiles follow standard conventions, with the exception of some specific modifications described in the Dockerfile/described below.

## Running Dockerfile

Instructions for running the Dockerfile can be added here.
To run Dockerfile - `Instructions here`