from loaders import load_pdf
from preprocessing import split_docs
from embeddings import get_embedder
from vectorstore import create_vectorstore

# 1. Load
docs = load_pdf("/Users/ekaanshjain/Desktop/proof_resources_grant1.pdf")

# 2. Split
chunks = split_docs(docs)

# 3. Embed
embedder = get_embedder()
texts = [c.page_content for c in chunks]

# Use embed_documents instead of encode
# Chroma can accept the embedder object directly
db = create_vectorstore(texts, embedder)

# 4. Test retrieval
results = db.similarity_search("What is the main goal of this document?", k=2)
for r in results:
    print(r.page_content[:300])