# pylint:disable=redefined-outer-name
import uuid
from datetime import datetime
import pytest


@pytest.fixture
def test_task_create_data():
    """Фикстура с тестовыми данными задачи"""
    return {
        "name": "create taskname",
        "description": "description1",
        "status": "created",
    }


@pytest.fixture
def test_task_update_data():
    """Фикстура с тестовыми данными задачи"""
    return {
        "name": "update taskname",
        "description": "updated description",
        "status": "in_work",
    }


@pytest.fixture
def test_task_minimal_data():
    """Фикстура с минимальными данными задачи"""
    return {
        "name": "minimal task",
        "status": "created",
    }


@pytest.fixture
def test_task_invalid_data():
    """Фикстура с невалидными данными"""
    return {
        "name": "",
        "description": "desc",
        "status": "invalid_status",
    }


async def create_test_task(async_client, task_data=None):
    """Вспомогательная функция для создания тестовой задачи"""
    if task_data is None:
        task_data = test_task_create_data()
    response = await async_client.post("api/tasks/", json=task_data)
    return response


@pytest.mark.asyncio
async def test_get_tasks_empty(async_client):
    """Тест на получение пустого списка задач"""
    response = await async_client.get("api/tasks/")
    assert response.status_code == 200
    assert response.json() == []
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_tasks_with_data(async_client, test_task_create_data):
    """Тест на получение списка задач с данными"""
    # Создаем задачу
    create_response = await create_test_task(async_client, test_task_create_data)
    assert create_response.status_code == 201

    # Получаем список
    response = await async_client.get("api/tasks/")
    assert response.status_code == 200
    tasks = response.json()

    assert isinstance(tasks, list)
    assert len(tasks) >= 1
    assert "uuid" in tasks[0]
    assert "name" in tasks[0]
    assert "status" in tasks[0]
    assert "createdAt" in tasks[0]


@pytest.mark.asyncio
async def test_create_task_success(async_client, test_task_create_data):
    """Тест на успешное создание задачи"""
    response = await create_test_task(async_client, test_task_create_data)

    assert response.status_code == 201
    data = response.json()

    assert "uuid" in data
    assert "name" in data
    assert "description" in data
    assert "status" in data
    assert "createdAt" in data

    assert data["name"] == "create taskname"
    assert data["description"] == "description1"
    assert data["status"] == "created"

    try:
        uuid.UUID(data["uuid"])
        assert True
    except ValueError:
        assert False, "Invalid UUID format"

    try:
        datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))
        assert True
    except ValueError:
        assert False, "Invalid datetime format"


@pytest.mark.asyncio
async def test_create_task_minimal_data(async_client, test_task_minimal_data):
    """Тест на создание задачи с минимальными данными"""
    response = await create_test_task(async_client, test_task_minimal_data)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "minimal task"
    assert data["status"] == "created"
    assert data["description"] is None or data["description"] == ""


@pytest.mark.asyncio
async def test_create_task_invalid_data(async_client, test_task_invalid_data):
    """Тест на создание задачи с невалидными данными"""
    response = await create_test_task(async_client, test_task_invalid_data)

    assert response.status_code == 422
    error_data = response.json()
    assert "detail" in error_data


@pytest.mark.asyncio
async def test_create_task_missing_required_fields(async_client):
    """Тест на создание задачи без обязательных полей"""
    # Без name
    response = await async_client.post(
        "api/tasks/", json={"description": "test", "status": "created"}
    )
    assert response.status_code == 422

    # Без status
    response = await async_client.post(
        "api/tasks/", json={"name": "test", "description": "test"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_task_by_id_success(async_client, test_task_create_data):
    """Тест на успешное получение задачи по UUID"""
    create_response = await create_test_task(async_client, test_task_create_data)
    assert create_response.status_code == 201

    task_uuid = create_response.json()["uuid"]
    response = await async_client.get(f"api/tasks/{task_uuid}")

    assert response.status_code == 200
    data = response.json()

    assert data["uuid"] == task_uuid
    assert data["name"] == "create taskname"
    assert data["description"] == "description1"
    assert data["status"] == "created"


@pytest.mark.asyncio
async def test_get_task_by_id_not_found(async_client):
    """Тест на получение несуществующей задачи"""

    random_uuid = "00000000-0000-0000-0000-000000000000"
    response = await async_client.get(f"api/tasks/{random_uuid}")

    assert response.status_code == 404
    assert "detail" in response.json()
    assert "does not exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_task_success(
    async_client, test_task_create_data, test_task_update_data
):
    """Тест на успешное обновление задачи"""
    create_response = await create_test_task(async_client, test_task_create_data)
    assert create_response.status_code == 201

    task_uuid = create_response.json()["uuid"]
    original_created_at = create_response.json()["createdAt"]

    response = await async_client.put(
        f"api/tasks/{task_uuid}", json=test_task_update_data
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "update taskname"
    assert data["description"] == "updated description"
    assert data["status"] == "in_work"

    assert data["uuid"] == task_uuid

    assert data["createdAt"] == original_created_at


@pytest.mark.asyncio
async def test_update_task_partial_data(async_client, test_task_create_data):
    """Тест на частичное обновление задачи"""
    create_response = await create_test_task(async_client, test_task_create_data)
    assert create_response.status_code == 201

    task_uuid = create_response.json()["uuid"]

    response = await async_client.put(
        f"api/tasks/{task_uuid}", json={"name": "partial update"}
    )

    print(response.json())

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "partial update"
    assert data["description"] == "description1"
    assert data["status"] == "created"


@pytest.mark.asyncio
async def test_update_task_not_found(async_client, test_task_update_data):
    """Тест на обновление несуществующей задачи"""
    random_uuid = "00000000-0000-0000-0000-000000000000"
    response = await async_client.put(
        f"api/tasks/{random_uuid}", json=test_task_update_data
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_invalid_data(
    async_client, test_task_create_data, test_task_invalid_data
):
    """Тест на обновление задачи с невалидными данными"""
    create_response = await create_test_task(async_client, test_task_create_data)
    assert create_response.status_code == 201

    task_uuid = create_response.json()["uuid"]
    response = await async_client.put(
        f"api/tasks/{task_uuid}", json=test_task_invalid_data
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_task_success(async_client, test_task_create_data):
    """Тест на успешное удаление задачи"""
    create_response = await create_test_task(async_client, test_task_create_data)
    assert create_response.status_code == 201

    task_uuid = create_response.json()["uuid"]

    response = await async_client.delete(f"api/tasks/{task_uuid}")
    assert response.status_code == 204

    response = await async_client.get(f"api/tasks/{task_uuid}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_found(async_client):
    """Тест на удаление несуществующей задачи"""
    random_uuid = "00000000-0000-0000-0000-000000000000"
    response = await async_client.delete(f"api/tasks/{random_uuid}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_task_status_validation(async_client):
    """Тест валидации статусов задачи"""
    valid_statuses = ["created", "in_work", "done"]

    for status in valid_statuses:
        response = await async_client.post(
            "api/tasks/", json={"name": f"test {status}", "status": status}
        )
        assert response.status_code == 201, f"Failed for status: {status}"
        assert response.json()["status"] == status


@pytest.mark.asyncio
async def test_task_status_invalid(async_client):
    """Тест на невалидный статус задачи"""
    response = await async_client.post(
        "api/tasks/", json={"name": "test invalid status", "status": "invalid_status"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_task_name_validation(async_client):
    """Тест валидации имени задачи"""
    # Слишком длинное имя
    long_name = "a" * 256
    response = await async_client.post(
        "api/tasks/", json={"name": long_name, "status": "created"}
    )
    assert response.status_code == 422

    # Пустое имя
    response = await async_client.post(
        "api/tasks/", json={"name": "", "status": "created"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_task_description_validation(async_client):
    """Тест валидации описания задачи"""
    long_description = "a" * 1001
    response = await async_client.post(
        "api/tasks/",
        json={
            "name": "test long description",
            "description": long_description,
            "status": "created",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_task_created_at_immutable(async_client, test_task_create_data):
    """Тест, что createdAt нельзя изменить при обновлении"""
    create_response = await create_test_task(async_client, test_task_create_data)
    assert create_response.status_code == 201

    task_uuid = create_response.json()["uuid"]
    original_created_at = create_response.json()["createdAt"]

    response = await async_client.put(
        f"api/tasks/{task_uuid}",
        json={"name": "try change created_at", "createdAt": "2023-01-01T00:00:00Z"},
    )

    assert response.status_code == 200
    assert response.json()["createdAt"] == original_created_at


@pytest.mark.asyncio
async def test_task_uuid_immutable(async_client, test_task_create_data):
    """Тест, что UUID нельзя изменить при обновлении"""
    create_response = await create_test_task(async_client, test_task_create_data)
    assert create_response.status_code == 201

    task_uuid = create_response.json()["uuid"]

    response = await async_client.put(
        f"api/tasks/{task_uuid}",
        json={
            "name": "try change uuid",
            "uuid": "00000000-0000-0000-0000-000000000000",
        },
    )

    assert response.status_code == 200
    assert response.json()["uuid"] == task_uuid


@pytest.mark.asyncio
async def test_task_content_type(async_client, test_task_create_data):
    """Тест правильности Content-Type в ответах"""
    response = await create_test_task(async_client, test_task_create_data)
    assert response.status_code == 201
    assert response.headers["content-type"] == "application/json"

    response = await async_client.get("api/tasks/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


@pytest.mark.asyncio
async def test_task_method_not_allowed(async_client):
    """Тест на неразрешенные HTTP методы"""
    # PATCH на коллекцию
    response = await async_client.patch("api/tasks/", json={})
    assert response.status_code == 405

    # PATCH на конкретную задачу
    response = await async_client.patch(
        "api/tasks/00000000-0000-0000-0000-000000000000", json={}
    )
    assert response.status_code == 405

    # POST на конкретную задачу
    response = await async_client.post(
        "api/tasks/00000000-0000-0000-0000-000000000000", json={}
    )
    assert response.status_code == 405


@pytest.mark.asyncio
async def test_task_large_payload(async_client):
    """Тест на очень большой payload"""
    large_name = "a" * 10000  # Очень длинное имя
    response = await async_client.post(
        "api/tasks/", json={"name": large_name, "status": "created"}
    )
    # Ожидаем ошибку валидации или размера payload
    assert response.status_code in [413, 422, 400]


@pytest.mark.asyncio
async def test_task_malformed_json(async_client):
    """Тест на невалидный JSON"""
    response = await async_client.post(
        "api/tasks/",
        content="{invalid json}",
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_task_wrong_content_type(async_client):
    """Тест на неправильный Content-Type"""
    response = await async_client.post(
        "api/tasks/",
        content="name=test&status=created",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 422
