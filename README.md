# ⚖️ SovereignSearch-Forensics

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black.svg)

**SovereignSearch-Forensics** is a privacy-first, local AI Retrieval-Augmented Generation (RAG) engine designed for offline document intelligence and forensic assembly. It ensures zero telemetry and absolute data sovereignty by running large language models entirely on local hardware.

---

## 🚀 Key Features

* **100% Air-Gapped Intelligence:** No API keys, no cloud data leaks. Built on top of local `Ollama` models (`llama3.1`, `nomic-embed-text`).
* **Hardware Empathy & Optimization:** Pre-configured for high-capacity system memory and 16GB VRAM accelerators (e.g., Intel Arc A770) leveraging OpenVINO/SYSMAN telemetry.
* **Asynchronous Ingestion Pipeline:** Non-blocking document chunking and embedding, allowing the UI to remain responsive during massive file imports.
* **Forensic Assembly Mode:** Built-in OCR pipeline (Tesseract) for manual bounding-box extraction and correction of corrupted or scanned PDF evidence.
* **Immutable Audit Trail:** SQLite-backed logging with Write-Ahead Logging (WAL) enabled to track every document modification and AI interaction.

## 🧠 System Architecture


The application adheres to a strict Separation of Concerns:
1. **Frontend (`frontend/`):** Streamlit-powered UI utilizing cached resource states to prevent VRAM reloading.
2. **Core AI Engine (`core/`):** LangChain orchestration, ChromaDB vector storage, and optimized text-splitting pipelines.
3. **Utilities (`utils/`):** Hashing, OCR sanitization, and asynchronous file queues.
4. **Configuration (`config/`):** Pydantic-validated, centralized environment and hardware settings.

---

## ⚙️ Quickstart (Docker Recommended)

The easiest way to run the Vault without managing local Python environments or Tesseract binaries is via Docker. Ensure Docker Desktop and [Ollama](https://ollama.com) are installed on your host machine.

1. **Pull Required Local Models (Host Machine):**
   ```bash
   ollama pull llama3.1
   ollama pull nomic-embed-text
    ```

2. **Boot the Container::**
    ```bash
    docker-compose up --build -d
    ```

3. **Access the Hub:**
    Open your browser and navigate to "http://localhost:8501"
    Note: Your data_in/ and vector_db/ folders are volume-mounted. All ingested documents and vector embeddings will persist on your host machine across container restarts.

🛠️ Bare Metal Setup (Windows)
If you prefer to run the engine directly on your hardware:

1. **Install Python 3.11+ and Tesseract OCR for Windows. Add Tesseract to your System PATH.**

2. **Clone the repository and run the setup script:**

    ```bash
    scripts\Setup_Environment.bat
    ```

3. **Launch the engine:**
    ```bash
    scripts\01_START_VAULT.bat
    ```

