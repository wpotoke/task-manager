import datetime
import uuid
from app.models.schemas.base import BaseScheameModel
from app.models.db.task import TaskStatus


class TaskCreate(BaseScheameModel):
    name: str
    description: str | None
    status: TaskStatus


class TaskGetDetail(BaseScheameModel):
    uuid: uuid.UUID


class TaskUpdate(BaseScheameModel):
    name: str | None
    description: str | None
    status: TaskStatus | None


class TaskDelete(BaseScheameModel):
    uuid: uuid.UUID


class TaskResponse(BaseScheameModel):
    uuid: uuid.UUID
    name: str
    description: str | None
    status: TaskStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
