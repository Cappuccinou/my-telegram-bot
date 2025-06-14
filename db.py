import asyncpg
import os

DB_URL = os.environ["DATABASE_URL"]  # переменная окружения с твоей PostgreSQL ссылкой

async def insert_interaction(from_user, to_user, command: str):
    if not to_user:
        return

    conn = await asyncpg.connect(DB_URL)
    await conn.execute(
        """
        INSERT INTO interactions (from_id, from_name, to_id, to_name, command)
        VALUES ($1, $2, $3, $4, $5)
        """,
        from_user.id,
        from_user.first_name,
        to_user.id,
        to_user.first_name,
        command
    )
    await conn.close()
