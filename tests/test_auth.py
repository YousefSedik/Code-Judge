import pytest

@pytest.mark.asyncio
async def test_authentication(async_client, async_session):
    # Sign up
    json = {
        "email": "user@example.com",
        "username": "string",
        "password1": "string",
        "password2": "string",
        "first_name": "string",
        "last_name": "string",
    }
    response = await async_client.post("/register", json=json)
    data = response.json()
    assert response.status_code == 201
    assert data == {"created": True}

    # Login
    data = {"username": "string", "password": "string"}
    response = await async_client.post("/token", data=data)
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data

