import datetime
import enum
import uuid
import sqlalchemy
from sqlalchemy.orm import (
    Mapped as SQLAlchemyMapped,
    mapped_column as sqlalchemy_mapped_column,
)
from sqlalchemy.sql import functions as sqlalchemy_functions

from app.repository.table import Base


class TaskStatus(enum.Enum):
    CREATED = "created"
    WORK = "in_work"
    DONE = "done"


class Task(Base):
    __tablename__ = "task"

    uuid: SQLAlchemyMapped[uuid] = sqlalchemy_mapped_column(
        sqlalchemy.UUID,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        primary_key=True,
    )
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=255), nullable=False
    )
    description: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String, nullable=True
    )
    status: SQLAlchemyMapped[TaskStatus] = sqlalchemy_mapped_column(
        sqlalchemy.Enum(TaskStatus), default=TaskStatus.CREATED, nullable=False
    )
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now(),
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
