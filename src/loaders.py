from langchain_community.document_loaders import PyPDFLoader
import docx

try:
    from langchain_community.document_loaders import PyMuPDFLoader
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("[WARNING] PyMuPDF not available, falling back to PyPDF")

def load_pdf(path: str):
    try:
        if PYMUPDF_AVAILABLE:
            loader = PyMuPDFLoader(path)  # more reliable for mixed-content PDFs
        else:
            loader = PyPDFLoader(path)  # fallback to PyPDF
        docs = loader.load()
        if not docs:
            print(f"[WARNING] No pages extracted from {path}")
        return docs
    except Exception as e:
        print(f"[ERROR] Could not read {path}: {e}")
        import traceback
        traceback.print_exc()
        return []
def load_docx(path: str):
    doc = docx.Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return [{"page_content": text, "metadata": {"source": path}}]

def load_txt(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [{"page_content": text, "metadata": {"source": path}}]