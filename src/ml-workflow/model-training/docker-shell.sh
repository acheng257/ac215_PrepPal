#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="preppal-model-training"
export BASE_DIR=$(pwd)
export PERSISTENT_DIR=$(pwd)/../../../../persistent-folder/
export SECRETS_DIR=$(pwd)/../../../../secrets/
export GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-service-account.json"
export GCP_PROJECT="preppal-438123"
export GCS_BUCKET_NAME="preppal-data"
export GCP_REGION="us-east1"
export GCS_PACKAGE_URI="ml-workflow/preppal_trainer_code"

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
# M1/2 chip macs use this line
#docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .
docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .

# Run Container
docker run --rm --name $IMAGE_NAME -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$PERSISTENT_DIR":/persistent \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
-e GCP_REGION=$GCP_REGION \
-e GCS_PACKAGE_URI=$GCS_PACKAGE_URI \
$IMAGE_NAME
