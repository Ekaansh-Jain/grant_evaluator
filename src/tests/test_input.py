import os
from src.agents.input_agent import input_agent
from src.agents.vectorstore_agent import vectorstore_agent

def test_input_and_vectorstore():
    sample_path = "/Users/ekaanshjain/Desktop/ocjs_sample_grant.pdf"  # update path

    # 1. Test Input Agent
    data = input_agent(sample_path)
    pages = data["pages"]
    print(f"Loaded {len(pages)} pages from {sample_path}")
    print("First page preview:", pages[0].page_content[:200], "...\n")

    # 2. Test Vectorstore Agent
    db, ask = vectorstore_agent(pages)

    # Example retrieval
    query = "Summary of proposal"
    results = ask(query)
    print(f"Retrieved {len(results)} docs for query: '{query}'")

    for i, r in enumerate(results[:2], 1):  # print top 2 results
        print(f"\n--- Result {i} ---\n{r.page_content[:300]}...\n")

if __name__ == "__main__":
    test_input_and_vectorstore()
