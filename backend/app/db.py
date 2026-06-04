"""
app/db.py — SQLite database for user accounts and terms agreements.
Uses aiosqlite for async access. Single file, no migrations needed.
"""
import os
import aiosqlite
from pathlib import Path

# Use /data if available (HF persistent storage), otherwise /tmp
_default_db = "/data/droidify.db" if Path("/data").exists() else "/tmp/droidify.db"
DB_PATH = Path(os.environ.get("DB_PATH", _default_db))


async def get_db() -> aiosqlite.Connection:
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db


async def init_db() -> None:
    """Create tables if they do not exist."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                github_id   INTEGER UNIQUE NOT NULL,
                login       TEXT    NOT NULL,
                name        TEXT,
                avatar_url  TEXT,
                created_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS terms_agreements (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                agreed_at   TEXT    DEFAULT (datetime('now')),
                ip          TEXT,
                user_agent  TEXT,
                UNIQUE(user_id)
            )
        """)
        await db.execute("""            CREATE TABLE IF NOT EXISTS watchlist (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                codename    TEXT    NOT NULL,
                added_at    TEXT    DEFAULT (datetime('now')),
                UNIQUE(user_id, codename)
            )
        """)
        await db.commit()


async def upsert_user(github_id: int, login: str,
                      name: str | None, avatar_url: str | None) -> int:
    """Insert or update a user. Returns the local user id."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("""
            INSERT INTO users (github_id, login, name, avatar_url)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(github_id) DO UPDATE SET
                login      = excluded.login,
                name       = excluded.name,
                avatar_url = excluded.avatar_url
        """, (github_id, login, name, avatar_url))
        await db.commit()
        cur = await db.execute(
            "SELECT id FROM users WHERE github_id = ?", (github_id,)
        )
        row = await cur.fetchone()
        return row["id"]


async def get_user_by_id(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        )
        row = await cur.fetchone()
        return dict(row) if row else None


async def record_terms_agreement(user_id: int, ip: str, ua: str) -> None:
    """Record that a user has agreed to the terms. Upserts."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO terms_agreements (user_id, ip, user_agent)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                agreed_at  = datetime('now'),
                ip         = excluded.ip,
                user_agent = excluded.user_agent
        """, (user_id, ip, ua))
        await db.commit()


async def has_agreed_terms(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT 1 FROM terms_agreements WHERE user_id = ?", (user_id,)
        )
        return await cur.fetchone() is not None


async def add_to_watchlist(user_id: int, codename: str) -> bool:
    """Add a device to user's watchlist. Returns False if already exists."""
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute(
                "INSERT INTO watchlist (user_id, codename) VALUES (?, ?)",
                (user_id, codename)
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def remove_from_watchlist(user_id: int, codename: str) -> bool:
    """Remove a device from user's watchlist. Returns False if not found."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM watchlist WHERE user_id = ? AND codename = ?",
            (user_id, codename)
        )
        await db.commit()
        return cur.rowcount > 0


async def get_watchlist(user_id: int) -> list[str]:
    """Get all codenames in user's watchlist, newest first."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT codename FROM watchlist WHERE user_id = ? ORDER BY added_at DESC",
            (user_id,)
        )
        rows = await cur.fetchall()
        return [row[0] for row in rows]


async def is_in_watchlist(user_id: int, codename: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT 1 FROM watchlist WHERE user_id = ? AND codename = ?",
            (user_id, codename)
        )
        return await cur.fetchone() is not None
