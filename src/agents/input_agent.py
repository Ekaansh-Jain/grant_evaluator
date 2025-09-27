# agents/input_agent.py

from src.loaders import load_pdf, load_docx, load_txt
from src.preprocessing import split_docs
import os

def input_agent(file_path: str, config_path="config.yaml") -> dict:
    """
    Input Agent: Load document, structure basic info, split into chunks.
    
    Args:
        file_path (str): Path to PDF, DOCX, or TXT file.
        config_path (str): Path to config.yaml for chunking settings.
    
    Returns:
        dict: {
            "title": str,
            "abstract": str,
            "objectives": str,
            "methodology": str,
            "budget": float or None,
            "duration_months": int or None,
            "requested_amount": float or None,
            "chunks": list of dicts {"page_content": str, "metadata": dict}
        }
    """
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        docs = load_pdf(file_path)
    elif ext == ".docx":
        docs = load_docx(file_path)
    elif ext == ".txt":
        docs = load_txt(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")
    
    # Split into chunks
    chunks = split_docs(docs, config_path=config_path)
    
    # Placeholder extraction for demo
    structured_data = {
        "title": "Not provided",
        "abstract": "Not provided",
        "objectives": "Not provided",
        "methodology": "Not provided",
        "budget": None,
        "duration_months": None,
        "requested_amount": None,
        "chunks": chunks
    }
    
    return structured_data


# Demo run
if __name__ == "__main__":
    sample_path = "/path/to/sample_grant.pdf"
    data = input_agent(sample_path)
    print(f"Structured Input:\n{data}")
    print(f"Number of chunks: {len(data['chunks'])}")
