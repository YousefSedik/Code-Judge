from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_read_main():
    data = {"username": "test", "password": "test"}
    response = client.post("/auth/register", data=data)
