from fastapi import APIRouter, HTTPException
from google.cloud import storage
import json
import os

# Initialize FastAPI router
router = APIRouter()

# Set GCS bucket details (use environment variables for security)
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
GCS_PANTRY_FOLDER = os.getenv("GCS_PANTRY_FOLDER", "pantry")

# Initialize GCS client
storage_client = storage.Client()

def get_bucket():
    """
    Fetches the GCS bucket instance.
    """
    return storage_client.bucket(GCS_BUCKET_NAME)

@router.get("/{user_id}")
async def get_user_pantry(user_id: str):
    """
    Fetches the pantry data for a specific user from the GCS bucket.
    """
    try:
        file_path = f"{GCS_PANTRY_FOLDER}/{user_id}.json"
        bucket = get_bucket()
        blob = bucket.blob(file_path)

        if not blob.exists():
            raise HTTPException(status_code=404, detail="User pantry not found")

        pantry_data = blob.download_as_text()
        return {"user_id": user_id, "pantry": json.loads(pantry_data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/{user_id}")
async def update_user_pantry(user_id: str, pantry_data: dict):
    """
    Updates or creates pantry data for a specific user in the GCS bucket.
    """
    try:
        file_path = f"{GCS_PANTRY_FOLDER}/{user_id}.json"
        bucket = get_bucket()
        blob = bucket.blob(file_path)

        # Upload pantry data as JSON
        blob.upload_from_string(
            data=json.dumps(pantry_data),
            content_type="application/json"
        )

        return {"message": "Pantry updated successfully", "user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/{user_id}")
async def delete_user_pantry(user_id: str):
    """
    Deletes pantry data for a specific user from the GCS bucket.
    """
    try:
        file_path = f"{GCS_PANTRY_FOLDER}/{user_id}.json"
        bucket = get_bucket()
        blob = bucket.blob(file_path)

        if not blob.exists():
            raise HTTPException(status_code=404, detail="User pantry not found")

        # Delete the blob
        blob.delete()

        return {"message": "Pantry deleted successfully", "user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
