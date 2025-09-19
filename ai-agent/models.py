# models.py (use absolute path for todos.db)
import sqlite3
import os
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, "todos.db")

def init_db() -> None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            status INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()

init_db()

def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "done", "completed")
    return False

def get_next_task_id() -> int:
    """Get the next available task ID"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(id), 0) FROM tasks")
    max_id = cursor.fetchone()[0]
    conn.close()
    return max_id + 1

def get_all_tasks() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, status FROM tasks ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    tasks: List[Dict[str, Any]] = []
    for r in rows:
        try:
            tasks.append({
                "id": int(r[0]),
                "name": r[1] or "",
                "description": r[2] or "",
                "status": _to_bool(r[3]),
            })
        except Exception:
            continue
    return tasks

def add_task(id: int, name: str, description: str, status: bool) -> str:
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (id, name, description, status) VALUES (?, ?, ?, ?)",
            (int(id), name, description, 1 if status else 0),
        )
        conn.commit()
        return f"Task {id} added."
    except sqlite3.IntegrityError as ie:
        raise ValueError(f"Task id {id} already exists") from ie
    finally:
        conn.close()

def update_task(id: int, name: str, description: str, status: bool) -> str:
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM tasks WHERE id=?", (int(id),))
        if not cursor.fetchone():
            raise ValueError(f"Task {id} not found")
        cursor.execute(
            "UPDATE tasks SET name=?, description=?, status=? WHERE id=?",
            (name, description, 1 if status else 0, int(id)),
        )
        conn.commit()
        return f"Task {id} updated."
    finally:
        conn.close()

def delete_task(id: int) -> str:
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM tasks WHERE id=?", (int(id),))
        if not cursor.fetchone():
            raise ValueError(f"Task {id} not found")
        cursor.execute("DELETE FROM tasks WHERE id=?", (int(id),))
        conn.commit()
        return f"Task {id} deleted."
    finally:
        conn.close()
