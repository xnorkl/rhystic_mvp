import httpx
import pytest

BASE_URL = "http://localhost:8000/v1"

@pytest.mark.asyncio
async def test_register_user():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/auth/register",
            json={
                "username": "testuser",
                "password": "password123"
            }
        )
        assert response.status_code == 201

@pytest.mark.asyncio
async def test_login():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/auth/token",
            data={
                "username": "testuser",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        assert "access_token" in response.json() 