from src.agents.input_agent import input_agent
from src.agents.vectorstore_agent import vectorstore_agent
from src.agents.summarizer import run_summarizer_extended
import json

SAMPLE_FILE = "/Users/ekaanshjain/Desktop/ocjs_sample_grant.pdf"

# Load document
pages = input_agent(SAMPLE_FILE)

# Create vectorstore and retriever
vs = vectorstore_agent(pages)

# Generate structured summary
summary = run_summarizer_extended(vs["ask"])
print(json.dumps(summary, indent=2))

# Debug: inspect what vectorstore is returning
retrieved_docs = vs["ask"]("Objectives of the proposal")
for i, doc in enumerate(retrieved_docs):
    print(f"--- Doc {i+1} ---")
    print("Page Number:", doc["page_number"])
    print("Source:", doc["source"])
    print("Text preview:", doc["text"][:1000])  # first 300 chars
    print()

