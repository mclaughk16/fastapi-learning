import pytest
from fastapi.testclient import TestClient
import jwt

from app import models
from app.config import settings

def test_root(client: TestClient):
    response = client.get("/")
    assert response.json().get('message') == 'Welcome to the API'
    assert response.status_code == 200

def test_create_user(client: TestClient):
    response = client.post("/users", json = {
        "email": "jim@gmail.com",
        "password": "password"
    })
    user = models.UserPublic(**response.json())
    assert user.email == "jim@gmail.com"
    assert response.status_code == 201

def test_login_user(client: TestClient, test_user):
    response = client.post("/login", data={
        "username": test_user['email'],
        "password": test_user['password']
    })
    login_response = models.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == 'bearer'
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password", 403),
    ("jim@gmail.com", "wrongPassword", 403),
    ("wrongemail@gmail.com", "wrongPassword", 403),
    (None, "password", 403),
    ("jim@gmail.com", None, 403)

])
def test_incorrect_login(client: TestClient, test_user, email, password, status_code):
    response = client.post("/login", data={
        "username": email,
        "password": password
    })
    print(response.status_code)
    assert response.status_code == status_code
