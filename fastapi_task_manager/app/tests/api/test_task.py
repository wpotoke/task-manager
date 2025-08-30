import pytest


@pytest.mark.asyncio
async def test_get_tasks(async_client):
    """Test getting all tasks"""
    response = await async_client.get("api/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_task(async_client):
    """Test task creation"""
    task_data = {"name": "Test", "description": "Test task", "status": "created"}
    response = await async_client.post("api/tasks/", json=task_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test"
