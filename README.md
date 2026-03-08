# ⚖️ SovereignSearch-Forensics

**A 100% Local, Air-Gapped Retrieval-Augmented Generation (RAG) Engine for Legal and Forensic Document Analysis.**

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black.svg)
![ChromaDB](https://img.shields.io/badge/Chroma-Vector_DB-orange.svg)

## 📌 Executive Summary
**SovereignSearch-Forensics** is a flagship AI systems engineering project demonstrating how to build a highly capable, completely offline RAG architecture. Designed for sensitive data environments (legal discovery, forensic audits, proprietary research), it guarantees zero data exfiltration by running all embedding and generation processes on local hardware. 

The system has been meticulously engineered for concurrency, modularity, and smooth user experience during heavy local compute workloads.

## ✨ Core Architecture & Features

* **Asynchronous, Non-Blocking Ingestion:** Utilizes a custom Python generator pattern paired with Streamlit `@st.fragment` decorators. This allows massive PDF/DOCX libraries to be embedded in the background without freezing the primary UI thread.
* **Thread-Safe Concurrency:** Migrated from flat JSON files to a robust SQLite database implementing Write-Ahead Logging (`PRAGMA journal_mode=WAL;`). This ensures zero database locking or race conditions during simultaneous read/write operations (e.g., querying the index while a background sync logs to the audit trail).
* **Decoupled, Modular Backend:** The application cleanly separates the Streamlit presentation layer from the LangChain/ChromaDB RAG engine and the OS-level file management, adhering to enterprise design patterns.
* **Human-in-the-Loop OCR Fallback:** Features a "Forensic Assembly" module using `streamlit-drawable-canvas` and Tesseract OCR, allowing users to manually bound, extract, and verify text from corrupted or scanned-image PDFs that standard loaders fail to parse.

## 🛠️ Technology Stack

* **Frontend/UI:** Streamlit
* **Orchestration:** LangChain
* **Vector Store:** ChromaDB
* **Local LLM Provider:** Ollama (Llama 3.1 8B for generation, Nomic-Embed-Text for embeddings)
* **Database (State & Auditing):** SQLite3 (WAL Mode)
* **Document Parsers:** PyMuPDF (fitz), Docx2txt, PyTesseract

## 💻 Target Hardware Profile
The engine is hardware-accelerated and designed to take advantage of high-VRAM local setups. The primary development and optimization environment features:
* **GPU:** Intel Arc A770 (16GB VRAM) - Configured with `ZES_ENABLE_SYSMAN=1`
* **RAM:** 128 GB 
* **CPU:** Intel Core i7 (9th Gen)
* *Note: Fallback CPU mode is supported but significantly impacts embedding speeds.*

## 🚀 Quickstart & Installation

**1. Prerequisites**
* [Python 3.10+](https://www.python.org/downloads/)
* [Ollama](https://ollama.com/)
* [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (Add to System PATH for Forensic Assembly mode)

**2. Setup Environment**
Run the initialization script to create the isolated virtual environment, install dependencies, and pull the required AI models to your local machine.
```cmd
scripts\Setup_Environment.bat