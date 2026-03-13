import streamlit as st
import os
from pathlib import Path
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
from streamlit_drawable_canvas import st_canvas
from langchain_chroma import Chroma

from frontend.components import live_query_window, run_ingestion_ui
from utils.file_manager import build_sync_queue
from core.database import log_audit

def render_discovery_hub(db: Chroma, selected_matter: str, focus_file: str) -> None:
    st.title("📂 Sovereign Discovery Hub")

    with st.expander("🔄 Vault Synchronization", expanded=True):
        if st.button("⚡ Start Priority Sync", type="primary"):
            sync_queue = build_sync_queue(selected_matter, focus_file)
            run_ingestion_ui(sync_queue, db, selected_matter)

    st.divider()
    live_query_window(db)

def render_forensic_assembly(selected_matter: str, all_pdfs: list[str], m_path: str) -> None:
    st.title("🧩 Forensic Assembly & Audit")
    
    if "Unassigned" in selected_matter:
        st.warning("Select a Matter to use Forensic Assembly.")
        return
        
    if not all_pdfs:
        st.info("No PDF evidence available in this matter.")
        return

    doc_name = st.selectbox("Select Evidence:", all_pdfs)
    
    # UPGRADE: Secure path resolution wired into forensic assembly
    doc_path = str((Path(m_path) / doc_name).resolve())
    
    try:
        pdf = fitz.open(doc_path)
    except Exception as e:
        st.error(f"Could not open document: {e}")
        return

    pg_num = st.number_input("Page:", 0, len(pdf) - 1, 0)
    pix = pdf[pg_num].get_pixmap(matrix=fitz.Matrix(2, 2))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    st.info("Manual Extraction & Order Correction")
    
    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 0, 0.2)", 
        background_image=img, 
        drawing_mode="rect",
        key="assem_canvas"
    )

    if canvas_result.json_data and canvas_result.json_data["objects"]:
        for i, obj in enumerate(canvas_result.json_data["objects"]):
            left, top = obj["left"], obj["top"]
            width, height = obj["width"], obj["height"]
            
            crop = img.crop((left, top, left + width, top + height))
            st.image(crop, width=300)
            
            extracted_text = pytesseract.image_to_string(crop)
            text = st.text_area(f"Verify Extract {i}:", value=extracted_text, key=f"text_{i}")
            
            if st.button(f"Commit Block {i}", key=f"commit_{i}"):
                log_audit("FORENSIC_FIX", selected_matter, doc_name, {"extract": text[:50]})
                st.success("Logged to Audit Trail.")