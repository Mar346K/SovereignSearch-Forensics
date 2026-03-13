# SovereignSearch-Forensics ⚖️
[![Vault Security & Integrity Pipeline](https://github.com/Mar346K/SovereignSearch-Forensics/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/SovereignSearch-Forensics/actions/workflows/ci.yml)

**A 100% Offline, Tamper-Evident RAG Intelligence Engine for Legal & Forensic Discovery.**

SovereignSearch-Forensics is a production-grade Data Vault and Retrieval-Augmented Generation (RAG) engine designed for zero-exfiltration environments. Built with a strict operations and QA mindset, this system ensures that highly sensitive legal depositions, discovery files, and forensic evidence can be synthesized locally without ever touching a third-party API.

## 🛡️ Core Architectural Philosophy

In forensic analysis, "it works" is not enough. The system must mathematically prove its own integrity, degrade gracefully under massive loads, and defend against hostile inputs. 

This architecture was engineered to meet strict enterprise DevSecOps standards:

* **Zero-Exfiltration:** 100% local processing utilizing hardware-aware local LLMs (Ollama) and vector databases (ChromaDB).
* **Immutable Auditability:** Every action is cryptographically chained, proving to opposing counsel or auditors that the data registry has not been tampered with.
* **OOM-Resilient Pipelines:** Built to ingest 10GB+ legal document dumps on consumer hardware without memory spikes via strict lazy-loading and batched backpressure.

## ⚙️ Enterprise Security & Resilience Features

### Forensic Integrity
* **SHA-256 Cryptographic Hashing:** Replaced legacy MD5 hashing with SHA-256 for bulletproof file identity and registry collision prevention.
* **Tamper-Evident Audit Ledgers:** SQLite logs utilize a blockchain-style `hash_chain` architecture. Every log hashes its own contents plus the previous log's hash, making retroactive database modification mathematically impossible to hide.
* **Strict Boundary Jailing:** `pathlib`-enforced path resolution mathematically guarantees user inputs cannot trigger directory traversal attacks to read host OS files.

### RAG Vulnerability Defense
* **LCEL Prompt Fencing:** Engineered a strict LangChain Expression Language (LCEL) pipeline that isolates document context from system instructions, effectively neutralizing Indirect Prompt Injection attacks embedded in malicious PDFs.

### Production Infrastructure
* **Batched Memory Backpressure:** Custom generator pipelines replace eager `.load()` calls with `.lazy_load()`, streaming multi-gigabyte files into the vector database in strict, memory-safe batches.
* **12-Factor App Compliance:** `pydantic-settings` manages all environment variables, ensuring deterministic configurations across Dev, Staging, and Prod without touching the codebase.
* **Least-Privilege Containerization:** Multi-stage Docker builds execute the application under a non-root `vaultuser`, neutralizing privilege escalation vectors.
* **Deterministic Testing:** A dedicated `pytest` suite mathematically proves all security boundaries, hashing algorithms, and RAG architectures before deployment.

## 🛠️ Technology Stack

* **Core Logic:** Python 3.11, Pydantic, Pytest
* **AI/RAG:** LangChain (LCEL), ChromaDB, Ollama (Llama 3.1, Nomic-Embed)
* **Document Parsing:** PyMuPDF, Tesseract OCR, Docx2txt
* **Frontend:** Streamlit
* **Infrastructure:** Docker, SQLite (WAL mode)

## 🚀 Quickstart

### 1. Environment Setup
The system automatically optimizes for your hardware (NVIDIA CUDA, AMD ROCm, or Intel Arc SYSMAN).
```bash
# Clone the repository
git clone [https://github.com/yourusername/SovereignSearch-Forensics.git](https://github.com/yourusername/SovereignSearch-Forensics.git)
cd SovereignSearch-Forensics

# Activate virtual environment and install frozen dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Security Suite
Prove the integrity of the vault before booting:

```Bash
python -m pytest tests/ -v
```

### 3. Boot the Vaults
```Bash
# Run the secure startup script
./scripts/01_START_VAULT.bat
```

Place all .pdf and .docx evidence files into the data_in/ directory and use the UI to initiate a secure sync.

### 🧪 Testing Coverage
The pytest suite enforces the core security boundaries:

* **test_audit_chaining: Verifies the cryptographic chain of the SQLite audit logs.**

* **test_get_file_hash_sha256: Proves memory-safe streaming and accurate SHA-256 output.**

* **test_safe_matter_path_resolution: Validates directory traversal defense.**

* **test_batched_lazy_ingestion: Proves the OOM-prevention backpressure logic.**

* **test_prompt_injection_fencing: Verifies the LCEL pipeline neutralizes malicious context.**
