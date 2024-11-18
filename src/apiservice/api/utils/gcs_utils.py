from google.cloud import storage
import json
import os

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "your-gcs-bucket")
USER_DB_FILE = "user_db.json"

# Initialize GCS client
storage_client = storage.Client()


def get_bucket():
    return storage_client.bucket(GCS_BUCKET_NAME)


def load_user_db():
    """
    Load the user database from GCS.
    """
    bucket = get_bucket()
    blob = bucket.blob(USER_DB_FILE)
    if not blob.exists():
        return {}
    user_data = blob.download_as_text()
    return json.loads(user_data)


def save_user_db(user_db):
    """
    Save the updated user database to GCS.
    """
    bucket = get_bucket()
    blob = bucket.blob(USER_DB_FILE)
    blob.upload_from_string(json.dumps(user_db), content_type="application/json")
