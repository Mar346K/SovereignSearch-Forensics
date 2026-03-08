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