import asyncpg
import os
import urllib.parse
import socket

DATABASE_URL = os.environ["DATABASE_URL"]
parsed = urllib.parse.urlparse(DATABASE_URL)

async def get_connection():
    host = socket.gethostbyname(parsed.hostname)  # DNS lookup внутри функции
    return await asyncpg.connect(
        host=host,
        port=parsed.port or 5432,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path.lstrip("/"),
        ssl="require",
        family=socket.AF_INET
    )

async def insert_interaction(from_user, to_user, command: str):
    if not to_user:
        return

    conn = await get_connection()
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

async def get_user_stats(user_id: int):
    conn = await get_connection()
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
    await conn.close()
    return rows
