import os
from google.cloud import storage

GCS_PACKAGE_URI = os.environ["GCS_PACKAGE_URI"]
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]


def upload_to_gcs(blob_name):
    """Uploads a file to Google Cloud Storage."""
    # Initialize the client
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket(GCS_BUCKET_NAME)

    # Create a new blob and upload the file
    blob = bucket.blob(f"{GCS_PACKAGE_URI}/{blob_name}")
    blob.upload_from_filename(blob_name)

    print(f"Uploaded '{blob_name}' to gs://{GCS_BUCKET_NAME}/{GCS_PACKAGE_URI}")


if __name__ == "__main__":
    # Variables
    blob_name = "trainer.tar.gz"

    # Upload file to GCS
    upload_to_gcs(blob_name)
