from fastapi import FastAPI
from app.routers import routers
from app.database.database import get_db, init_db
from typing import AsyncGenerator


async def lifespan(_: FastAPI) -> AsyncGenerator:
    pool = await get_db().__anext__()

    await init_db(pool)
    print("Database initialized on startup")

    yield
    await pool.close()
    print("Database connection closed")

app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)