from fastapi import APIRouter, HTTPException
from google.cloud import storage
import json
import os

router = APIRouter()


def get_bucket():
    storage_client = storage.Client()
    return storage_client.bucket(os.getenv("GCS_BUCKET_NAME"))


@router.get("/{user_id}")
async def get_user_pantry(user_id: str):
    GCS_PANTRY_FOLDER = os.getenv("GCS_PANTRY_FOLDER", "pantry")
    try:
        file_path = f"{GCS_PANTRY_FOLDER}/{user_id}.json"
        bucket = get_bucket()
        blob = bucket.blob(file_path)

        if not blob.exists():
            default_pantry_json = json.dumps({})
            blob.upload_from_string(default_pantry_json, content_type="application/json")
            return {"user_id": user_id, "pantry": {}}

        pantry_data = blob.download_as_text()
        return {"user_id": user_id, "pantry": json.loads(pantry_data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.put("/{user_id}")
async def update_user_pantry(user_id: str, pantry_data: dict):
    GCS_PANTRY_FOLDER = os.getenv("GCS_PANTRY_FOLDER", "pantry")
    try:
        file_path = f"{GCS_PANTRY_FOLDER}/{user_id}.json"
        bucket = get_bucket()
        blob = bucket.blob(file_path)

        # Upload pantry data as JSON
        blob.upload_from_string(data=json.dumps(pantry_data), content_type="application/json")

        return {"message": "Pantry updated successfully", "user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.delete("/{user_id}")
async def delete_user_pantry(user_id: str):
    GCS_PANTRY_FOLDER = os.getenv("GCS_PANTRY_FOLDER", "pantry")
    try:
        file_path = f"{GCS_PANTRY_FOLDER}/{user_id}.json"
        bucket = get_bucket()
        blob = bucket.blob(file_path)

        if not blob.exists():
            raise HTTPException(status_code=404, detail="User pantry not found")
        blob.delete()

        return {"message": "Pantry deleted successfully", "user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
