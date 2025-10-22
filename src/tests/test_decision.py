from src.agents.input_agent import input_agent
from src.agents.vectorstore_agent import vectorstore_agent
from src.agents.summarizer import run_summarizer_extended
from src.agents.scoring import run_grant_scoring
from src.agents.critique import run_grant_critique
from src.agents.budget_agent import run_budget_agent
from src.agents.decision import run_final_decision_agent  
import json

# === Configuration ===
SAMPLE_FILE = "/Users/ekaanshjain/Desktop/ocjs_sample_grant.pdf"
MAX_BUDGET = 30000  # Example: max allowed budget

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

# === Step 6: Prepare Budget input from summary and scorer ===
budget_input = {
    "text": summary["Budget"]["text"],
    "notes": summary["Budget"]["notes"],
    "references": summary["Budget"]["references"],
    "score": scores["scores"]["Budget"]["score"],
    "summary": scores["scores"]["Budget"]["summary"],
    "strengths": scores["scores"]["Budget"]["strengths"],
    "weaknesses": scores["scores"]["Budget"]["weaknesses"]
}

# === Step 7: Run Budget Agent ===
budget_evaluation = run_budget_agent(budget_input, max_budget=MAX_BUDGET)

# === Step 8: Run Final Decision Agent ===
final_decision = run_final_decision_agent(
    summary_json=summary,
    scores_json=scores,
    critique_json=critique,
    budget_json=budget_evaluation
)

# === Step 9: Display outputs ===
# print("\n=== SUMMARY ===\n")
# print(json.dumps(summary, indent=2))

# print("\n=== SCORER OUTPUT ===\n")
# print(json.dumps(scores, indent=2))

# print("\n=== CRITIQUE AGENT OUTPUT ===\n")
# print(json.dumps(critique, indent=2))

# print("\n=== BUDGET AGENT OUTPUT ===\n")
# print(json.dumps(budget_evaluation, indent=2))

print("\n=== FINAL DECISION AGENT OUTPUT ===\n")
print(json.dumps(final_decision, indent=2))
