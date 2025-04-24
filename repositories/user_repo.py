from asyncpg import Connection
from typing import Optional
from schemas.user_schema import UserCreate

class UserRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def create_user(self, user: UserCreate) -> int:
        query = """
        INSERT INTO users (username, email)
        VALUES ($1, $2)
        RETURNING id;
        """
        row = await self.conn.fetchrow(query, user.username, user.email)
        return row["id"]

    async def get_user(self, user_id: int) -> Optional[dict]:
        query = "SELECT * FROM users WHERE id = $1;"
        row = await self.conn.fetchrow(query, user_id)
        return dict(row) if row else None

    async def get_user_by_username(self, username: str) -> Optional[dict]:
        query = "SELECT * FROM users WHERE username = $1;"
        row = await self.conn.fetchrow(query, username)
        return dict(row) if row else None