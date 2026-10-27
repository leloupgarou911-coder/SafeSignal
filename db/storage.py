import json
import sqlite3

from core.config import DB_PATH
from .models import SCHEMA


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with _connect() as connection:
        connection.executescript(SCHEMA)


def save_analysis(report: dict, original_text: str, consent: bool = False):
    if not consent:
        return False
    summary = ", ".join(item["title"] for item in report["findings"]) or "No pattern detected"
    with _connect() as connection:
        connection.execute(
            "INSERT INTO analyses(summary, report, original_text) VALUES (?, ?, ?)",
            (summary, json.dumps(report, ensure_ascii=False), original_text),
        )
    return True


def list_history():
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, created_at, summary, report FROM analyses ORDER BY id DESC LIMIT 100"
        ).fetchall()
    return [dict(row) for row in rows]


def clear_history():
    with _connect() as connection:
        connection.execute("DELETE FROM analyses")
