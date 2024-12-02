import os
from google.cloud import storage

GCS_PACKAGE_URI = os.environ["GCS_PACKAGE_URI"]


def upload_to_gcs(blob_name):
    """Uploads a file to Google Cloud Storage."""
    # Initialize the client
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket(f"preppal-data/{GCS_PACKAGE_URI}")

    # Create a new blob and upload the file
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(blob_name)

    print(f"Uploaded '{blob_name}' to gs://preppal-data/{GCS_PACKAGE_URI}")


if __name__ == "__main__":
    # Variables
    blob_name = "trainer.tar.gz"

    # Upload file to GCS
    upload_to_gcs(blob_name)
