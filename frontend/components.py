import streamlit as st
import os
from typing import List, Dict, Any
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

from core.rag_engine import get_retriever
from utils.file_manager import process_files_generator

@st.fragment
def live_query_window(db: Chroma) -> None:
    """Renders the live intelligence query interface."""
    st.subheader("🕵️ Live Intelligence Query")
    st.caption("Interrogate partial database during sync.")
    l_query = st.text_input("Live Inquiry:", key="live_q", placeholder="Search indexed data...")
    
    if l_query:
        with st.spinner("Analyzing available vectors..."):
            retriever: VectorStoreRetriever = get_retriever(db)
            results = retriever.invoke(l_query)
            
            if results:
                for doc in results:
                    st.markdown(f"**Source:** `{os.path.basename(doc.metadata.get('source', ''))}`")
                    st.write(doc.page_content[:300] + "...")
            else:
                st.info("No matches in current index.")

@st.fragment
def run_ingestion_ui(sync_queue: List[Dict[str, Any]], db: Chroma, selected_matter: str) -> None:
    """Processes ingestion asynchronously via generator, updating the UI without blocking."""
    if not sync_queue:
        st.success("Vault is current.")
        return

    status_text = st.empty()
    p_bar = st.progress(0)
    total_files = len(sync_queue)
    
    for i, (success, name, error) in enumerate(process_files_generator(sync_queue, db, selected_matter)):
        if success:
            status_text.write(f"Indexed: `{name}`")
        else:
            st.error(f"Error indexing {name}: {error}")
        
        p_bar.progress((i + 1) / total_files)
        
    status_text.success("✅ Vault Synchronized.")