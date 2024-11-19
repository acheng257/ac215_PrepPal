#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="preppal-api-service"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export PERSISTENT_DIR=$(pwd)/../../../persistent-folder/

# More environment variables for GCP functionality
export GCP_PROJECT="preppal-438123"
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-service-account.json"
export MODEL_ENDPOINT_GOOGLE_APPLICATION_CREDENTIALS="/secrets/preppal-llm-service-account.json"
export GCS_BUCKET_NAME="preppal-data"
export CHROMADB_HOST="llm-rag-chromadb"
export CHROMADB_PORT=8000

# Create network if we don't have it yet
docker network inspect llm-rag-network >/dev/null 2>&1 || docker network create llm-rag-network

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$PERSISTENT_DIR":/persistent \
-p 9000:9000 \
-e DEV=1 \
-e GCP_PROJECT=$GCP_PROJECT \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e MODEL_ENDPOINT_GOOGLE_APPLICATION_CREDENTIALS=$MODEL_ENDPOINT_GOOGLE_APPLICATION_CREDENTIALS \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e CHROMADB_HOST=$CHROMADB_HOST \
-e CHROMADB_PORT=$CHROMADB_PORT \
--network llm-rag-network \
$IMAGE_NAME
