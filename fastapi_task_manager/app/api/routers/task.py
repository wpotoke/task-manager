import uuid
import fastapi
from app.repository.crud.task import TaskCRUDRepository
from app.api.dependencies.repository import get_repository
from app.models.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = fastapi.APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    name="tasks:create-task",
    response_model=TaskResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def create_task(
    task_create: TaskCreate,
    task_repo: TaskCRUDRepository = fastapi.Depends(
        get_repository(repo_type=TaskCRUDRepository)
    ),
) -> TaskResponse:
    """Создание новой задачи"""
    task = await task_repo.create_task(task_create=task_create)
    return task


@router.get(
    "/",
    name="tasks:read-tasks",
    response_model=list[TaskResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def read_tasks(
    task_repo: TaskCRUDRepository = fastapi.Depends(
        get_repository(repo_type=TaskCRUDRepository)
    ),
) -> list[TaskResponse]:
    """Получение всех задач"""
    tasks = await task_repo.read_tasks()
    return tasks


@router.get(
    "/{task_uuid}",
    name="tasks:read-task-by-uuid",
    response_model=TaskResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def read_task(
    task_uuid: uuid.UUID,
    task_repo: TaskCRUDRepository = fastapi.Depends(
        get_repository(repo_type=TaskCRUDRepository)
    ),
) -> TaskResponse:
    """Получение задачи по UUID"""
    task = await task_repo.read_task_by_uuid(uuid=task_uuid)
    return task


@router.put(
    "/{task_uuid}",
    name="tasks:update-task-by-uuid",
    response_model=TaskResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_task(
    task_uuid: uuid.UUID,
    task_update: TaskUpdate,
    task_repo: TaskCRUDRepository = fastapi.Depends(
        get_repository(repo_type=TaskCRUDRepository)
    ),
) -> TaskResponse:
    """Обновить задачу"""
    task = await task_repo.update_task_by_uuid(uuid=task_uuid, task_update=task_update)
    return task


@router.delete(
    "/{task_uuid}",
    name="tasks:delete-task-by-uuid",
    status_code=fastapi.status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_uuid: uuid.UUID,
    task_repo: TaskCRUDRepository = fastapi.Depends(
        get_repository(repo_type=TaskCRUDRepository)
    ),
) -> None:
    """Удалить задачу"""
    deletion_res = await task_repo.delete_task_by_uuid(uuid=task_uuid)
    return {"notification": deletion_res}
