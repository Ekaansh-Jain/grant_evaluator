import os
from dotenv import load_dotenv
import google.genai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# --- Gemini setup ---
client = genai.Client(api_key=api_key)

# Import your modules
from src.loaders import load_pdf
from src.preprocessing import split_docs
from src.embeddings import get_embedder
from src.vectorstore import create_vectorstore
from src.agents.scoring import run_scorer

# --- LLM wrapper ---
def gemini_llm(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # or "gemini-1.5-pro"
        contents=prompt,
    )
    return response.text

if __name__ == "__main__":
    # --- 1. Load document ---
    docs = load_pdf("/Users/ekaanshjain/Desktop/ocjs_sample_grant.pdf")
    chunks = split_docs(docs)
    texts = [c.page_content for c in chunks]

    # --- 2. Embeddings + Vectorstore ---
    embedder = get_embedder()
    db = create_vectorstore(texts, embedder)
    retriever = db.as_retriever()

    # --- 3. Run summarizer ---
    summary = run_scorer(gemini_llm, chunks)

    print("\n===== SUMMARY =====\n")
    print(summary)
