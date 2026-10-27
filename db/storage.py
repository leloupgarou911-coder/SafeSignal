import json,sqlite3
from pathlib import Path
from .models import SCHEMA
DB_PATH=Path(__file__).resolve().parent/"safesignal.sqlite3"
def _connect():
 c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_db():
 with _connect() as c: c.executescript(SCHEMA)
def save_analysis(report:dict,original_text:str,consent:bool=False):
 if not consent: return False
 summary=", ".join(x["title"] for x in report["findings"]) or "No pattern detected"
 with _connect() as c: c.execute("INSERT INTO analyses(summary,report,original_text) VALUES(?,?,?)",(summary,json.dumps(report,ensure_ascii=False),original_text))
 return True
def list_history():
 with _connect() as c: rows=c.execute("SELECT id,created_at,summary,report FROM analyses ORDER BY id DESC LIMIT 100").fetchall()
 return [dict(r) for r in rows]
def clear_history():
 with _connect() as c: c.execute("DELETE FROM analyses")
