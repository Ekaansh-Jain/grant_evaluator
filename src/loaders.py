from langchain_community.document_loaders import PyPDFLoader
import docx

from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(path: str):
    try:
        loader = PyMuPDFLoader(path)  # more reliable for mixed-content PDFs
        return loader.load()
    except Exception as e:
        print(f"[ERROR] Could not read {path}: {e}")
        return []
def load_docx(path: str):
    doc = docx.Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return [{"page_content": text, "metadata": {"source": path}}]

def load_txt(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [{"page_content": text, "metadata": {"source": path}}]