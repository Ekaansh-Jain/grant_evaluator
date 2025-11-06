"""
Grant Evaluation Pipeline
Orchestrates the full evaluation process from document loading to final decision.
"""

import sys
import os

# Allow `src/...` imports when executed as script
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.input_agent import input_agent
from src.agents.vectorstore_agent import vectorstore_agent
from src.agents.summarizer import run_summarizer_extended
from src.agents.domain_selection import classify_domain
from src.agents.scoring import run_grant_scoring
from src.config.domain_weights import compute_weighted_score
from src.agents.critique import run_grant_critique
from src.agents.budget_agent import run_budget_agent
from src.agents.decision import run_final_decision_agent
from src.llm_wrapper import set_deterministic_mode


def run_full_evaluation(file_path: str, max_budget: float = 50000):
    """
    Run complete adaptive grant evaluation pipeline.

    Args:
        file_path: Path to the grant proposal file (PDF/DOCX)
        max_budget: Maximum allowed requested budget

    Returns:
        dict: structured evaluation result for frontend
    """

    # Make evaluation deterministic to remove LLM randomness
    try:
        set_deterministic_mode(True)
    except:
        pass

    # Step 1 — Extract text pages
    print(f"[INFO] Loading document: {file_path}")
    pages = input_agent(file_path)
    if not pages:
        raise ValueError("Document extraction failed.")
    print(f"[INFO] Loaded {len(pages)} pages")

    # Step 2 — Build vectorstore fresh each run (avoid cross-proposal contamination)
    print("[INFO] Creating in-memory vectorstore...")
    vs = vectorstore_agent(pages, persist_dir=None)

    # Step 3 — Structured summarization (section-wise)
    print("[INFO] Generating structured summary...")
    summary = run_summarizer_extended(vs["ask"])

    # Step 4 — Domain classification
    print("[INFO] Detecting academic / research domain...")
    domain = classify_domain(" ".join([p.page_content for p in pages]))
    print(f"[INFO] Domain Detected → {domain}")

    # Step 5 — Scoring (raw, before weighting)
    print("[INFO] Running scoring agent...")
    scores = run_grant_scoring(summary, domain)

    # Step 6 — Apply adaptive weighting model
    print("[INFO] Computing weighted score...")
    final_weighted_score = compute_weighted_score(scores["scores"], domain)
    print(f"[INFO] Weighted Score = {final_weighted_score}")

    # Step 7 — Critique (uses scoring, does NOT modify score)
    print("[INFO] Generating critique...")
    critique = run_grant_critique(
        scorer_json=scores,
        summaries_json=summary,
        domain=domain
    )

    # Step 8 — Budget analysis
    print("[INFO] Evaluating budget...")
    budget_input = {
        "text": summary.get("Budget", {}).get("text", ""),
        "notes": summary.get("Budget", {}).get("notes", ""),
        "references": summary.get("Budget", {}).get("references", []),
        "score": scores.get("scores", {}).get("Budget", {}).get("score", 0),
        "summary": scores.get("scores", {}).get("Budget", {}).get("summary", ""),
        "strengths": scores.get("scores", {}).get("Budget", {}).get("strengths", []),
        "weaknesses": scores.get("scores", {}).get("Budget", {}).get("weaknesses", [])
    }

    budget_evaluation = run_budget_agent(
        budget_input,
        max_budget=max_budget,
        domain=domain
    )

    # Step 9 — Final decision (uses weighted score, does NOT recalc score)
    print("[INFO] Finalizing decision...")
    final_decision = run_final_decision_agent(
        summary_json=summary,
        scores_json=scores,
        critique_json=critique,
        budget_json=budget_evaluation,
        final_weighted_score=final_weighted_score,
        domain=domain
    )

    # Done — format into frontend-ready shape
    return format_evaluation_response(
        summary, scores, critique, budget_evaluation, final_decision, final_weighted_score
    )


def format_evaluation_response(summary, scores, critique, budget_eval, decision, final_weighted_score):
    """
    Convert internal evaluation results to a frontend-compatible output format.
    """

    section_scores = []
    score_details = []

    for section_name, section_data in scores.get("scores", {}).items():
        section_scores.append({
            "section": section_name,
            "score": section_data.get("score", 0)
        })
        score_details.append({
            "category": section_name,
            "score": section_data.get("score", 0),
            "maxScore": 10,
            "strengths": section_data.get("strengths", []),
            "weaknesses": section_data.get("weaknesses", [])
        })

    return {
        "decision": decision.get("decision", "CONDITIONALLY ACCEPT"),
        "overall_score": final_weighted_score,
        "scores": score_details,
        "full_critique": critique,
        "budget_analysis": budget_eval,
        "section_scores": section_scores
    }
