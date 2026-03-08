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