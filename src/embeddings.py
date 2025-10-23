from langchain_huggingface import HuggingFaceEmbeddings
import yaml
import os

def get_embedder(config_path="config.yaml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} not found.")

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    if cfg is None or "model" not in cfg or "embeddings" not in cfg["model"]:
        raise ValueError(f"{config_path} must contain a 'model: embeddings:' section.")

    embedder =HuggingFaceEmbeddings(
        model_name=cfg["model"]["embeddings"]
    )
    return embedder