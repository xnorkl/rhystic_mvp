import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rhystic.api.database import Base
from rhystic.api.models import user

BASE_URL = "http://localhost:8000/v1"

# Test database URL
TEST_DB_URL = "sqlite:///./test.db"

# Create test database
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Test database setup
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Test user registration
# TODO: Add tests for invalid email format
# TODO: Add tests for duplicate username
# TODO: Add tests for duplicate email
# TODO: Add tests for weak password
# TODO: Add tests for token expiration
# TODO: Add tests for token refresh
# TODO: Add tests for token validation

@pytest.mark.asyncio
async def test_register_user():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/auth/register",
            json={
                "username": "testuser",
                "password": "password123",
                "email": "test@example.com"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["username"] == "testuser"

@pytest.mark.asyncio
async def test_login():
    # First register a user
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BASE_URL}/auth/register",
            json={
                "username": "testuser2",
                "password": "password1234",
                "email": "test2@example.com"
            }
        )
        
        # Then try to login
        response = await client.post(
            f"{BASE_URL}/auth/token",
            data={
                "username": "testuser2",
                "password": "password1234"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer" 