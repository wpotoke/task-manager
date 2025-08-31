import uuid
from datetime import datetime
import pytest
from pydantic import ValidationError
from app.models.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.db.task import TaskStatus


class TestTaskSchemas:
    """Unit-тесты для Pydantic схем задач"""

    def test_task_create_valid(self):
        """Тест валидного создания задачи"""
        task_data = {
            "name": "Test Task",
            "description": "Test Description",
            "status": TaskStatus.CREATED,
        }

        task = TaskCreate(**task_data)
        assert task.name == "Test Task"
        assert task.description == "Test Description"
        assert task.status == TaskStatus.CREATED

    def test_task_create_minimal(self):
        """Тест создания с минимальными данными"""
        task_data = {"name": "Test Task", "status": TaskStatus.CREATED}

        task = TaskCreate(**task_data)
        assert task.name == "Test Task"
        assert task.description is None
        assert task.status == TaskStatus.CREATED

    def test_task_create_invalid_name(self):
        """Тест невалидного имени"""
        with pytest.raises(ValidationError):
            TaskCreate(name="", status=TaskStatus.CREATED)

    def test_task_create_missing_required(self):
        """Тест отсутствия обязательных полей"""
        with pytest.raises(ValidationError):
            TaskCreate(status=TaskStatus.CREATED)  # Нет name

        with pytest.raises(ValidationError):
            TaskCreate(name="Test Task")  # Нет status

    def test_task_update_partial(self):
        """Тест частичного обновления"""
        update_data = {"name": "Updated Name"}
        task_update = TaskUpdate(**update_data)

        assert task_update.name == "Updated Name"
        assert task_update.description is None
        assert task_update.status is None

    def test_task_update_empty(self):
        """Тест пустого обновления"""
        task_update = TaskUpdate()
        assert task_update.name is None
        assert task_update.description is None
        assert task_update.status is None

    def test_task_response_from_orm(self):
        """Тест создания response из ORM модели"""
        task_uuid = uuid.uuid4()
        created_at = datetime.now()

        task_data = {
            "uuid": task_uuid,
            "name": "Test Task",
            "description": "Test Description",
            "status": TaskStatus.CREATED,
            "created_at": created_at,
            "updated_at": None,
        }

        response = TaskResponse(**task_data)
        assert response.uuid == task_uuid
        assert response.name == "Test Task"
        assert response.description == "Test Description"
        assert response.status == TaskStatus.CREATED
        assert response.created_at == created_at
        assert response.updated_at is None
