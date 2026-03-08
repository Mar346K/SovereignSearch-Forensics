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