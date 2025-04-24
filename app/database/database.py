import asyncpg
from typing import AsyncGenerator
from app.settings import DB_URL

async def get_db() -> AsyncGenerator[asyncpg.Pool, None]:
    database_url = DB_URL
    pool = await asyncpg.create_pool(database_url)
    try:
        yield pool
    finally:
        await pool.close()

async def init_db(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                deadline TIMESTAMPTZ NOT NULL,
                status VARCHAR(50) NOT NULL
            );
        """)