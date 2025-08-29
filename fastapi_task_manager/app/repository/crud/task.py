# pylint: disable=redefined-outer-name
import typing
import uuid
import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from app.models.db.task import Task
from app.models.schemas.task import (
    TaskCreate,
    TaskUpdate,
)
from app.repository.crud.base import BaseCRUDRepository
from app.utils.exceptions.database import EntityDoesNotExist


class TaskCRUDRepository(BaseCRUDRepository):
    async def create_task(self, task_create: TaskCreate) -> Task:
        new_task = Task(
            name=task_create.name,
            description=task_create.description,
            status=task_create.status,
        )
        self.async_session.add(instance=new_task)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_task)

        return new_task

    async def read_tasks(self) -> typing.Sequence[Task]:
        stmt = sqlalchemy.select(Task)
        query = await self.async_session.execute(statement=stmt)

        return query.scalars().all()

    async def read_task_by_uuid(self, uuid: uuid.UUID) -> Task:
        stmt = sqlalchemy.select(Task).where(Task.uuid == uuid)
        query = await self.async_session.execute(statement=stmt)
        task = query.scalar()

        if not task:
            raise EntityDoesNotExist(f"Task with uuid - {uuid} does not exists")

        return query.scalar()

    async def update_task_by_uuid(
        self, uuid: uuid.UUID, task_update: TaskUpdate
    ) -> Task:
        select_stmt = sqlalchemy.select(Task).where(Task.uuid == uuid)
        query = await self.async_session.execute(statement=select_stmt)
        update_task = query.scalar()
        if not update_task:
            raise EntityDoesNotExist(f"Task with uuid - {uuid} does not exists")

        update_data = task_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = sqlalchemy_functions.now()

        update_stmt = (
            sqlalchemy.update(Task)
            .where(Task.uuid == update_task.uuid)
            .values(**update_data)
        )

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_task)

        return update_task

    async def delete_task_by_uuid(self, uuid: uuid.UUID):
        select_stmt = sqlalchemy.select(Task).where(Task.uuid == uuid)
        query = await self.async_session.execute(statement=select_stmt)
        deleted_task = query.scalar()

        if not deleted_task:
            raise EntityDoesNotExist(f"Task with uuid - {uuid} does not exists")

        stmt = sqlalchemy.delete(table=Task).where(Task.uuid == deleted_task.uuid)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"Task with uuid '{uuid}' is successfully deleted"
