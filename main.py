from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.database import connect_to_db, close_db
from routers import routers

@asynccontextmanager
async def lifespan(_: FastAPI):
    app.state.db = await connect_to_db()
    yield
    await close_db(app.state.db)

app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)


