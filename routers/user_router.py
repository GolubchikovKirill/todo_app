from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Connection

from schemas.user_schema import UserCreate, UserOut
from repositories.user_repo import UserRepository
from database.database import connect_to_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=int)
async def create_user(
    user: UserCreate,
    conn: Connection = Depends(connect_to_db),
):
    repo = UserRepository(conn)
    existing = await repo.get_user_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    user_id = await repo.create_user(user)
    return user_id

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    conn: Connection = Depends(connect_to_db),
):
    repo = UserRepository(conn)
    user = await repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user