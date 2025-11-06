from src.agents.input_agent import input_agent
from src.agents.vectorstore_agent import vectorstore_agent
from src.agents.summarizer import run_summarizer_extended
from src.agents.scoring import run_grant_scoring
from src.agents.domain_selection import classify_domain  # ✅ NEW
import json

SAMPLE_FILE = "/Users/ekaanshjain/Desktop/ocjs_sample_grant.pdf"

# 1. Load document
pages = input_agent(SAMPLE_FILE)

# 2. Create vectorstore and retriever
vs = vectorstore_agent(pages)

# 3. Generate structured summary
summary = run_summarizer_extended(vs["ask"])

# 4. ✅ Detect the proposal's research domain
domain = classify_domain(" ".join([p.page_content for p in pages]))
print(f"\n🔍 Detected Domain: {domain}\n")

# 5. ✅ Run scoring with domain-awareness
scores = run_grant_scoring(summary, domain)

print("\n📊 Raw Section Scores (before weighting):\n")
print(json.dumps(scores, indent=2))
