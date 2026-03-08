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