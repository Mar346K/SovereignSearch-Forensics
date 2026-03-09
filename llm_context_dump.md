# AI Developer Context Dump
*Generated: 2026-03-08 19:43:19 UTC*

## Directory Tree
```text
SovereignSearch-Forensics/
├── .idea
│   ├── inspectionProfiles
│   │   ├── Project_Default.xml
│   │   └── profiles_settings.xml
│   ├── .gitignore
│   ├── SovereignSearch-Forensics.iml
│   ├── misc.xml
│   ├── modules.xml
│   └── workspace.xml
├── assets
├── config
│   ├── __init__.py
│   └── settings.py
├── core
│   ├── __init__.py
│   ├── database.py
│   ├── ingestion.py
│   └── rag_engine.py
├── data_in
│   ├── Smith_v_Jones
│   │   └── Depositions
│   ├── 0303PolicyForum_Ai_FF-2.pdf
│   ├── 04-Van Lier Walqui Language and CCSS FINAL.pdf
│   ├── 9a2dfa5e9d69b2c0bd06b38606827f1c_durant_promote.pdf
│   ├── AmericanGovernment3e-WEB.pdf
│   ├── Astronomy2e-WEB.pdf
│   ├── Biology2e-WEB.pdf
│   ├── Boroditsky_ea_2003.pdf
│   ├── BusinessEthics-OP.pdf
│   ├── CalculusVolume3-OP.pdf
│   ├── Calculus_Volume_1_-_WEB_68M1Z5W.pdf
│   ├── Calculus_Volume_2_-_WEB.pdf
│   ├── Chemistry2e-WEB.pdf
│   ├── CollegeAlgebra-OP.pdf
│   ├── Creative Commons guide_final.pdf
│   ├── IntroductionToSociology2e-OP_tbTLqMj.pdf
│   ├── Introduction_to_Philosophy-WEB_cszrKYp.pdf
│   ├── IntroductoryStatistics-OP_i6tAI7e.pdf
│   ├── Lowes_et_al_Manuscript_2_.pdf
│   ├── Microbiology-WEB.pdf
│   ├── Perspectives.pdf
│   ├── Psychology2e_WEB.pdf
│   ├── STUDENT_-_AP_Biology_Lab_Manual_Full.pdf
│   ├── STUDENT_-_AP_Physics_Lab_Manual_Full.pdf
│   ├── UniversityPhysicsVolume1-LR.pdf
│   ├── UniversityPhysicsVolume3-WEB.pdf
│   ├── University_Physics_Volume_2_-_WEB.pdf
│   ├── WhyMajorinLinguistics.pdf
│   ├── World_History_Volume_1-WEB.pdf
│   ├── World_History_Volume_2-WEB_LdwoslB.pdf
│   ├── carehive-september-2020-research-note-final.pdf
│   ├── goodman-2016-underrev.pdf
│   ├── nathannunn-slide-culture_and_the_historical_process_30min.pdf
│   ├── pietrocola.pdf
│   ├── realanal.pdf
│   ├── science-technology-society.pdf
│   ├── shapin-here_and_everywhere_1995.pdf
│   └── whorf.scienceandlinguistics.pdf
├── frontend
│   ├── __init__.py
│   ├── app.py
│   ├── components.py
│   └── views.py
├── output
├── scripts
│   ├── 01_START_VAULT.bat
│   └── Setup_Environment.bat
├── src
│   ├── __init__.py
│   ├── database.py
│   ├── file_manager.py
│   ├── rag_engine.py
│   └── sanitizer.py
├── utils
│   ├── __init__.py
│   ├── file_manager.py
│   └── sanitizer.py
├── vector_db
│   ├── 8705f7c3-8b00-4b32-951a-a3ff0827e971
│   │   ├── data_level0.bin
│   │   ├── header.bin
│   │   ├── index_metadata.pickle
│   │   ├── length.bin
│   │   └── link_lists.bin
│   ├── chroma.sqlite3
│   └── vault_metadata.sqlite3
├── .gitignore
├── Dockerfile
├── Setup_Quickstart.txt
├── check_setup.py
├── docker-compose.yml
├── logo.ico
└── requirements.txt
```

## Source Code

### File: `.gitignore`
```
# ==========================================
# SovereignSearch-Forensics .gitignore
# ==========================================

# Environments & Secrets
.env
.venv
env/
venv/
ENV/

# IDEs & Editors
.idea/
.vscode/
*.swp
*.swo

# Python Core
__pycache__/
*.py[cod]
*$py.class
*.so
.pytest_cache/

# Application State & Data (Privacy First)
data_in/
vector_db/
output/

# Application Logs
*.log

# OS Generated Files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```

### File: `check_setup.py`
```python
import sys
import ollama

print(f"--- System Check ---")
print(f"Python Version: {sys.version}")

try:
    # Fix for the new Ollama library version
    response = ollama.list()
    print("Ollama Connection: SUCCESS")

    # Check for the 'models' attribute and access name properly
    models = [m.model for m in response.models]
    print(f"Available Models: {models}")
except Exception as e:
    print(f"Ollama Connection: FAILED. Error: {e}")
```

### File: `docker-compose.yml`
```
version: '3.8'

services:
  vault-app:
    build: .
    container_name: sovereign-search-app
    ports:
      - "8501:8501"
    volumes:
      # Mount local directories so vectors and PDFs are not lost on restart
      - ./data_in:/app/data_in
      - ./vector_db:/app/vector_db
    environment:
      # Pass through hardware optimization flags
      - ZES_ENABLE_SYSMAN=1
      - OLLAMA_NUM_GPU=999
      # Point LangChain inside the container to the host machine's Ollama instance
      - OLLAMA_HOST=http://host.docker.internal:11434
    extra_hosts:
      # Allows the container to resolve 'host.docker.internal' to your Windows machine
      - "host.docker.internal:host-gateway"
```

### File: `Dockerfile`
```
# Use a slim Python 3.11 image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (Tesseract OCR for forensic image scanning)
# Clean up apt cache to keep the image size small
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first to leverage Docker's layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY config/ config/
COPY core/ core/
COPY frontend/ frontend/
COPY utils/ utils/

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the application
CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.headless", "true", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

### File: `logo.ico`
*Error reading file: 'utf-8' codec can't decode byte 0x9e in position 34: invalid start byte*

### File: `requirements.txt`
```
streamlit
streamlit-drawable-canvas
langchain
langchain-community
langchain-ollama
langchain-chroma
langchain-classic
docx2txt
PyMuPDF
pytesseract
Pillow
reportlab
```

### File: `Setup_Quickstart.txt`
```
========================================================================
             SOVEREIGN SEARCH v2.5 - QUICKSTART GUIDE
========================================================================
Thank you for choosing the Vault. This system provides professional-grade,
100% private AI intelligence using your local hardware.

Follow these 3 steps to initialize your Intelligence Engine.

1. INSTALL CORE DEPENDENCIES
------------------------------------------------------------------------
Before launching, ensure your computer is ready for AI acceleration:
- Run 'Setup_Environment.bat'.
  This will install the necessary Python libraries and download the
  Nomic-Embed and Llama 3.1 models to your machine.

2. HARDWARE OPTIMIZATION
------------------------------------------------------------------------
The Vault is designed to detect your GPU automatically.
- NVIDIA USERS: Ensure you have the latest CUDA drivers (v12+).
- AMD USERS: Ensure you have the latest Adrenalin/ROCm drivers.
- INTEL USERS: The system is pre-optimized for Intel Arc A-Series GPUs.

If your GPU is not detected, the system will fallback to CPU mode.
(Note: CPU mode is significantly slower for 1GB+ archives).

3. LOADING & SEARCHING
------------------------------------------------------------------------
- Place all files (.pdf, .docx) into the 'data_in' folder.
- Run 'Start_Sovereign_Search.bat'.
- Once the browser opens, click [⚡ Sync & Index New Files] in the sidebar.
- Wait for the progress bar to complete. Your data is now "Vaulted."

FORENSIC SYNTHESIS MODE
------------------------------------------------------------------------
Enable "Synthesis Mode" for complex inquiries. This forces the AI to
find connections across different subject matters (e.g., linking
Linguistics research with Sociology findings).

SUPPORT & TROUBLESHOOTING
------------------------------------------------------------------------
- Site "Refused to Connect"? Give the engine 10 seconds to warm up the GPU.
- Low GPU Usage? The initial file reading is a CPU task; the GPU will
  spike during the "Embedding" phase.
========================================================================
                      SECURE. PRIVATE. SOVEREIGN.
========================================================================
```

### File: `.idea\.gitignore`
```
# Default ignored files
/shelf/
/workspace.xml

```

### File: `.idea\misc.xml`
```
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="Black">
    <option name="sdkName" value="Python 3.11 (SovereignSearch-Forensics)" />
  </component>
  <component name="ProjectRootManager" version="2" project-jdk-name="Python 3.11 (SovereignSearch-Forensics)" project-jdk-type="Python SDK" />
</project>
```

### File: `.idea\modules.xml`
```
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectModuleManager">
    <modules>
      <module fileurl="file://$PROJECT_DIR$/.idea/SovereignSearch-Forensics.iml" filepath="$PROJECT_DIR$/.idea/SovereignSearch-Forensics.iml" />
    </modules>
  </component>
</project>
```

### File: `.idea\SovereignSearch-Forensics.iml`
```
<?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <excludeFolder url="file://$MODULE_DIR$/.venv" />
    </content>
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>
```

### File: `.idea\workspace.xml`
```
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="SELECTIVE" />
  </component>
  <component name="ChangeListManager">
    <list default="true" id="5feddb3d-a291-4f1d-9826-4c2bf26999a7" name="Changes" comment="" />
    <option name="SHOW_DIALOG" value="false" />
    <option name="HIGHLIGHT_CONFLICTS" value="true" />
    <option name="HIGHLIGHT_NON_ACTIVE_CHANGELIST" value="false" />
    <option name="LAST_RESOLUTION" value="IGNORE" />
  </component>
  <component name="FileTemplateManagerImpl">
    <option name="RECENT_TEMPLATES">
      <list>
        <option value="Python Script" />
      </list>
    </option>
  </component>
  <component name="ProjectColorInfo"><![CDATA[{
  "associatedIndex": 6
}]]></component>
  <component name="ProjectId" id="37cnoTIje1AKxuruyx88B5PiZCb" />
  <component name="ProjectViewState">
    <option name="hideEmptyMiddlePackages" value="true" />
    <option name="showLibraryContents" value="true" />
  </component>
  <component name="PropertiesComponent"><![CDATA[{
  "keyToString": {
    "Python.check_setup.executor": "Run",
    "Python.ingest_data.executor": "Run",
    "Python.organizer.executor": "Run",
    "RunOnceActivity.ShowReadmeOnStart": "true"
  }
}]]></component>
  <component name="SharedIndexes">
    <attachedChunks>
      <set>
        <option value="bundled-python-sdk-d7ad00fb9fc3-c546a90a8094-com.jetbrains.pycharm.community.sharedIndexes.bundled-PC-242.23726.102" />
      </set>
    </attachedChunks>
  </component>
  <component name="SpellCheckerSettings" RuntimeDictionaries="0" Folders="0" CustomDictionaries="0" DefaultDictionary="application-level" UseSingleDictionary="true" transferred="true" />
  <component name="TaskManager">
    <task active="true" id="Default" summary="Default task">
      <changelist id="5feddb3d-a291-4f1d-9826-4c2bf26999a7" name="Changes" comment="" />
      <created>1767211401872</created>
      <option name="number" value="Default" />
      <option name="presentableId" value="Default" />
      <updated>1767211401872</updated>
    </task>
    <servers />
  </component>
</project>
```

### File: `.idea\inspectionProfiles\profiles_settings.xml`
```
<component name="InspectionProjectProfileManager">
  <settings>
    <option name="USE_PROJECT_PROFILE" value="false" />
    <version value="1.0" />
  </settings>
</component>
```

### File: `.idea\inspectionProfiles\Project_Default.xml`
```
<component name="InspectionProjectProfileManager">
  <profile version="1.0">
    <option name="myName" value="Project Default" />
    <inspection_tool class="PyPackageRequirementsInspection" enabled="true" level="WARNING" enabled_by_default="true">
      <option name="ignoredPackages">
        <value>
          <list size="22">
            <item index="0" class="java.lang.String" itemvalue="pyinstaller" />
            <item index="1" class="java.lang.String" itemvalue="lackey" />
            <item index="2" class="java.lang.String" itemvalue="pydantic" />
            <item index="3" class="java.lang.String" itemvalue="networkx" />
            <item index="4" class="java.lang.String" itemvalue="faiss-cpu" />
            <item index="5" class="java.lang.String" itemvalue="opencv-python" />
            <item index="6" class="java.lang.String" itemvalue="ollama" />
            <item index="7" class="java.lang.String" itemvalue="sentence-transformers" />
            <item index="8" class="java.lang.String" itemvalue="pipreqs" />
            <item index="9" class="java.lang.String" itemvalue="requests" />
            <item index="10" class="java.lang.String" itemvalue="numpy" />
            <item index="11" class="java.lang.String" itemvalue="pywinauto" />
            <item index="12" class="java.lang.String" itemvalue="pyyaml" />
            <item index="13" class="java.lang.String" itemvalue="python-socketio" />
            <item index="14" class="java.lang.String" itemvalue="fastapi" />
            <item index="15" class="java.lang.String" itemvalue="pyqtgraph" />
            <item index="16" class="java.lang.String" itemvalue="langchain" />
            <item index="17" class="java.lang.String" itemvalue="pillow" />
            <item index="18" class="java.lang.String" itemvalue="PySide6" />
            <item index="19" class="java.lang.String" itemvalue="uvicorn" />
            <item index="20" class="java.lang.String" itemvalue="poco" />
            <item index="21" class="java.lang.String" itemvalue="nuitka" />
          </list>
        </value>
      </option>
    </inspection_tool>
  </profile>
</component>
```

### File: `config\settings.py`
```python
import os
from pathlib import Path
from pydantic import BaseModel, Field

class SystemSettings(BaseModel):
    """
    Centralized configuration and environment state for SovereignSearch-Forensics.
    Provides strict type hinting and validation for all application variables.
    """
    # Core Paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data_in")
    db_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "vector_db")
    db_path: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "vector_db" / "vault_metadata.sqlite3")

    # Local AI Model Configuration
    embedding_model: str = Field(default="nomic-embed-text", description="Fast, local embedding model.")
    llm_model: str = Field(default="llama3.1", description="Primary local reasoning model.")
    llm_temperature: float = Field(default=0.1, description="Low temperature for analytical/forensic accuracy.")
    
    # Hardware & VRAM Tuning (Tuned for 16GB GPU VRAM / High Capacity System RAM)
    ollama_num_gpu: int = Field(default=999, description="Forces Ollama to offload maximum layers to the GPU.")
    zes_enable_sysman: int = Field(default=1, description="Enables Intel SYSMAN telemetry for Arc/OpenVINO.")
    
    # RAG Tuning
    chunk_size: int = 1000
    chunk_overlap: int = 150
    retriever_k: int = 3

    def initialize_environment(self) -> None:
        """Ensures all critical directories exist before engine boot."""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.db_dir, exist_ok=True)
        
        # Inject hardware flags directly into the OS environment for child processes
        os.environ["OLLAMA_NUM_GPU"] = str(self.ollama_num_gpu)
        os.environ["ZES_ENABLE_SYSMAN"] = str(self.zes_enable_sysman)

# Global settings instance to be imported across the app
settings = SystemSettings()
```

### File: `config\__init__.py`
```python

```

### File: `core\database.py`
```python
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any

from config.settings import settings

def get_connection() -> sqlite3.Connection:
    """
    Returns a thread-safe SQLite connection with WAL (Write-Ahead Logging) enabled.
    WAL mode significantly improves concurrency and disk I/O for local-first applications.
    """
    # Dynamically pull the database path from our Pydantic settings
    conn = sqlite3.connect(settings.db_path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;") 
    return conn

def init_db() -> None:
    """
    Initializes the database schemas for the file registry and forensic audit trails.
    """
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS file_registry (
                hash TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                matter TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matter TEXT NOT NULL,
                file TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL
            )
        ''')

def load_registry() -> Dict[str, Dict[str, str]]:
    """
    Loads the file registry into memory for fast O(1) hash lookups during ingestion.
    
    Returns:
        Dict mapping file hashes to their metadata (name, matter, timestamp).
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hash, name, matter, timestamp FROM file_registry")
        
        return {
            row[0]: {"name": row[1], "matter": row[2], "timestamp": row[3]} 
            for row in cursor.fetchall()
        }

def register_file(file_hash: str, name: str, matter: str) -> None:
    """
    Commits a newly embedded file to the SQLite registry.
    """
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO file_registry (hash, name, matter, timestamp) VALUES (?, ?, ?, ?)",
            (file_hash, name, matter, datetime.now().isoformat())
        )

def log_audit(action: str, matter: str, file: str, details: Any) -> None:
    """
    Safely logs system actions and forensic modifications to the immutable audit trail.
    """
    # Ensure details are properly serialized to JSON if a dict or list is passed
    details_str = json.dumps(details) if isinstance(details, (dict, list)) else str(details)
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO audit_trail (matter, file, action, details, timestamp) VALUES (?, ?, ?, ?, ?)",
            (matter, file, action, details_str, datetime.now().isoformat())
        )
```

### File: `core\ingestion.py`
```python
from typing import List, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config.settings import settings

def chunk_and_embed(db: Chroma, docs: List[Document], matter: str) -> None:
    """
    Splits loaded documents into semantic chunks and embeds them into the vector database.
    
    Args:
        db (Chroma): The active Chroma database instance.
        docs (List[Document]): The raw documents loaded from the file system.
        matter (str): The legal or structural matter/folder name to tag as metadata.
    """
    # Initialize splitter using our centralized hardware/RAG tuning settings
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size, 
        chunk_overlap=settings.chunk_overlap
    )
    
    # Process the chunks in system memory
    chunks = splitter.split_documents(docs)
    
    # Inject forensic metadata
    for chunk in chunks:
        chunk.metadata["matter"] = matter
        
    # Execute batch insertion into the vector store
    # With large VRAM and system memory, Chroma can handle these bulk operations efficiently
    if chunks:
        db.add_documents(chunks)
```

### File: `core\rag_engine.py`
```python
from typing import Tuple, Any
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

from config.settings import settings

def init_system() -> Tuple[Chroma, ChatOllama]:
    """
    Initializes and returns the ChromaDB client and local LLM.
    Leverages settings for hardware-aware model loading and optimized VRAM allocation.
    
    Returns:
        Tuple containing the configured Chroma vector database and the ChatOllama LLM.
    """
    # Nomic is highly efficient for local embedding matrices
    emb = OllamaEmbeddings(model=settings.embedding_model)
    
    # Initialize Chroma with our centralized path
    db = Chroma(
        persist_directory=str(settings.db_dir), 
        embedding_function=emb
    )
    
    # Initialize the reasoning model, locking in a low temperature for forensic accuracy
    llm = ChatOllama(
        model=settings.llm_model, 
        temperature=settings.llm_temperature
    )
    
    return db, llm

def get_retriever(db: Chroma) -> VectorStoreRetriever:
    """
    Returns the configured retrieval interface for the vector database.
    
    Args:
        db (Chroma): The active Chroma vector database instance.
        
    Returns:
        VectorStoreRetriever: Interface ready for similarity searches.
    """
    return db.as_retriever(search_kwargs={"k": settings.retriever_k})
```

### File: `core\__init__.py`
```python

```

### File: `data_in\0303PolicyForum_Ai_FF-2.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\04-Van Lier Walqui Language and CCSS FINAL.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xc4 in position 10: invalid continuation byte*

### File: `data_in\9a2dfa5e9d69b2c0bd06b38606827f1c_durant_promote.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\AmericanGovernment3e-WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Astronomy2e-WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Biology2e-WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Boroditsky_ea_2003.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xc4 in position 10: invalid continuation byte*

### File: `data_in\BusinessEthics-OP.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\CalculusVolume3-OP.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Calculus_Volume_1_-_WEB_68M1Z5W.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Calculus_Volume_2_-_WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\carehive-september-2020-research-note-final.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Chemistry2e-WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\CollegeAlgebra-OP.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Creative Commons guide_final.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\goodman-2016-underrev.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 10: invalid continuation byte*

### File: `data_in\IntroductionToSociology2e-OP_tbTLqMj.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Introduction_to_Philosophy-WEB_cszrKYp.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\IntroductoryStatistics-OP_i6tAI7e.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Lowes_et_al_Manuscript_2_.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 10: invalid continuation byte*

### File: `data_in\Microbiology-WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\nathannunn-slide-culture_and_the_historical_process_30min.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 10: invalid continuation byte*

### File: `data_in\Perspectives.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\pietrocola.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\Psychology2e_WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\realanal.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xd0 in position 10: invalid continuation byte*

### File: `data_in\science-technology-society.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xaa in position 10: invalid start byte*

### File: `data_in\shapin-here_and_everywhere_1995.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\STUDENT_-_AP_Biology_Lab_Manual_Full.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xc4 in position 10: invalid continuation byte*

### File: `data_in\STUDENT_-_AP_Physics_Lab_Manual_Full.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xc4 in position 10: invalid continuation byte*

### File: `data_in\UniversityPhysicsVolume1-LR.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\UniversityPhysicsVolume3-WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\University_Physics_Volume_2_-_WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\whorf.scienceandlinguistics.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xc4 in position 10: invalid continuation byte*

### File: `data_in\WhyMajorinLinguistics.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\World_History_Volume_1-WEB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `data_in\World_History_Volume_2-WEB_LdwoslB.pdf`
*Error reading file: 'utf-8' codec can't decode byte 0xe2 in position 10: invalid continuation byte*

### File: `frontend\app.py`
```python
import streamlit as st
import os

# 1. Initialize environment and configs before importing heavy AI modules
from config.settings import settings
settings.initialize_environment()

from core.database import init_db
from core.rag_engine import init_system
from utils.file_manager import get_matters
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
    """
    Caches the database and model initialization. 
    Prevents the LLM and Embedding models from reloading into GPU VRAM on every UI interaction.
    """
    init_db()
    db, llm = init_system()
    return db, llm

db, llm = startup_system()

# 4. SIDEBAR: CONTROL CENTER
with st.sidebar:
    st.title("⚖️ Workspace")
    
    matters = get_matters()
    selected_matter = st.selectbox("Current Matter:", matters)

    m_path = os.path.join(settings.data_dir, selected_matter.replace(" / ", "/"))
    all_pdfs = [f for f in os.listdir(m_path) if f.lower().endswith('.pdf')] if os.path.exists(m_path) else []
    
    focus_file = st.selectbox("🎯 Focus Scan:", ["None"] + all_pdfs)

    st.divider()
    mode = st.radio("Switch View:", ["Discovery Hub", "Forensic Assembly"])

# 5. MAIN UI ROUTING
if mode == "Discovery Hub":
    render_discovery_hub(db, selected_matter, focus_file)
elif mode == "Forensic Assembly":
    render_forensic_assembly(selected_matter, all_pdfs, m_path)
```

### File: `frontend\components.py`
```python
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
```

### File: `frontend\views.py`
```python
import streamlit as st
import os
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
from streamlit_drawable_canvas import st_canvas
from langchain_chroma import Chroma

from frontend.components import live_query_window, run_ingestion_ui
from utils.file_manager import build_sync_queue
from core.database import log_audit

def render_discovery_hub(db: Chroma, selected_matter: str, focus_file: str) -> None:
    """Renders the primary document discovery and ingestion interface."""
    st.title("📂 Sovereign Discovery Hub")

    with st.expander("🔄 Vault Synchronization", expanded=True):
        if st.button("⚡ Start Priority Sync", type="primary"):
            sync_queue = build_sync_queue(selected_matter, focus_file)
            run_ingestion_ui(sync_queue, db, selected_matter)

    st.divider()
    live_query_window(db)

def render_forensic_assembly(selected_matter: str, all_pdfs: list[str], m_path: str) -> None:
    """Renders the manual OCR and data extraction correction tool."""
    st.title("🧩 Forensic Assembly & Audit")
    
    if "Unassigned" in selected_matter:
        st.warning("Select a Matter to use Forensic Assembly.")
        return
        
    if not all_pdfs:
        st.info("No PDF evidence available in this matter.")
        return

    doc_name = st.selectbox("Select Evidence:", all_pdfs)
    doc_path = os.path.join(m_path, doc_name)
    
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
```

### File: `frontend\__init__.py`
```python

```

### File: `scripts\01_START_VAULT.bat`
```
@echo off
title Sovereign Search: Universal Engine
echo 🕵️ Detecting Hardware Acceleration...

:: Navigate to the project root (since script is in scripts/)
cd /d "%~dp0\.."

:: --- NVIDIA SUPPORT ---
set CUDA_VISIBLE_DEVICES=0

:: --- AMD SUPPORT ---
set HSA_OVERRIDE_GFX_VERSION=10.3.0
set ROCR_VISIBLE_DEVICES=0

:: --- INTEL SUPPORT (Pre-optimized for Arc A770 16GB) ---
set OLLAMA_NUM_GPU=999
set ZES_ENABLE_SYSMAN=1

:: Start the Vault
echo [*] Activating Virtual Environment...
call .venv\Scripts\activate

echo [*] Initializing Local GPU and booting RAG Engine...
start /b "" python -m streamlit run frontend/app.py --server.headless true --server.port 8501

echo [*] Waiting for Streamlit Server to spin up...
timeout /t 10 /nobreak >nul
start http://localhost:8501
exit
```

### File: `scripts\Setup_Environment.bat`
```
@echo off
title Sovereign Search - First Time Setup
echo 🕵️ Initializing Forensic AI Environment...

:: Navigate to the project root (assuming script is run from scripts/ directory)
cd /d "%~dp0\.."

:: 1. Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH. Please install Python 3.10+.
    pause
    exit
)

:: 2. Create and Activate Virtual Environment
echo [*] Setting up Python Virtual Environment...
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate

:: 3. Install Dependencies
echo [*] Installing required Python packages...
python -m pip install --upgrade pip
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [!] requirements.txt not found in the root directory!
    pause
    exit
)

:: 4. Initialize Vault Directories
echo [*] Initializing SQLite schema and Vault directories...
if not exist "data_in" mkdir data_in
if not exist "vector_db" mkdir vector_db

:: 5. Check for Ollama
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Ollama not found. Please install it from https://ollama.com
    start https://ollama.com
    pause
    exit
)

:: 6. Pull Required Local AI Models
echo [*] Downloading Intelligence Models (this may take a few minutes)...
ollama pull llama3.1
ollama pull nomic-embed-text

:: 7. Tesseract OCR Warning
echo.
echo ====================================================================
echo [i] NOTE: Forensic Assembly mode requires Tesseract OCR on Windows.
echo     If you haven't installed the binaries, please download from:
echo     https://github.com/UB-Mannheim/tesseract/wiki
echo     Ensure it is added to your System PATH.
echo ====================================================================
echo.

echo [SUCCESS] Environment is fully configured.
echo You can now launch the engine using scripts\01_START_VAULT.bat
pause
```

### File: `src\database.py`
```python
import sqlite3
import json
from datetime import datetime

DB_PATH = "vector_db/vault_metadata.sqlite3"

def get_connection():
    """Returns a thread-safe SQLite connection with WAL enabled."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    """Initializes the database schemas for registry and auditing."""
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS file_registry (
                            hash TEXT PRIMARY KEY,
                            name TEXT,
                            matter TEXT,
                            timestamp TEXT)''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS audit_trail (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            matter TEXT,
                            file TEXT,
                            action TEXT,
                            details TEXT,
                            timestamp TEXT)''')

def load_registry():
    """Returns the file registry as a dictionary for fast hash lookups."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hash, name, matter, timestamp FROM file_registry")
        return {row[0]: {"name": row[1], "matter": row[2], "timestamp": row[3]} for row in cursor.fetchall()}

def register_file(file_hash, name, matter):
    """Commits a newly embedded file to the registry."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO file_registry (hash, name, matter, timestamp) VALUES (?, ?, ?, ?)",
            (file_hash, name, matter, str(datetime.now()))
        )

def log_audit(action, matter, file, details):
    """Safely logs system actions to the audit trail."""
    details_str = json.dumps(details) if isinstance(details, dict) else str(details)
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO audit_trail (matter, file, action, details, timestamp) VALUES (?, ?, ?, ?, ?)",
            (matter, file, action, details_str, str(datetime.now()))
        )
```

### File: `src\file_manager.py`
```python
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
```

### File: `src\rag_engine.py`
```python
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

DB_DIR = "vector_db"

def init_system():
    """Initializes and returns the ChromaDB client and local LLM."""
    # Preserving optimized configuration for local hardware acceleration (Intel Arc)
    emb = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=DB_DIR, embedding_function=emb)
    llm = ChatOllama(model="llama3.1", temperature=0.1)
    return db, llm

def get_retriever(db, k=3):
    """Returns the retrieval interface for the vector database."""
    return db.as_retriever(search_kwargs={"k": k})

def chunk_and_embed(db, docs, matter):
    """Splits documents and embeds them into the vector database."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    for c in chunks:
        c.metadata["matter"] = matter
    db.add_documents(chunks)
```

### File: `src\sanitizer.py`
```python
import os
import fitz  # PyMuPDF

DATA_DIR = "data_in"


def sanitize_vault():
    print("🔍 Starting Data Sanitization...")
    report = {"clean": [], "scanned_image": [], "corrupted": []}

    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.lower().endswith(".pdf"):
                f_path = os.path.join(root, file)
                try:
                    doc = fitz.open(f_path)
                    text_found = False
                    for page in doc:
                        if page.get_text().strip():
                            text_found = True
                            break

                    if text_found:
                        report["clean"].append(file)
                    else:
                        report["scanned_image"].append(file)
                    doc.close()
                except:
                    report["corrupted"].append(file)

    print("\n--- SANITIZATION REPORT ---")
    print(f"✅ Readable: {len(report['clean'])}")
    print(f"🚨 Scanned (Needs OCR): {len(report['scanned_image'])}")
    print(f"❌ Corrupted: {len(report['corrupted'])}")

    if report["scanned_image"]:
        print("\nAction Required: The following files are images and cannot be read by AI without OCR:")
        for f in report["scanned_image"]: print(f" - {f}")


if __name__ == "__main__":
    sanitize_vault()
```

### File: `src\__init__.py`
```python

```

### File: `utils\file_manager.py`
```python
import os
import hashlib
from typing import List, Dict, Any, Generator, Tuple, Optional
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader
from langchain_chroma import Chroma

from config.settings import settings
from core.database import load_registry, register_file, log_audit
from core.ingestion import chunk_and_embed

def get_file_hash(filepath: str) -> str:
    """Generates an MD5 hash for a file to track indexing status and prevent duplicates."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192): 
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
```

### File: `utils\sanitizer.py`
```python
import os
import fitz  # PyMuPDF
from typing import Dict, List

from config.settings import settings

def sanitize_vault() -> Dict[str, List[str]]:
    """
    Scans the data directory for PDFs and categorizes them by readability.
    Identifies files that require OCR preprocessing for the AI to ingest them.
    
    Returns:
        Dict containing lists of 'clean', 'scanned_image', and 'corrupted' filenames.
    """
    print("🔍 Starting Data Sanitization...")
    report: Dict[str, List[str]] = {"clean": [], "scanned_image": [], "corrupted": []}

    for root, _, files in os.walk(settings.data_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                f_path = os.path.join(root, file)
                try:
                    doc = fitz.open(f_path)
                    text_found = False
                    for page in doc:
                        if page.get_text().strip():
                            text_found = True
                            break

                    if text_found:
                        report["clean"].append(file)
                    else:
                        report["scanned_image"].append(file)
                    doc.close()
                except Exception:
                    # Catching Exception specifically prevents catching SystemExit/KeyboardInterrupt
                    report["corrupted"].append(file)

    print("\n--- SANITIZATION REPORT ---")
    print(f"✅ Readable: {len(report['clean'])}")
    print(f"🚨 Scanned (Needs OCR): {len(report['scanned_image'])}")
    print(f"❌ Corrupted: {len(report['corrupted'])}")

    if report["scanned_image"]:
        print("\nAction Required: The following files are images and cannot be read by AI without OCR:")
        for f in report["scanned_image"]: 
            print(f" - {f}")
            
    return report

if __name__ == "__main__":
    # Ensure environment is initialized if run as a standalone script
    settings.initialize_environment()
    sanitize_vault()
```

### File: `utils\__init__.py`
```python

```

### File: `vector_db\chroma.sqlite3`
*Error reading file: 'utf-8' codec can't decode byte 0x87 in position 27: invalid start byte*

### File: `vector_db\vault_metadata.sqlite3`
*Error reading file: 'utf-8' codec can't decode byte 0x8b in position 99: invalid start byte*

### File: `vector_db\8705f7c3-8b00-4b32-951a-a3ff0827e971\data_level0.bin`
*Error reading file: 'utf-8' codec can't decode byte 0x8f in position 134: invalid start byte*

### File: `vector_db\8705f7c3-8b00-4b32-951a-a3ff0827e971\header.bin`
*Error reading file: 'utf-8' codec can't decode byte 0xbc in position 21: invalid start byte*

### File: `vector_db\8705f7c3-8b00-4b32-951a-a3ff0827e971\index_metadata.pickle`
*Error reading file: 'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte*

### File: `vector_db\8705f7c3-8b00-4b32-951a-a3ff0827e971\length.bin`
*Error reading file: 'utf-8' codec can't decode byte 0xa0 in position 8: invalid start byte*

### File: `vector_db\8705f7c3-8b00-4b32-951a-a3ff0827e971\link_lists.bin`
*Error reading file: 'utf-8' codec can't decode byte 0xa2 in position 36: invalid start byte*
