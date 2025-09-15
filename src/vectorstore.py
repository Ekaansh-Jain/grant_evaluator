from langchain_community.vectorstores import Chroma
import os

def create_vectorstore(texts, embeddings, persist_dir="data/vectorstore"):
    """
    Create a Chroma vectorstore from texts and an embedding object.
    """
    os.makedirs(persist_dir, exist_ok=True)
    db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,      # must be a LangChain embedding object
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