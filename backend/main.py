from __future__ import annotations

import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from models import ErrorResponse, Task, TaskCreate, TaskUpdate


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


DB_PATH = os.getenv("TASKS_DB_PATH", os.path.join(os.path.dirname(__file__), "tasks.db"))


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    with closing(get_conn()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL,
                category TEXT NOT NULL,
                important INTEGER NOT NULL,
                completed INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );
            """.strip()
        )
        conn.commit()


def row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id=int(row["id"]),
        title=str(row["title"]),
        description=str(row["description"]),
        priority=str(row["priority"]),
        category=str(row["category"]),
        important=bool(row["important"]),
        completed=bool(row["completed"]),
        created_at=datetime.fromisoformat(str(row["created_at"])),
    )


app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    with closing(get_conn()) as conn:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        return [row_to_task(r) for r in rows]


@app.get("/api/tasks/{task_id}", response_model=Task, responses={404: {"model": ErrorResponse}})
def get_task(task_id: int) -> Task:
    with closing(get_conn()) as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return row_to_task(row)


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    created_at = utc_now().isoformat()
    with closing(get_conn()) as conn:
        cur = conn.execute(
            """
            INSERT INTO tasks (title, description, priority, category, important, completed, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """.strip(),
            (
                payload.title,
                payload.description,
                payload.priority,
                payload.category,
                int(payload.important),
                int(payload.completed),
                created_at,
            ),
        )
        conn.commit()
        task_id = int(cur.lastrowid)

        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return row_to_task(row)


@app.put(
    "/api/tasks/{task_id}",
    response_model=Task,
    responses={404: {"model": ErrorResponse}},
)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    with closing(get_conn()) as conn:
        existing = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Task not found")

        conn.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, priority = ?, category = ?, important = ?, completed = ?
            WHERE id = ?
            """.strip(),
            (
                payload.title,
                payload.description,
                payload.priority,
                payload.category,
                int(payload.important),
                int(payload.completed),
                task_id,
            ),
        )
        conn.commit()

        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return row_to_task(row)


@app.delete(
    "/api/tasks/{task_id}",
    status_code=204,
    response_class=Response,
    responses={404: {"model": ErrorResponse}},
)
def delete_task(task_id: int) -> Response:
    with closing(get_conn()) as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return Response(status_code=204)
