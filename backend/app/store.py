import json
import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parents[1] / "signalstack.db"


def connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize() -> None:
    with connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS profiles (
          id TEXT PRIMARY KEY, github_username TEXT, skills TEXT NOT NULL,
          projects TEXT NOT NULL, topics TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS documents (
          id TEXT PRIMARY KEY, title TEXT NOT NULL, source TEXT NOT NULL,
          source_type TEXT NOT NULL, kind TEXT NOT NULL, url TEXT NOT NULL,
          tags TEXT NOT NULL, content TEXT NOT NULL, action TEXT NOT NULL,
          published_at TEXT, ingested_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)


def upsert_profile(profile_id: str, profile: dict) -> dict:
    with connection() as conn:
        conn.execute("""INSERT INTO profiles(id, github_username, skills, projects, topics)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET github_username=excluded.github_username, skills=excluded.skills,
        projects=excluded.projects, topics=excluded.topics""", (
            profile_id, profile.get("github_username"), json.dumps(profile.get("skills", [])),
            json.dumps(profile.get("projects", [])), json.dumps(profile.get("topics", [])),
        ))
    return get_profile(profile_id)


def get_profile(profile_id: str) -> dict | None:
    with connection() as conn:
        row = conn.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    if not row:
        return None
    return {"id": row["id"], "github_username": row["github_username"], "skills": json.loads(row["skills"]), "projects": json.loads(row["projects"]), "topics": json.loads(row["topics"])}


def upsert_documents(documents: list[dict]) -> int:
    with connection() as conn:
        for doc in documents:
            conn.execute("""INSERT INTO documents(id,title,source,source_type,kind,url,tags,content,action,published_at)
            VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET title=excluded.title, content=excluded.content,
            tags=excluded.tags, published_at=excluded.published_at, ingested_at=CURRENT_TIMESTAMP""", (
                doc["id"], doc["title"], doc["source"], doc["source_type"], doc["kind"], doc["url"],
                json.dumps(doc.get("tags", [])), doc["content"], doc["action"], doc.get("published_at"),
            ))
    return len(documents)


def get_documents() -> list[dict]:
    with connection() as conn:
        rows = conn.execute("SELECT * FROM documents ORDER BY ingested_at DESC").fetchall()
    return [{**dict(row), "tags": json.loads(row["tags"])} for row in rows]
