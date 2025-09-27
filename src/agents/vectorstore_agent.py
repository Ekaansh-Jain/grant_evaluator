# agents/vectorstore_agent.py

from src.embeddings import get_embedder
from src.vectorstore import create_vectorstore
from langchain.vectorstores.base import VectorStoreRetriever

def vectorstore_agent(chunks: list, config_path="config.yaml", persist_dir="data/vectorstore"):
    """
    Vectorstore Agent: Create embeddings and return a retriever.
    
    Args:
        chunks (list): List of chunk dicts {"page_content": str, "metadata": dict}
        config_path (str): Path to config.yaml for embedding model
        persist_dir (str): Directory to save the vectorstore
    
    Returns:
        tuple: (vectorstore, retriever)
    """
    # Extract text from chunks
    texts = [c.page_content for c in chunks]
    
    # Load embedder
    embedder = get_embedder(config_path=config_path)
    
    # Create vectorstore
    db = create_vectorstore(texts, embedder, persist_dir=persist_dir)
    
    # Create retriever for RAG
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    
    return db, retriever


# Demo run
if __name__ == "__main__":
    from agents.input_agent import input_agent
    sample_path = "/path/to/sample_grant.pdf"
    
    data = input_agent(sample_path)
    db, retriever = vectorstore_agent(data["chunks"])
    
    print("Vectorstore created!")
    # Example retrieval
    query = "Objectives of the proposal"
    results = retriever.get_relevant_documents(query)
    print(f"Retrieved {len(results)} documents for query: '{query}'")
