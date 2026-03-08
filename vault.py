import streamlit as st
import os
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
from streamlit_drawable_canvas import st_canvas

# Extracted Modular Logic
from src.database import init_db, log_audit
from src.rag_engine import init_system, get_retriever
from src.file_manager import get_matters, build_sync_queue, process_files_generator

# --- 1. SYSTEM CONFIG & PATHS ---
st.set_page_config(page_title="Sovereign Search: Legal Workspace", layout="wide", page_icon="⚖️")
DATA_DIR = "data_in"
DB_DIR = "vector_db"

for d in [DATA_DIR, DB_DIR]:
    os.makedirs(d, exist_ok=True)

init_db()

# --- 2. INITIALIZE ENGINE ---
db, llm = init_system()

# --- 3. LIVE QUERY FRAGMENT ---
@st.fragment
def live_query_window():
    st.subheader("🕵️ Live Intelligence Query")
    st.caption("Interrogate partial database during sync.")
    l_query = st.text_input("Live Inquiry:", key="live_q", placeholder="Search indexed data...")
    
    if l_query:
        with st.spinner("Analyzing available vectors..."):
            retriever = get_retriever(db, k=3)
            results = retriever.invoke(l_query)
            if results:
                for doc in results:
                    st.markdown(f"**Source:** `{os.path.basename(doc.metadata.get('source', ''))}`")
                    st.write(doc.page_content[:300] + "...")
            else:
                st.info("No matches in current index.")

# --- 4. ASYNC INGESTION FRAGMENT ---
@st.fragment
def run_ingestion_ui(sync_queue, db, selected_matter):
    """Processes ingestion asynchronously via generator, preventing UI blocking."""
    if not sync_queue:
        st.success("Vault is current.")
        return

    status_text = st.empty()
    p_bar = st.progress(0)
    total_files = len(sync_queue)
    
    # Iterate over the generator mapped in file_manager.py
    for i, (success, name, error) in enumerate(process_files_generator(sync_queue, db, selected_matter)):
        if success:
            status_text.write(f"Indexed: `{name}`")
        else:
            st.error(f"Error indexing {name}: {error}")
        
        p_bar.progress((i + 1) / total_files)
        
    status_text.success("✅ Vault Synchronized.")

# --- 5. SIDEBAR: CONTROL CENTER ---
with st.sidebar:
    st.title("⚖️ Workspace")
    matters = get_matters()
    selected_matter = st.selectbox("Current Matter:", matters)

    m_path = os.path.join(DATA_DIR, selected_matter.replace(" / ", "/"))
    all_pdfs = [f for f in os.listdir(m_path) if f.lower().endswith('.pdf')] if os.path.exists(m_path) else []
    focus_file = st.selectbox("🎯 Focus Scan:", ["None"] + all_pdfs)

    st.divider()
    mode = st.radio("Switch View:", ["Discovery Hub", "Forensic Assembly"])

# --- 6. MAIN UI ROUTES ---
if mode == "Discovery Hub":
    st.title("📂 Sovereign Discovery Hub")

    with st.expander("🔄 Vault Synchronization", expanded=True):
        if st.button("⚡ Start Priority Sync", type="primary"):
            sync_queue = build_sync_queue(selected_matter, focus_file)
            run_ingestion_ui(sync_queue, db, selected_matter)

    st.divider()
    live_query_window()

# --- 7. FORENSIC ASSEMBLY ---
else:
    st.title("🧩 Forensic Assembly & Audit")
    if "Unassigned" in selected_matter:
        st.warning("Select a Matter to use Forensic Assembly.")
    else:
        if all_pdfs:
            doc_name = st.selectbox("Select Evidence:", all_pdfs)
            doc_path = os.path.join(m_path, doc_name)
            pdf = fitz.open(doc_path)
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
                    crop = img.crop((obj["left"], obj["top"], obj["left"] + obj["width"], obj["top"] + obj["height"]))
                    st.image(crop, width=300)
                    text = st.text_area(f"Verify Extract {i}:", value=pytesseract.image_to_string(crop))
                    if st.button(f"Commit Block {i}"):
                        log_audit("FORENSIC_FIX", selected_matter, doc_name, {"extract": text[:50]})
                        st.success("Logged to Audit Trail.")