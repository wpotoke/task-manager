import datetime
import uuid
from typing import Optional
from pydantic import Field, field_validator
from app.models.schemas.base import BaseScheameModel
from app.models.db.task import TaskStatus


class TaskCreate(BaseScheameModel):
    name: str = Field(min_length=5, max_length=255)
    description: str | None = Field(None, max_length=1000)
    status: TaskStatus

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return value.strip()


class TaskGetDetail(BaseScheameModel):
    uuid: uuid.UUID


class TaskUpdate(BaseScheameModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return value.strip() if value else None


class TaskDelete(BaseScheameModel):
    uuid: uuid.UUID


class TaskResponse(BaseScheameModel):
    uuid: uuid.UUID
    name: str
    description: str | None
    status: TaskStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
