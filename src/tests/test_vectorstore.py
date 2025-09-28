from src.agents.input_agent import input_agent
from src.agents.vectorstore_agent import vectorstore_agent
import json

SAMPLE_FILE = "/Users/ekaanshjain/Desktop/ocjs_sample_grant.pdf"

# 1️⃣ Load PDF into Document objects
pages = input_agent(SAMPLE_FILE)
print(f"Loaded {len(pages)} pages.")
print("First page preview:", pages[0].page_content[:200], "...\n")
print("Metadata for first page:", pages[0].metadata)

# 2️⃣ Create vectorstore + retriever
vs = vectorstore_agent(pages)

# 3️⃣ Test retrieval
query = "Objectives of the proposal"
retrieved_docs = vs["ask"](query)

print(f"Retrieved {len(retrieved_docs)} documents for query: '{query}'\n")
for i, doc in enumerate(retrieved_docs, 1):
    print(f"--- Result {i} ---")
    print(f"Page Number: {doc['page_number']}, Source: {doc['source']}")
    print(doc["text"][:300], "...\n")  # Show first 300 chars
