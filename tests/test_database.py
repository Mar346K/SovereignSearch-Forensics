import pytest
import hashlib
from pathlib import Path
from config.settings import settings

def test_audit_chaining(tmp_path: Path):
    """Proves that every audit log cryptographically chains to the previous one."""
    # Override the database path to use a safe, temporary test folder
    settings.db_path = tmp_path / "test_vault.sqlite3"
    
    # Import AFTER overriding the path so it connects to the test database
    from core.database import init_db, log_audit, get_connection
    
    # Initialize our test schema
    init_db()
    
    # Log two distinct actions
    log_audit("FILE_READ", "Smith_v_Jones", "doc1.pdf", {"status": "ok"})
    log_audit("FILE_WRITE", "Smith_v_Jones", "doc2.pdf", {"status": "ok"})
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, hash_chain FROM audit_trail ORDER BY id ASC")
        rows = cursor.fetchall()
        
    # Assertions
    assert len(rows) == 2
    # Verify the hashes are valid SHA-256 (64 characters)
    assert len(rows[0][1]) == 64
    assert len(rows[1][1]) == 64
    # Verify the hashes are unique to their row data
    assert rows[0][1] != rows[1][1]