import sqlite3
import json
from datetime import datetime

DB_PATH = "vector_db/vault_metadata.sqlite3"

def get_connection():
    """Returns a thread-safe SQLite connection with WAL enabled."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    """Initializes the database schemas for registry and auditing."""
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS file_registry (
                            hash TEXT PRIMARY KEY,
                            name TEXT,
                            matter TEXT,
                            timestamp TEXT)''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS audit_trail (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            matter TEXT,
                            file TEXT,
                            action TEXT,
                            details TEXT,
                            timestamp TEXT)''')

def load_registry():
    """Returns the file registry as a dictionary for fast hash lookups."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hash, name, matter, timestamp FROM file_registry")
        return {row[0]: {"name": row[1], "matter": row[2], "timestamp": row[3]} for row in cursor.fetchall()}

def register_file(file_hash, name, matter):
    """Commits a newly embedded file to the registry."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO file_registry (hash, name, matter, timestamp) VALUES (?, ?, ?, ?)",
            (file_hash, name, matter, str(datetime.now()))
        )

def log_audit(action, matter, file, details):
    """Safely logs system actions to the audit trail."""
    details_str = json.dumps(details) if isinstance(details, dict) else str(details)
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO audit_trail (matter, file, action, details, timestamp) VALUES (?, ?, ?, ?, ?)",
            (matter, file, action, details_str, str(datetime.now()))
        )