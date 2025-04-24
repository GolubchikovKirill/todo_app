from fastapi import APIRouter, HTTPException, Depends
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskOut
from app.repositories.task_repo import TaskRepository

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.post("/", response_model=TaskOut)
async def create_task(task: TaskCreate, repo: TaskRepository = Depends()):
    return await repo.create(task)

@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: int, repo: TaskRepository = Depends()):
    task = await repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/", response_model=list[TaskOut])
async def get_tasks(status: str = None, repo: TaskRepository = Depends()):
    return await repo.get_all(status)

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task: TaskUpdate, repo: TaskRepository = Depends()):
    updated_task = await repo.update(task_id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
async def delete_task(task_id: int, repo: TaskRepository = Depends()):
    result = await repo.delete(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}