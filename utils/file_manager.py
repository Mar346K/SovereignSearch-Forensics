import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Generator, Tuple, Optional
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader
from langchain_chroma import Chroma

from config.settings import settings
from core.database import load_registry, register_file, log_audit
from core.ingestion import chunk_and_embed

def get_file_hash(filepath: str) -> str:
    """Generates a SHA-256 hash for a file to track indexing status and ensure forensic integrity."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        # 64KB chunks for memory-efficient streaming
        for chunk in iter(lambda: f.read(65536), b""): 
            hasher.update(chunk)
    return hasher.hexdigest()

def get_matters() -> List[str]:
    """Scans the data directory and returns a list of available matters (folders)."""
    matters = ["Unassigned (Root)"]
    if not os.path.exists(settings.data_dir): 
        return matters
        
    for client in os.listdir(settings.data_dir):
        c_path = os.path.join(settings.data_dir, client)
        if os.path.isdir(c_path):
            subfolders = [f for f in os.listdir(c_path) if os.path.isdir(os.path.join(c_path, f))]
            for m in subfolders: 
                matters.append(f"{client} / {m}")
    return matters

def build_sync_queue(selected_matter: str, focus_file: str) -> List[Dict[str, Any]]:
    """Builds a prioritized queue of unindexed files, sorted by size for optimal processing."""
    registry = load_registry()
    sync_queue: List[Dict[str, Any]] = []
    
    m_path = os.path.join(settings.data_dir, selected_matter.replace(" / ", "/"))
    target_dir = m_path if "Unassigned" not in selected_matter else str(settings.data_dir)
    
    for root, _, files in os.walk(target_dir):
        for f in files:
            if f.lower().endswith(('.pdf', '.docx')):
                f_full = os.path.join(root, f)
                if get_file_hash(f_full) not in registry:
                    sync_queue.append({"path": f_full, "size": os.path.getsize(f_full), "name": f})
                    
    if sync_queue:
        # Sort by size to handle smaller files first, keeping the UI highly responsive
        sync_queue.sort(key=lambda x: x['size'])
        if focus_file != "None":
            focus_data = next((i for i in sync_queue if i["name"] == focus_file), None)
            if focus_data: 
                sync_queue.insert(0, sync_queue.pop(sync_queue.index(focus_data)))
            
    return sync_queue

def process_files_generator(
    sync_queue: List[Dict[str, Any]], 
    db: Chroma, 
    selected_matter: str
) -> Generator[Tuple[bool, str, Optional[str]], None, None]:
    """
    Generator that processes files and yields status updates back to the UI thread.
    Prevents Streamlit from blocking during heavy I/O and OpenVINO/SYSMAN embedding tasks.
    """
    for item in sync_queue:
        try:
            loader = PyMuPDFLoader(item['path']) if item['path'].endswith(".pdf") else Docx2txtLoader(item['path'])
            docs = loader.load()
            
            if docs:
                chunk_and_embed(db, docs, selected_matter)
                
            file_hash = get_file_hash(item['path'])
            register_file(file_hash, item['name'], selected_matter)
            log_audit("SYNC_SUCCESS", selected_matter, item['name'], f"Size: {item['size']}b")
            
            yield True, item['name'], None
        except Exception as e:
            yield False, item['name'], str(e)

def get_safe_matter_path(base_dir: Path | str, user_input: str) -> Path:
    """
    Resolves and jails user-provided matter paths to prevent directory traversal.
    """
    base_path = Path(base_dir).resolve()
    sanitized_input = user_input.replace(" / ", "/")
    
    # .resolve() evaluates symlinks and '..' components to their absolute real path
    target_path = (base_path / sanitized_input).resolve()
    
    # Strict boundary check: If the target isn't inside the base_dir, it's an attack.
    if not target_path.is_relative_to(base_path):
        raise ValueError(f"SECURITY ALERT: Path Traversal Attempt Detected. Target: {target_path}")
    
    return target_path