from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from asyncpg import Connection

from schemas.task_schema import TaskCreate, TaskUpdate, TaskOut
from repositories.task_repo import TaskRepository
from database.database import connect_to_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])

FAKE_USER_ID = 1


@router.post("/", response_model=int)
async def create_task(
    task: TaskCreate,
    conn: Connection = Depends(connect_to_db),
):
    repo = TaskRepository(conn)
    task_id = await repo.create_task(FAKE_USER_ID, task)
    return task_id


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: int,
    conn: Connection = Depends(connect_to_db),
):
    repo = TaskRepository(conn)
    task = await repo.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=List[TaskOut])
async def list_tasks(
    due_before: Optional[datetime] = Query(None),
    is_completed: Optional[bool] = Query(None),
    conn: Connection = Depends(connect_to_db),
):
    repo = TaskRepository(conn)
    tasks = await repo.get_tasks(FAKE_USER_ID, due_before, is_completed)
    return tasks


@router.put("/{task_id}", response_model=bool)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    conn: Connection = Depends(connect_to_db),
):
    repo = TaskRepository(conn)
    updated = await repo.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found or nothing to update")
    return True


@router.delete("/{task_id}", response_model=bool)
async def delete_task(
    task_id: int,
    conn: Connection = Depends(connect_to_db),
):
    repo = TaskRepository(conn)
    deleted = await repo.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return True