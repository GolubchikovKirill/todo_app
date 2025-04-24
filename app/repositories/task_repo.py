import asyncpg
from fastapi import Depends
from app.database.database import get_db
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskOut
from typing import Optional, List

class TaskRepository:
    def __init__(self, db: asyncpg.Pool = Depends(get_db)):
        self.db = db

    async def create(self, task: TaskCreate) -> TaskOut:
        query = """
            INSERT INTO tasks (title, description, deadline, status)
            VALUES ($1, $2, $3, $4)
            RETURNING id, title, description, deadline, status;
        """
        result = await self.db.fetchrow(query, task.title, task.description, task.deadline, task.status)
        return TaskOut(**result)

    async def get(self, task_id: int) -> Optional[TaskOut]:
        query = "SELECT * FROM tasks WHERE id = $1"
        result = await self.db.fetchrow(query, task_id)
        return TaskOut(**result) if result else None

    async def get_all(self, status: Optional[str] = None) -> List[TaskOut]:
        if status:
            query = "SELECT * FROM tasks WHERE status = $1"
            result = await self.db.fetch(query, status)
        else:
            query = "SELECT * FROM tasks"
            result = await self.db.fetch(query)

        return [TaskOut(**task) for task in result]

    async def update(self, task_id: int, task: TaskUpdate) -> Optional[TaskOut]:
        query = """
            UPDATE tasks
            SET title = $1, description = $2, deadline = $3, status = $4
            WHERE id = $5
            RETURNING id, title, description, deadline, status;
        """
        result = await self.db.fetchrow(query, task.title, task.description, task.deadline, task.status, task_id)
        return TaskOut(**result) if result else None

    async def delete(self, task_id: int) -> bool:
        query = "DELETE FROM tasks WHERE id = $1"
        result = await self.db.execute(query, task_id)
        return result == "DELETE 1"