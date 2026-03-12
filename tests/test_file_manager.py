import pytest
import hashlib
from pathlib import Path
from utils.file_manager import get_file_hash, get_safe_matter_path

def test_get_file_hash_sha256(tmp_path: Path):
    """Proves that get_file_hash uses SHA-256 and processes file streams correctly."""
    test_file = tmp_path / "evidence.txt"
    test_data = b"forensic audit trail test data for Keepsafe architecture"
    test_file.write_bytes(test_data)
    
    expected_hash = hashlib.sha256(test_data).hexdigest()
    actual_hash = get_file_hash(str(test_file))
    
    assert actual_hash == expected_hash
    assert len(actual_hash) == 64

def test_safe_matter_path_resolution(tmp_path: Path):
    """Proves that user input is strictly jailed to the target data directory."""
    base_dir = tmp_path / "data_in"
    base_dir.mkdir()
    
    # Test 1: Valid Path
    valid_matter = "Smith_v_Jones"
    expected_safe_path = (base_dir / valid_matter).resolve()
    assert get_safe_matter_path(base_dir, valid_matter) == expected_safe_path
    
    # Test 2: Malicious Path Traversal - Escape to Host OS
    with pytest.raises(ValueError, match="Path Traversal Attempt"):
        get_safe_matter_path(base_dir, "../../../Windows/System32")
        
    # Test 3: Malicious Path Traversal - Internal Escape
    with pytest.raises(ValueError, match="Path Traversal Attempt"):
        get_safe_matter_path(base_dir, "Smith_v_Jones/../../etc/passwd")