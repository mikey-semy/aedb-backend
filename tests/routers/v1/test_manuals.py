import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.routers.v1.manuals import router
from app.schemas.manuals import ManualSchema, GroupSchema, CategorySchema

client = TestClient(router)

@pytest.fixture
def mock_manual_service():
    with patch('app.routers.v1.manuals.ManualService') as mock:
        yield mock

def test_get_nested_manuals(mock_manual_service):
    mock_service = mock_manual_service.return_value
    mock_service.get_nested_manuals.return_value = [{"id": 1, "name": "Test Manual"}]
    
    response = client.get("/nested")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Manual"}]

def test_search_manuals(mock_manual_service):
    mock_service = mock_manual_service.return_value
    mock_service.search_manuals.return_value = [ManualSchema(id=1, name="Test Manual")]
    
    response = client.get("/search_manuals?q=test")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Manual"}]

def test_put_manual(mock_manual_service):
    mock_service = mock_manual_service.return_value
    mock_service.update_manual.return_value = ManualSchema(id=1, name="Updated Manual")
    
    response = client.put("/manual/1", json={"id": 1, "name": "Updated Manual"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Manual"}

def test_delete_manual(mock_manual_service):
    mock_service = mock_manual_service.return_value
    mock_service.delete_manual.return_value = True
    
    response = client.delete("/manual/1")
    assert response.status_code == 200
    assert response.json() == True

def test_post_group(mock_manual_service):
    mock_service = mock_manual_service.return_value
    mock_service.add_group.return_value = GroupSchema(id=1, name="New Group")
    
    response = client.post("/group", json={"name": "New Group"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "New Group"}

def test_upload_manual(mock_manual_service):
    mock_service = mock_manual_service.return_value
    mock_service.upload_file.return_value = {"filename": "test.pdf", "status": "success"}
    
    response = client.post("/upload_manual", files={"manual": ("test.pdf", b"file content")})
    assert response.status_code == 200
    assert response.json() == {"filename": "test.pdf", "status": "success"}

def test_add_all_groups(mock_manual_service):
    mock_service = mock_manual_service.return_value
    mock_service.add_all_groups.return_value = None
    
    response = client.post("/add_groups")
    assert response.status_code == 200
    assert response.json() is None

def test_search_categories_min_length(mock_manual_service):
    response = client.get("/search_categories?q=ab")
    assert response.status_code == 422  # Validation error for min_length

def test_delete_manuals(mock_manual_service):
    mock_service = mock_manual_service.return_value
    mock_service.delete_manuals.return_value = True
    
    response = client.delete("/")
    assert response.status_code == 200
    assert response.json() == True
