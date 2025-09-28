import os
from langchain.schema import Document
from src.loaders import load_pdf, load_docx, load_txt

def input_agent(file_path: str):
    """
    Load PDF/DOCX/TXT and return a list of LangChain Document objects
    with metadata including source and page number.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")

    # Load raw pages depending on file type
    if file_path.lower().endswith(".pdf"):
        raw_pages = load_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        raw_pages = load_docx(file_path)
    elif file_path.lower().endswith(".txt"):
        raw_pages = load_txt(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")

    # Convert to LangChain Document objects
    documents = []
    for i, page in enumerate(raw_pages):
        if isinstance(page, dict):
            content = page.get("page_content", page.get("text", ""))
        else:
            content = str(page)  # fallback

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": os.path.basename(file_path),
                    "page": i + 1
                }
            )
        )

    return documents
