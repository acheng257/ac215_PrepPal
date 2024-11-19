import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.routers import auth, pantry, recipes

sys.path.append("./")

# client = TestClient(auth.router)
auth_client = TestClient(auth.router)
pantry_client = TestClient(pantry.router)
recipes_client = TestClient(recipes.router)

mock_user_db = {"test_user": {"password": "secure_password", "user_id": "1"}}

GCS_BUCKET_NAME = "mock_bucket"
GCS_PANTRY_FOLDER = "mock_pantry_folder"


@pytest.fixture
def mock_gcs_utils():
    with patch("api.routers.auth.load_user_db", return_value=mock_user_db) as mock_load, patch("api.routers.auth.save_user_db") as mock_save:
        yield mock_load, mock_save


def test_login_success(mock_gcs_utils):
    mock_load, _ = mock_gcs_utils  # Explicitly reference mock_load
    mock_load.return_value = mock_user_db  # Ensure the mock database is correctly set

    response = auth_client.post("/login", data={"username": "test_user", "password": "secure_password"})
    assert response.status_code == 200
    assert response.json() == {"user_id": "1"}


def test_signup_success(mock_gcs_utils):
    mock_load, mock_save = mock_gcs_utils
    mock_load.return_value = {}

    response = auth_client.post("/signup", data={"username": "newuser", "password": "newpass"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully", "user_id": "1"}
    mock_save.assert_called_once_with({"newuser": {"password": "newpass", "user_id": "1"}})


@pytest.fixture
def mock_get_bucket():
    with patch("api.routers.pantry.get_bucket") as mock_get_bucket:
        mock_bucket = MagicMock()
        mock_blob = MagicMock()

        mock_get_bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob

        yield mock_bucket, mock_blob


def test_get_user_pantry_exists(mock_get_bucket):
    """
    Test retrieving existing pantry data.
    """
    mock_bucket, mock_blob = mock_get_bucket
    mock_blob.exists.return_value = True
    mock_blob.download_as_text.return_value = '{"item": "value"}'

    response = pantry_client.get("/12345")
    assert response.status_code == 200
    assert response.json() == {"user_id": "12345", "pantry": {"item": "value"}}
    mock_blob.exists.assert_called_once()
    mock_blob.download_as_text.assert_called_once()


def test_update_user_pantry(mock_get_bucket):
    """
    Test updating pantry data.
    """
    mock_bucket, mock_blob = mock_get_bucket

    response = pantry_client.put("/12345", json={"item": "new_value"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Pantry updated successfully",
        "user_id": "12345",
    }
    mock_blob.upload_from_string.assert_called_once_with(data='{"item": "new_value"}', content_type="application/json")


def test_delete_user_pantry_exists(mock_get_bucket):
    """
    Test deleting pantry data when it exists.
    """
    mock_bucket, mock_blob = mock_get_bucket
    mock_blob.exists.return_value = True

    response = pantry_client.delete("/12345")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Pantry deleted successfully",
        "user_id": "12345",
    }
    mock_blob.exists.assert_called_once()
    mock_blob.delete.assert_called_once()


@pytest.fixture
def mock_llm_utils():
    """
    Mock the dependencies of generate_recommendation_list.
    """
    with patch("api.utils.llm_rag_utils.generate_query_embedding") as mock_generate_embedding, patch("api.utils.llm_rag_utils.collection.query") as mock_query, patch(
        "api.utils.llm_rag_utils.GenerativeModel"
    ) as mock_model:
        mock_generate_embedding.return_value = [0.1, 0.2, 0.3]  # Example embedding
        mock_query.return_value = {"documents": [["Recipe A", "Recipe B", "Recipe C", "Recipe D", "Recipe E"]]}

        mock_generate_content = MagicMock()
        mock_generate_content.generate_content.return_value = MagicMock(text="Ranked Recipes: Recipe A > Recipe B")
        mock_model.return_value = mock_generate_content

        yield mock_generate_embedding, mock_query, mock_model


def test_get_recs(mock_llm_utils):
    """
    Test the /get_recs endpoint.
    """
    body = {
        "filters": {
            "ingredients": ["chicken", "onion", "garlic"],
            # Uncomment if more filters are added
            # "cookingTime": 30,
            # "servings": 4,
            # "cuisine": "Italian"
        }
    }

    response = recipes_client.post("/get_recs", json=body)
    assert response.status_code == 200
    recommendations = response.json()["recommendations"]
    assert "ranking" in recommendations
    assert "possible_recipes" in recommendations
    assert "Recipe A" in recommendations["possible_recipes"]
    assert "Recipe B" in recommendations["ranking"]

    # Verify mocks
    mock_generate_embedding, mock_query, mock_model = mock_llm_utils
    mock_generate_embedding.assert_called_once_with("I want to use chicken, onion, garlic to cook a recipe.")
    mock_query.assert_called_once()
    mock_model.return_value.generate_content.assert_called_once()
