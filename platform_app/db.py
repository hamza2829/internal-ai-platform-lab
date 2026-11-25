import json
import os
import sqlite3
from pathlib import Path


def connect():
    path = Path(os.getenv("AI_DB_PATH", "platform.sqlite3"))
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
        CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, item_id TEXT, input_hash TEXT, output TEXT, flags TEXT, status TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, rating INTEGER CHECK(rating BETWEEN 1 AND 5), comment TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT, run_id TEXT, details TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
    """)
    return db


def audit(db, event: str, run_id: str, details: dict):
    db.execute("INSERT INTO audit(event, run_id, details) VALUES (?, ?, ?)", (event, run_id, json.dumps(details, sort_keys=True)))
