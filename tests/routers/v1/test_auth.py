from unittest.mock import Mock, patch
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.v1.auth import router, authenticate
from app.schemas.auth import TokenSchema


client = TestClient(router)

@pytest.fixture
def mock_auth_service():
    with patch('app.routers.v1.auth.AuthService') as mock:
        yield mock

@pytest.fixture
def mock_db_session():
    return Mock(spec=AsyncSession)

@pytest.mark.asyncio
async def test_authenticate_success(mock_auth_service, mock_db_session):
    mock_service = mock_auth_service.return_value
    mock_service.authenticate.return_value = TokenSchema(access_token="test_token", token_type="bearer")
    
    form_data = {"username": "testuser", "password": "testpass"}
    response = await client.post("", data=form_data)
    
    assert response.status_code == 200
    assert response.json() == {"access_token": "test_token", "token_type": "bearer"}

@pytest.mark.asyncio
async def test_authenticate_invalid_credentials(mock_auth_service, mock_db_session):
    mock_service = mock_auth_service.return_value
    mock_service.authenticate.return_value = None
    
    form_data = {"username": "invaliduser", "password": "invalidpass"}
    response = await client.post("", data=form_data)
    
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_authenticate_user_not_found(mock_auth_service, mock_db_session):
    mock_service = mock_auth_service.return_value
    mock_service.authenticate.side_effect = ValueError("User not found")
    
    form_data = {"username": "nonexistentuser", "password": "testpass"}
    response = await client.post("", data=form_data)
    
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_authenticate_missing_credentials(mock_auth_service, mock_db_session):
    form_data = {}
    response = await client.post("", data=form_data)
    
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_authenticate_empty_credentials(mock_auth_service, mock_db_session):
    form_data = {"username": "", "password": ""}
    response = await client.post("", data=form_data)
    
    assert response.status_code == 422
