import sqlite3
import json
import hashlib
from datetime import datetime
from typing import Dict, Any

from config.settings import settings

def get_connection() -> sqlite3.Connection:
    """Returns a thread-safe SQLite connection with WAL enabled."""
    conn = sqlite3.connect(settings.db_path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;") 
    return conn

def init_db() -> None:
    """Initializes the database schemas for the file registry and forensic audit trails."""
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS file_registry (
                hash TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                matter TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        
        # UPGRADE: Added hash_chain column for tamper-evidence
        conn.execute('''
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matter TEXT NOT NULL,
                file TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL,
                hash_chain TEXT NOT NULL
            )
        ''')

def load_registry() -> Dict[str, Dict[str, str]]:
    """Loads the file registry into memory for fast O(1) hash lookups."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hash, name, matter, timestamp FROM file_registry")
        return {
            row[0]: {"name": row[1], "matter": row[2], "timestamp": row[3]} 
            for row in cursor.fetchall()
        }

def register_file(file_hash: str, name: str, matter: str) -> None:
    """Commits a newly embedded file to the SQLite registry."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO file_registry (hash, name, matter, timestamp) VALUES (?, ?, ?, ?)",
            (file_hash, name, matter, datetime.now().isoformat())
        )

def log_audit(action: str, matter: str, file: str, details: Any) -> None:
    """Safely logs system actions with a cryptographic chain to prove immutability."""
    details_str = json.dumps(details) if isinstance(details, (dict, list)) else str(details)
    timestamp = datetime.now().isoformat()
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Fetch the previous row's hash (or use a genesis string if empty)
        cursor.execute("SELECT hash_chain FROM audit_trail ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        prev_hash = row[0] if row else "0" * 64
        
        # 2. Compute the new cryptographic hash using the previous hash as the salt
        payload = f"{prev_hash}{matter}{file}{action}{details_str}{timestamp}"
        current_hash = hashlib.sha256(payload.encode()).hexdigest()
        
        # 3. Commit the chained record
        conn.execute(
            "INSERT INTO audit_trail (matter, file, action, details, timestamp, hash_chain) VALUES (?, ?, ?, ?, ?, ?)",
            (matter, file, action, details_str, timestamp, current_hash)
        )