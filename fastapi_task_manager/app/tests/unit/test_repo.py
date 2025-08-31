import uuid
from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.crud.task import TaskCRUDRepository
from app.models.schemas.task import TaskCreate, TaskUpdate
from app.models.db.task import Task, TaskStatus
from app.utils.exceptions.database import EntityDoesNotExist


class TestTaskCRUDRepository:
    """Unit-тесты для репозитория задач"""

    @pytest.fixture
    def mock_session(self):
        """Фикстура мок-сессии"""
        session = AsyncMock(spec=AsyncSession)
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()
        return session

    @pytest.fixture
    def task_repo(self, mock_session):
        """Фикстура репозитория с мок-сессией"""
        return TaskCRUDRepository(async_session=mock_session)

    @pytest.mark.asyncio
    async def test_create_task(self, task_repo, mock_session):
        """Тест создания задачи"""
        task_create = TaskCreate(
            name="Test Task", description="Test Description", status=TaskStatus.CREATED
        )

        result = await task_repo.create_task(task_create)

        assert isinstance(result, Task)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_tasks(self, task_repo, mock_session):
        """Тест чтения всех задач"""
        mock_task = MagicMock()
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.scalars.return_value.all.return_value = [
            mock_task
        ]

        results = await task_repo.read_tasks()

        assert len(results) == 1
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_task_by_uuid_found(self, task_repo, mock_session):
        """Тест чтения существующей задачи"""
        task_uuid = uuid.uuid4()
        mock_task = MagicMock()
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.scalar.return_value = mock_task

        result = await task_repo.read_task_by_uuid(task_uuid)

        assert result == mock_task
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_task_by_uuid_not_found(self, task_repo, mock_session):
        """Тест чтения несуществующей задачи"""
        task_uuid = uuid.uuid4()
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.scalar.return_value = None

        with pytest.raises(EntityDoesNotExist):
            await task_repo.read_task_by_uuid(task_uuid)

    @pytest.mark.asyncio
    async def test_update_task_by_uuid(self, task_repo, mock_session):
        """Тест обновления задачи"""
        task_uuid = uuid.uuid4()
        mock_task = MagicMock()
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.scalar.return_value = mock_task

        task_update = TaskUpdate(name="Updated Name")
        result = await task_repo.update_task_by_uuid(task_uuid, task_update)

        assert result == mock_task
        mock_session.execute.assert_called()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_task_by_uuid(self, task_repo, mock_session):
        """Тест удаления задачи"""
        task_uuid = uuid.uuid4()
        mock_task = MagicMock()
        mock_session.execute.return_value = MagicMock()
        mock_session.execute.return_value.scalar.return_value = mock_task

        result = await task_repo.delete_task_by_uuid(task_uuid)

        assert "successfully deleted" in result
        mock_session.execute.assert_called()
        mock_session.commit.assert_called_once()
