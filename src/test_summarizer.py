import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# --- Configure Gemini (Generative AI SDK) ---
genai.configure(api_key=api_key)

# Import your modules
from src.loaders import load_pdf
from src.preprocessing import split_docs
from src.embeddings import get_embedder
from src.vectorstore import create_vectorstore
from src.agents.summarizer import run_summarizer


# --- LLM wrapper ---
def gemini_llm(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    # Prefer .text if available
    if hasattr(response, "text") and response.text:
        return response.text

    # Otherwise, dig into candidates
    if hasattr(response, "candidates") and response.candidates:
        parts = response.candidates[0].content.parts
        texts = [p.text for p in parts if hasattr(p, "text")]
        if texts:
            return " ".join(texts)

    return "No text response from Gemini"


if __name__ == "__main__":
    # --- 1. Load document ---
    docs = load_pdf("/Users/ekaanshjain/Desktop/ocjs_sample_grant.pdf")  # absolute path
    chunks = split_docs(docs)
    texts = [c.page_content for c in chunks]

    # --- 2. Embeddings + Vectorstore ---
    embedder = get_embedder()
    db = create_vectorstore(texts, embedder)
    retriever = db.as_retriever()

    # --- 3. Run summarizer ---
    summary = run_summarizer(gemini_llm, chunks)

    print("\n===== SUMMARY =====\n")
    print(summary)
