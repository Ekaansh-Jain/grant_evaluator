from langchain.text_splitter import RecursiveCharacterTextSplitter
import yaml
import os

def split_docs(docs, config_path="config.yaml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found.")

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    if cfg is None:
        raise ValueError(f"{config_path} is empty. It must contain a 'retrieval' section.")

    if "retrieval" not in cfg:
        raise ValueError("The config file must contain a 'retrieval' section.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg["retrieval"].get("chunk_size", 1000),
        chunk_overlap=cfg["retrieval"].get("chunk_overlap", 100)
    )
    return splitter.split_documents(docs)