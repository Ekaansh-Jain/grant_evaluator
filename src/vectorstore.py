from langchain_community.vectorstores import Chroma
import os
from langchain.schema import Document

def create_vectorstore(docs: list[Document], embeddings, persist_dir="data/vectorstore"):
    """
    Create a Chroma vectorstore from Document objects with metadata.
    """
    os.makedirs(persist_dir, exist_ok=True)
    db = Chroma.from_documents(
        documents=docs,        # <-- preserve text + metadata
        embedding=embeddings,  
        persist_directory=persist_dir
    )
    return db


def load_vectorstore(embedding, persist_dir="data/vectorstore"):
    """
    Load an existing Chroma vectorstore from disk.
    """
    db = Chroma(
        embedding_function=embedding,  # LangChain embedding object
        persist_directory=persist_dir
    )
    return db