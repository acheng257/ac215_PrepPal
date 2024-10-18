#!/bin/bash

echo "Container is running!!!"

gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
if [[ $? -ne 0 ]]; then
  echo "ERROR: Failed to authenticate with Google Cloud!"
  exit 1
fi
mkdir -p /mnt/gcs_bucket
gcsfuse --key-file=$GOOGLE_APPLICATION_CREDENTIALS $GCS_BUCKET_NAME /mnt/gcs_data
echo 'GCS bucket mounted at /mnt/gcs_data'
mkdir -p /app/dvc_store /app/dvc_store/rag_data /app/dvc_store/rag_data/embedded_recipes_entire_recipe /app/dvc_store/rag_data/embedded_recipes_sliding_window
mount --bind /mnt/gcs_data/rag_data /app/dvc_store
mount --bind /mnt/gcs_data/rag_data/embedded_recipes_entire_recipe /app/dvc_store/rag_data/embedded_recipes_entire_recipe
mount --bind /mnt/gcs_data/rag_data/embedded_recipes_sliding_window /app/dvc_store/rag_data/embedded_recipes_sliding_window

pipenv shell