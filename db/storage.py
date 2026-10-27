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
    """Persist a report only when the user explicitly opts in."""
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
    """Return recent saved analyses, including original text only from opted-in rows."""
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, created_at, summary, report, original_text "
            "FROM analyses ORDER BY id DESC LIMIT 100"
        ).fetchall()
    return [dict(row) for row in rows]


def clear_history():
    with _connect() as connection:
        connection.execute("DELETE FROM analyses")


def add_custom_rule(keyword: str, label: str, explanation: str) -> bool:
    """Store a user's local keyword rule; return False when the keyword already exists."""
    keyword = keyword.strip().casefold()
    label = label.strip()
    explanation = explanation.strip()
    if not keyword or not label or not explanation:
        raise ValueError("keyword, label and explanation are required")
    try:
        with _connect() as connection:
            connection.execute(
                "INSERT INTO custom_rules(keyword, label, explanation) VALUES (?, ?, ?)",
                (keyword, label, explanation),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_custom_rules():
    """Return custom rules as tuples to keep a simple, stable interface for the UI."""
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, keyword, label, explanation FROM custom_rules ORDER BY id DESC"
        ).fetchall()
    return [tuple(row) for row in rows]


def delete_custom_rule(rule_id: int):
    with _connect() as connection:
        connection.execute("DELETE FROM custom_rules WHERE id = ?", (rule_id,))
