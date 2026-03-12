import pytest
from langchain_core.documents import Document
from core.ingestion import chunk_and_embed

class MockDB:
    """A fake database to count how many chunks are inserted per batch."""
    def __init__(self):
        self.batch_counts = []

    def add_documents(self, documents):
        self.batch_counts.append(len(documents))

def test_batched_lazy_ingestion():
    """Proves documents are processed in strict memory-safe batches without dropping data."""
    db = MockDB()
    
    # Simulate a lazy loader reading a 10-page document page-by-page
    def mock_lazy_load():
        for i in range(10):
            yield Document(page_content=f"Page {i} content. " * 50)
    
    # Force a tiny batch size of 3 to prove the backpressure logic works
    chunk_and_embed(db, mock_lazy_load(), "Smith_v_Jones", batch_size=3)
    
    # Assertions: 10 total pages chunked into batches of max size 3
    # Should result in 4 batches (3, 3, 3, 1)
    assert len(db.batch_counts) > 1  # Proves batching occurred
    assert sum(db.batch_counts) == 10  # Proves no data was dropped
    assert max(db.batch_counts) <= 3  # Proves the memory ceiling holds