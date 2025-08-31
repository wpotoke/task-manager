import pytest
from app.models.db.task import Task, TaskStatus


class TestTaskModel:
    """Unit-тесты для модели Task"""

    def test_task_creation(self):
        """Тест создания задачи с валидными данными"""
        task = Task(
            name="Test Task", description="Test Description", status=TaskStatus.CREATED
        )

        assert task.name == "Test Task"
        assert task.description == "Test Description"
        assert task.status == TaskStatus.CREATED
        assert task.updated_at is None

    def test_task_default_values(self):
        """Тест значений по умолчанию"""
        task = Task(name="Test Task", status=TaskStatus.CREATED)

        assert task.description is None

    @pytest.mark.parametrize(
        "status", [TaskStatus.CREATED, TaskStatus.WORK, TaskStatus.DONE]
    )
    def test_task_status_values(self, status):
        """Тест всех возможных статусов"""
        task = Task(name="Test Task", status=status)
        assert task.status == status

    def test_task_equality(self):
        """Тест сравнения задач"""
        task1 = Task(name="Task 1", status=TaskStatus.CREATED)
        task2 = Task(name="Task 2", status=TaskStatus.CREATED)

        assert task1 != task2
