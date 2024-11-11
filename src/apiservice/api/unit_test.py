import pytest
from fastapi.testclient import TestClient
from service import app  # Replace with the actual file name where your app is defined

client = TestClient(app)

def test_register():
    response = client.post("/register", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"message": "User testuser registered successfully"}

    # Test registering the same user again
    response = client.post("/register", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_login():
    client.post("/register", data={"username": "testuser2", "password": "testpass2"})
    response = client.post("/login", data={"username": "testuser2", "password": "testpass2"})
    assert response.status_code == 200
    assert response.json() == {"message": "User testuser2 logged in successfully"}

    # Test invalid credentials
    response = client.post("/login", data={"username": "testuser2", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_logout():
    response = client.post("/logout", data={"username": "testuser2"})
    assert response.status_code == 200
    assert response.json() == {"message": "User testuser2 logged out successfully"}

def test_update_pantry():
    response = client.post("/update_pantry", json={"add": {"apples": 5, "bananas": 3}})
    assert response.status_code == 200
    assert response.json() == {"message": "Pantry updated", "pantry": {"apples": 5, "bananas": 3}}

    response = client.post("/update_pantry", json={"subtract": {"apples": 2}})
    assert response.status_code == 200
    assert response.json() == {"message": "Pantry updated", "pantry": {"apples": 3, "bananas": 3}}

    # Test subtracting more than available
    response = client.post("/update_pantry", json={"subtract": {"apples": 5}})
    assert response.status_code == 400
    assert response.json() == {"detail": "Not enough apples in pantry"}

def test_get_recs():
    filters = {"diet": "vegetarian"}
    response = client.post("/get_recs", json={"filters": filters, "more_recommendations": False})
    assert response.status_code == 200
    assert "recommendations" in response.json()

    # Test with more recommendations
    response = client.post("/get_recs", json={"filters": filters, "more_recommendations": True})
    assert response.status_code == 200
    assert "recommendations" in response.json()
    assert len(response.json()["recommendations"]) >= 5

def test_chat_gemini(monkeypatch):
    def mock_generate_text(prompt):
        class MockResponse:
            text = "Mocked response from Gemini"
        return MockResponse()

    monkeypatch.setattr("google.generativeai.GenerativeModel.generate_text", mock_generate_text)
    response = client.post("/chat_gemini", data={"message": "Hello"})
    assert response.status_code == 200
    assert response.json()["response"] == "Mocked response from Gemini"
    assert "chat_history" in response.json()

def test_get_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Preppal"}
