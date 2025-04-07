from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_welcome():
    response = client.get("/api/v1/welcome")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome Engineer!"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
