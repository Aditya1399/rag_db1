#Necessary imports
import pytest
from fastapi.testclient import TestClient
from main import app
from models import User
from database import SessionLocal

# Initialize the Test Client
client = TestClient(app)


@pytest.fixture(scope="module")
def create_test_user():
    db = SessionLocal()
    test_username = "test_user"
    test_password = "test_password"

    # Clean up any existing test user
    db.query(User).filter(User.username == test_username).delete()
    db.commit()

    # Create a new test user
    hashed_password = User.hash_password(test_password)
    new_user = User(username=test_username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.close()

    return {"username": test_username, "password": test_password}


# Test successful token generation

def test_token_generation(create_test_user):
    response = client.post(
        "/token",
        data={"username": create_test_user["username"], "password": create_test_user["password"]},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# Test invalid credentials

def test_invalid_credentials():
    response = client.post(
        "/token",
        data={"username": "wrong_user", "password": "wrong_password"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


# Test protected /ingest endpoint

def test_ingest_document(create_test_user):
    login_response = client.post(
        "/token",
        data={"username": create_test_user["username"], "password": create_test_user["password"]},
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/ingest",  json={"title": "Test Doc", "content": "Test content."},
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    


# Test protected /qa endpoint

def test_qa_with_existing_doc(create_test_user):
    login_response = client.post(
        "/token",
        data={"username": create_test_user["username"], "password": create_test_user["password"]},
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/qa", json={"question": "What is test content?", "top_k": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    


# Test protected /documents endpoint

def test_list_documents(create_test_user):
    login_response = client.post(
        "/token",
        data={"username": create_test_user["username"], "password": create_test_user["password"]},
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/documents",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    


# Test access without token

def test_access_without_token():
    response = client.get("/documents")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
