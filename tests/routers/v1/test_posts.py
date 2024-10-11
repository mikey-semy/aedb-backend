import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.routers.v1.posts import router, get_post, get_posts
from app.schemas.posts import PostSchema
from app.schemas.auth import UserSchema

client = TestClient(router)

@pytest.fixture
def mock_post_service():
    with patch('app.routers.v1.posts.PostService') as mock:
        yield mock

@pytest.fixture
def mock_current_user():
    return UserSchema(id=1, username="testuser")

def test_get_post(mock_post_service, mock_current_user):
    mock_service = mock_post_service.return_value
    mock_service.get_post.return_value = PostSchema(id=1, title="Test Post", content="Test Content")
    
    response = client.get("/1", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Post", "content": "Test Content"}

def test_get_post_not_found(mock_post_service, mock_current_user):
    mock_service = mock_post_service.return_value
    mock_service.get_post.side_effect = ValueError("Post not found")
    
    response = client.get("/999", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 404

def test_get_posts(mock_post_service, mock_current_user):
    mock_service = mock_post_service.return_value
    mock_service.get_posts.return_value = [
        PostSchema(id=1, title="Post 1", content="Content 1"),
        PostSchema(id=2, title="Post 2", content="Content 2")
    ]
    
    response = client.get("/", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0] == {"id": 1, "title": "Post 1", "content": "Content 1"}
    assert response.json()[1] == {"id": 2, "title": "Post 2", "content": "Content 2"}

def test_get_posts_empty(mock_post_service, mock_current_user):
    mock_service = mock_post_service.return_value
    mock_service.get_posts.return_value = []
    
    response = client.get("/", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json() == []

def test_get_post_unauthorized():
    response = client.get("/1")
    assert response.status_code == 401

def test_get_posts_unauthorized():
    response = client.get("/")
    assert response.status_code == 401
