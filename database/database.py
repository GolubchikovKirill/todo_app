from pathlib import Path
import asyncpg
from settings import settings


async def connect_to_db() -> asyncpg.Pool:
    return await asyncpg.create_pool(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        min_size=1,
        max_size=10,
    )

async def close_db(db_pool: asyncpg.Pool):
    await db_pool.close()

async def init_db(db_pool: asyncpg.Pool):
    sql_path = Path(__file__).parent / "sql" / "init.sql"
    sql = sql_path.read_text()
    async with db_pool.acquire() as conn:
        await conn.execute(sql)