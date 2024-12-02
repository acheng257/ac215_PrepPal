#!/bin/bash

# exit immediately if a command exits with a non-zero status
#set -e

# Define some environment variables
export IMAGE_NAME="preppal-app-deployment"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export GCP_PROJECT="preppal-438123"
export GCP_ZONE="us-east1-c"
export GCP_REGION="us-east1"
export GOOGLE_APPLICATION_CREDENTIALS=/secrets/deployment.json
# export GCS_BUCKET_NAME="cheese-app-ml-workflow-demo" -> ML WORKFLOW
# export GCS_SERVICE_ACCOUNT="ml-workflow@ac215-project.iam.gserviceaccount.com" -> ML WORKFLOW
# export GCS_PACKAGE_URI="gs://cheese-app-trainer-code" -> ML WORKFLOW

# Build the image based on the Dockerfile
#docker build -t $IMAGE_NAME -f Dockerfile .
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$HOME/.ssh":/home/app/.ssh \
-v "$BASE_DIR/../apiservice":/apiservice \
-v "$BASE_DIR/../frontend-react":/frontend-react \
-v "$BASE_DIR/../llm-rag":/llm-rag \
-v "$BASE_DIR/../postgres-db":/postgres-db \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e USE_GKE_GCLOUD_AUTH_PLUGIN=True \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCP_ZONE=$GCP_ZONE \
-e GCP_REGION=$GCP_REGION \
$IMAGE_NAME

# -v "$BASE_DIR/../data-collector":/data-collector \ -> ML WORKFLOW
# -v "$BASE_DIR/../data-processor":/data-processor \ -> ML WORKFLOW
# -e GCS_SERVICE_ACCOUNT=$GCS_SERVICE_ACCOUNT \
# -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \ -> ML WORKFLOW
# -e GCS_PACKAGE_URI=$GCS_PACKAGE_URI \ -> ML WORKFLOW
# -e WANDB_KEY=$WANDB_KEY \ -> ML WORKFLOW
