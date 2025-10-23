from src.embeddings import get_embedder
from src.vectorstore import create_vectorstore
from langchain.schema import Document

def vectorstore_agent(pages: list, config_path="config.yaml", persist_dir=None, deterministic: bool = True):
    """
    Create vectorstore and return a retriever wrapper.
    
    Args:
        pages: List of document pages
        config_path: Path to config file
        persist_dir: Directory to persist vectorstore. If None (default), uses in-memory mode for isolation.
        deterministic: Use deterministic retrieval settings
    
    Returns:
        dict with 'vectorstore' and 'ask' function
    """
    # Use actual Document objects for Chroma, preserving metadata
    documents = [Document(page_content=p.page_content, metadata=p.metadata) for p in pages]

    embedder = get_embedder(config_path)
    
    # Create vectorstore WITHOUT persistence by default (in-memory) to avoid contamination
    # Each evaluation gets a fresh, isolated vectorstore
    db = create_vectorstore(documents, embedder, persist_dir=persist_dir)
    
    # Use deterministic retriever settings by default (fixed k, similarity search)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 10})

    # wrapped retriever
    def ask(query: str):
        # Ensure a stable ordering of retrieved documents
        retrieved_docs = retriever.get_relevant_documents(query)
        return [
            {
                "page_number": doc.metadata.get("page", "Unknown"),
                "text": doc.page_content,
                "source": doc.metadata.get("source", "Unknown")
            }
            for doc in retrieved_docs
        ]
    
    return {"vectorstore": db, "ask": ask}
