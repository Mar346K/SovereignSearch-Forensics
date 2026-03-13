import streamlit as st
import os
from pathlib import Path

# 1. Initialize environment and configs before importing heavy AI modules
from config.settings import settings
settings.initialize_environment()

from core.database import init_db
from core.rag_engine import init_system
from utils.file_manager import get_matters, get_safe_matter_path
from frontend.views import render_discovery_hub, render_forensic_assembly

# 2. PAGE CONFIGURATION
st.set_page_config(
    page_title="Sovereign Search: Legal Workspace", 
    layout="wide", 
    page_icon="⚖️"
)

# 3. CACHED SYSTEM STARTUP
@st.cache_resource
def startup_system():
    init_db()
    db, llm = init_system()
    return db, llm

db, llm = startup_system()

# 4. SIDEBAR: CONTROL CENTER
with st.sidebar:
    st.title("⚖️ Workspace")
    
    matters = get_matters()
    selected_matter = st.selectbox("Current Matter:", matters)

    # UPGRADE: Secure path resolution wired into the UI
    if "Unassigned" in selected_matter:
        m_path = str(settings.data_dir)
    else:
        m_path = str(get_safe_matter_path(settings.data_dir, selected_matter))

    all_pdfs = [f for f in os.listdir(m_path) if f.lower().endswith('.pdf')] if os.path.exists(m_path) else []
    
    focus_file = st.selectbox("🎯 Focus Scan:", ["None"] + all_pdfs)

    st.divider()
    mode = st.radio("Switch View:", ["Discovery Hub", "Forensic Assembly"])

# 5. MAIN UI ROUTING
if mode == "Discovery Hub":
    render_discovery_hub(db, selected_matter, focus_file)
elif mode == "Forensic Assembly":
    render_forensic_assembly(selected_matter, all_pdfs, m_path)