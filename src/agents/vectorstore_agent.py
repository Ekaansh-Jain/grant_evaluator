from src.embeddings import get_embedder
from src.vectorstore import create_vectorstore
from langchain.schema import Document

def vectorstore_agent(pages: list, config_path="config.yaml", persist_dir="data/vectorstore"):
    """
    Create vectorstore and return a retriever wrapper.
    """
    # Use actual Document objects for Chroma, preserving metadata
    documents = [Document(page_content=p.page_content, metadata=p.metadata) for p in pages]

    embedder = get_embedder(config_path)
    # Use from_documents instead of from_texts
    db = create_vectorstore(documents, embedder, persist_dir)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # wrapped retriever
    def ask(query: str):
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
