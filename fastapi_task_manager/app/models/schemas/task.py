import datetime

from app.models.schemas.base import BaseScheameModel
from app.models.db.task import TaskStatus


class TaskCreate(BaseScheameModel):
    name: str
    description: str | None
    status: TaskStatus


class TaskGetDetail(BaseScheameModel):
    uuid: str


class TaskUpdate(BaseScheameModel):
    name: str | None
    description: str | None
    status: TaskStatus | None


class TaskDelete(BaseScheameModel):
    uuid: str


class TaskResponse(BaseScheameModel):
    uuid: str
    name: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime | None
