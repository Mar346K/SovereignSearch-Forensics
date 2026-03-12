import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class SystemSettings(BaseSettings):
    """
    Centralized configuration and environment state.
    Complies with 12-Factor App standards by reading from the environment first.
    """
    base_dir: Path = Path(__file__).parent.parent
    data_dir: Path = Field(default=Path(__file__).parent.parent / "data_in")
    db_dir: Path = Field(default=Path(__file__).parent.parent / "vector_db")
    db_path: Path = Field(default=Path(__file__).parent.parent / "vector_db" / "vault_metadata.sqlite3")

    embedding_model: str = "nomic-embed-text"
    llm_model: str = "llama3.1"
    llm_temperature: float = 0.1
    
    ollama_num_gpu: int = 999
    zes_enable_sysman: int = 1
    
    chunk_size: int = 1000
    chunk_overlap: int = 150
    retriever_k: int = 3

    # Automatically load overrides from a .env file if it exists
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def initialize_environment(self) -> None:
        """Ensures all critical directories exist before engine boot."""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.db_dir, exist_ok=True)
        os.environ["OLLAMA_NUM_GPU"] = str(self.ollama_num_gpu)
        os.environ["ZES_ENABLE_SYSMAN"] = str(self.zes_enable_sysman)

settings = SystemSettings()