#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Set vairables
export BASE_DIR="$(pwd)"
export SECRETS_DIR="$(pwd)/../../../../secrets/" # CHANGE
export GCP_PROJECT="preppal-finetuning"
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/preppal-llm-service-account.json"
export GCS_BUCKET_NAME="preppal-data"
export IMAGE_NAME="llm-fine-tuner"


# Create the network if we don't have it yet
# docker network inspect datapipeline-network >/dev/null 2>&1 || docker network create datapipeline-network

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run All Containers
# docker-compose run --rm --service-ports $IMAGE_NAME


# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
$IMAGE_NAME
