from typing import List, Optional
from datetime import datetime
from asyncpg import Connection
from schemas.task_schema import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def create_task(self, user_id: int, task: TaskCreate) -> int:
        query = """
        INSERT INTO tasks (title, description, due_date, user_id)
        VALUES ($1, $2, $3, $4)
        RETURNING id;
        """
        row = await self.conn.fetchrow(query, task.title, task.description, task.due_date, user_id)
        return row["id"]

    async def get_task(self, task_id: int) -> Optional[dict]:
        query = "SELECT * FROM tasks WHERE id = $1;"
        row = await self.conn.fetchrow(query, task_id)
        return dict(row) if row else None

    async def get_tasks(
        self,
        user_id: int,
        due_before: Optional[datetime] = None,
        is_completed: Optional[bool] = None
    ) -> List[dict]:
        base_query = "SELECT * FROM tasks WHERE user_id = $1"
        args = [user_id]
        if due_before is not None:
            base_query += " AND due_date <= $2"
            args.append(due_before)
        if is_completed is not None:
            idx = len(args) + 1
            base_query += f" AND is_completed = ${idx}"
            args.append(is_completed)

        rows = await self.conn.fetch(base_query, *args)
        return [dict(row) for row in rows]

    async def update_task(self, task_id: int, task: TaskUpdate) -> bool:
        fields = []
        values = []
        idx = 1

        for field, value in task.model_dump(exclude_unset=True).items():
            fields.append(f"{field} = ${idx}")
            values.append(value)
            idx += 1

        if not fields:
            return False

        query = f"""
        UPDATE tasks SET {', '.join(fields)} WHERE id = ${idx}
        """
        values.append(task_id)

        result = await self.conn.execute(query, *values)
        return result == "UPDATE 1"

    async def delete_task(self, task_id: int) -> bool:
        query = "DELETE FROM tasks WHERE id = $1"
        result = await self.conn.execute(query, task_id)
        return result == "DELETE 1"