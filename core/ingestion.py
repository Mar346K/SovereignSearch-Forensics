from typing import Iterable, List
from itertools import islice
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config.settings import settings

def _lazy_chunk_generator(doc_iterator: Iterable[Document], splitter: RecursiveCharacterTextSplitter):
    """Helper generator to process documents lazily and yield individual chunks."""
    for doc in doc_iterator:
        # Split a single document/page at a time to prevent RAM spikes
        chunks = splitter.split_documents([doc])
        for chunk in chunks:
            yield chunk

def chunk_and_embed(db: Chroma, doc_iterator: Iterable[Document], matter: str, batch_size: int = 100) -> None:
    """
    Splits and embeds documents using lazy loading and batched insertion
    to prevent Out-Of-Memory (OOM) crashes on large forensic datasets.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size, 
        chunk_overlap=settings.chunk_overlap
    )
    
    # Create a true lazy generator of chunks
    chunk_generator = _lazy_chunk_generator(doc_iterator, splitter)
    
    while True:
        # Pull exactly 'batch_size' chunks from the generator
        batch = list(islice(chunk_generator, batch_size))
        if not batch:
            break
        
        # Inject forensic metadata
        for chunk in batch:
            chunk.metadata["matter"] = matter
            
        # Execute batch insertion safely
        db.add_documents(batch)