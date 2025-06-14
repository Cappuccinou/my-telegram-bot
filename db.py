import asyncpg
import os
import urllib.parse

DATABASE_URL = os.environ["DATABASE_URL"]

async def get_connection():
    # Используем DATABASE_URL напрямую без ручного разбора
    return await asyncpg.connect(
        dsn=DATABASE_URL,
        ssl="require"
    )

async def insert_interaction(from_user, to_user, command: str):
    if not to_user:
        return

    conn = await get_connection()
    try:
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
    finally:
        await conn.close()

async def get_user_stats(user_id: int):
    conn = await get_connection()
    try:
        rows = await conn.fetch(
            """
            SELECT command, COUNT(*) as count
            FROM interactions
            WHERE to_id = $1
            GROUP BY command
            ORDER BY count DESC
            """,
            user_id
        )
        return rows
    finally:
        await conn.close()
