import os
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    # if our router doesn't have it under v1, check root health
    if response.status_code == 404:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}

def test_chat_validation_error():
    # Send an empty JSON POST body to /api/chat
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422 # Unprocessable Entity
    
if __name__ == "__main__":
    print("Running basic tests...")
    test_health_check()
    test_chat_validation_error()
    print("All standard schema tests passed!")
