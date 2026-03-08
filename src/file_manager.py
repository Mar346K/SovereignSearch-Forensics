import os
import hashlib
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader
from src.database import load_registry, register_file, log_audit
from src.rag_engine import chunk_and_embed

DATA_DIR = "data_in"

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192): 
            hasher.update(chunk)
    return hasher.hexdigest()

def get_matters():
    matters = ["Unassigned (Root)"]
    if not os.path.exists(DATA_DIR): return matters
    for client in os.listdir(DATA_DIR):
        c_path = os.path.join(DATA_DIR, client)
        if os.path.isdir(c_path):
            subfolders = [f for f in os.listdir(c_path) if os.path.isdir(os.path.join(c_path, f))]
            for m in subfolders: matters.append(f"{client} / {m}")
    return matters

def build_sync_queue(selected_matter, focus_file):
    """Builds a prioritized queue of unindexed files."""
    registry = load_registry()
    sync_queue = []
    m_path = os.path.join(DATA_DIR, selected_matter.replace(" / ", "/"))
    target_dir = m_path if "Unassigned" not in selected_matter else DATA_DIR
    
    for root, _, files in os.walk(target_dir):
        for f in files:
            if f.lower().endswith(('.pdf', '.docx')):
                f_full = os.path.join(root, f)
                if get_file_hash(f_full) not in registry:
                    sync_queue.append({"path": f_full, "size": os.path.getsize(f_full), "name": f})
                    
    if sync_queue:
        sync_queue.sort(key=lambda x: x['size'])
        if focus_file != "None":
            focus_data = next((i for i in sync_queue if i["name"] == focus_file), None)
            if focus_data: sync_queue.insert(0, sync_queue.pop(sync_queue.index(focus_data)))
            
    return sync_queue

def process_files_generator(sync_queue, db, selected_matter):
    """Generator that yields status updates back to the UI thread."""
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