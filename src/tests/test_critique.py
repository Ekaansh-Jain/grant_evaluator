from src.agents.input_agent import input_agent
from src.agents.vectorstore_agent import vectorstore_agent
from src.agents.summarizer import run_summarizer_extended
from src.agents.scoring import run_grant_scoring
from src.agents.critique import run_grant_critique
import json

# === Configuration ===
SAMPLE_FILE = "/Users/ekaanshjain/Desktop/ocjs_sample_grant.pdf"

# === Step 1: Load document ===
pages = input_agent(SAMPLE_FILE)

# === Step 2: Create vectorstore and retriever ===
vs = vectorstore_agent(pages)

# === Step 3: Generate structured summary ===
summary = run_summarizer_extended(vs["ask"])

# === Step 4: Run scoring agent ===
scores = run_grant_scoring(summary)

# === Step 5: Run critique agent ===
critique = run_grant_critique(scorer_json=scores, summaries_json=summary)

# === Step 6: Display output ===
print("\n=== CRITIQUE AGENT OUTPUT ===\n")
print(json.dumps(critique, indent=2))
