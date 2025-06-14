import asyncpg
import os
import urllib.parse

# Разбор DATABASE_URL вручную
DATABASE_URL = os.environ["DATABASE_URL"]
parsed = urllib.parse.urlparse(DATABASE_URL)

DB_CONFIG = {
    "user": parsed.username,
    "password": parsed.password,
    "database": parsed.path[1:],  # убрать /
    "host": parsed.hostname,
    "port": parsed.port or 5432,
    "ssl": "require",  # 🔥 ВАЖНО для Supabase!
}

async def insert_interaction(from_user, to_user, command: str):
    if not to_user:
        return

    conn = await asyncpg.connect(**DB_CONFIG)
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
    conn = await asyncpg.connect(**DB_CONFIG)
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
