"""
Grant Evaluation Pipeline
Orchestrates the full evaluation process from document loading to final decision
"""

import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.input_agent import input_agent
from src.agents.vectorstore_agent import vectorstore_agent
from src.agents.summarizer import run_summarizer_extended
from src.agents.scoring import run_grant_scoring
from src.agents.critique import run_grant_critique
from src.agents.budget_agent import run_budget_agent
from src.agents.decision import run_final_decision_agent
import json
from src.llm_wrapper import set_deterministic_mode


def run_full_evaluation(file_path: str, max_budget: float = 50000):
    """
    Run complete grant evaluation pipeline with clean slate for each evaluation.
    
    Args:
        file_path: Path to the grant proposal file (PDF/DOCX)
        max_budget: Maximum allowed budget
        
    Returns:
        dict: Formatted evaluation results matching frontend expectations
    """
    
    # Force deterministic LLM behavior for this evaluation run (avoid sampling noise)
    try:
        set_deterministic_mode(True)
    except Exception:
        pass
    
    # Step 1: Load document
    print(f"[INFO] Loading document: {file_path}")
    pages = input_agent(file_path)
    if not pages:
        raise ValueError(f"No content extracted from {file_path}. The file may be empty or corrupted.")
    print(f"[INFO] Loaded {len(pages)} pages")
    
    # Step 2: Create vectorstore and retriever with NO PERSISTENCE
    # This ensures each evaluation starts with a clean slate, preventing context contamination
    print(f"[INFO] Creating fresh in-memory vectorstore (no persistence)...")
    vs = vectorstore_agent(pages, persist_dir=None)  # <-- IN-MEMORY MODE: no contamination
    
    # Step 3: Generate structured summary
    print(f"[INFO] Generating summary...")
    summary = run_summarizer_extended(vs["ask"])
    
    # Step 4: Run scoring agent
    scores = run_grant_scoring(summary)
    
    # Step 5: Run critique agent
    critique = run_grant_critique(scorer_json=scores, summaries_json=summary)
    
    # Step 6: Prepare Budget input from summary and scorer
    budget_input = {
        "text": summary.get("Budget", {}).get("text", ""),
        "notes": summary.get("Budget", {}).get("notes", ""),
        "references": summary.get("Budget", {}).get("references", []),
        "score": scores.get("scores", {}).get("Budget", {}).get("score", 0),
        "summary": scores.get("scores", {}).get("Budget", {}).get("summary", ""),
        "strengths": scores.get("scores", {}).get("Budget", {}).get("strengths", []),
        "weaknesses": scores.get("scores", {}).get("Budget", {}).get("weaknesses", [])
    }
    
    # Step 7: Run Budget Agent
    budget_evaluation = run_budget_agent(budget_input, max_budget=max_budget)
    
    # Step 8: Run Final Decision Agent
    final_decision = run_final_decision_agent(
        summary_json=summary,
        scores_json=scores,
        critique_json=critique,
        budget_json=budget_evaluation
    )
    
    # Cleanup: Explicitly delete vectorstore to free memory
    # (In-memory vectorstore will be garbage collected, but this makes cleanup explicit)
    try:
        del vs
    except:
        pass
    
    # Transform outputs to match frontend expectations
    return format_evaluation_response(
        summary, scores, critique, budget_evaluation, final_decision
    )


def format_evaluation_response(summary, scores, critique, budget_eval, decision):
    """
    Format pipeline outputs to match frontend TypeScript interface
    """
    
    # Extract section scores from scores JSON
    section_scores = []
    score_details = []
    
    sections = scores.get("scores", {})
    for section_name, section_data in sections.items():
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
    
    # Extract critique domains (7 domains from critique agent)
    critique_domains = []
    domain_mapping = {
        "scientific_critique": "Scientific Rigor",
        "practical_critique": "Practical Feasibility",
        "language_critique": "Language & Clarity",
        "context_critique": "Context & Alignment",
        "persuasiveness_critique": "Persuasiveness",
        "ethical_critique": "Ethics & Inclusivity",
        "innovation_critique": "Innovation & Impact"
    }
    
    for key, label in domain_mapping.items():
        if key in critique:
            # Estimate score based on issue count (simplified)
            issues = critique[key].get("issues", [])
            recommendations = critique[key].get("recommendations", [])
            # Score: 10 - (issue_count * 1.5) but clamped to 0-10
            estimated_score = max(0, min(10, 10 - len(issues) * 1.5))
            critique_domains.append({
                "domain": label,
                "score": int(estimated_score)
            })
    
    # Format full critique
    all_issues = []
    all_recommendations = []
    
    for key in domain_mapping.keys():
        if key in critique:
            for issue in critique[key].get("issues", []):
                all_issues.append({
                    "severity": "high" if "critical" in issue.lower() or "serious" in issue.lower() else "medium",
                    "category": domain_mapping[key],
                    "description": issue
                })
            
            for rec in critique[key].get("recommendations", []):
                all_recommendations.append({
                    "priority": "high" if any(word in rec.lower() for word in ["must", "critical", "essential"]) else "medium",
                    "recommendation": rec
                })
    
    full_critique = {
        "summary": critique.get("overall_feedback", "Comprehensive evaluation completed."),
        "issues": all_issues[:10],  # Limit to top 10
        "recommendations": all_recommendations[:10]  # Limit to top 10
    }
    
    # Format budget analysis
    budget_breakdown = []
    # Parse budget from summary if available
    budget_text = summary.get("Budget", {}).get("text", "")
    total_budget = budget_eval.get("budget_score", 0) * 5000  # Estimate based on score
    
    # Default budget categories
    default_categories = [
        {"category": "Personnel", "percentage": 40},
        {"category": "Equipment", "percentage": 20},
        {"category": "Travel", "percentage": 10},
        {"category": "Supplies", "percentage": 15},
        {"category": "Indirect Costs", "percentage": 15}
    ]
    
    for cat in default_categories:
        budget_breakdown.append({
            "category": cat["category"],
            "amount": total_budget * (cat["percentage"] / 100),
            "percentage": cat["percentage"]
        })
    
    budget_flags = []
    for flag_msg in budget_eval.get("budget_flags", []):
        flag_type = "error" if "over budget" in flag_msg.lower() else "warning" if "missing" in flag_msg.lower() else "info"
        budget_flags.append({
            "type": flag_type,
            "message": flag_msg
        })
    
    budget_analysis = {
        "totalBudget": total_budget,
        "breakdown": budget_breakdown,
        "flags": budget_flags,
        "summary": budget_eval.get("budget_summary", "Budget reviewed and analyzed.")
    }
    
    # Final response
    return {
        "decision": decision.get("decision", "REVISE"),
        "overall_score": decision.get("final_score", scores.get("overall_score", 7.0)),
        "scores": score_details,
        "critique_domains": critique_domains,
        "section_scores": section_scores,
        "full_critique": full_critique,
        "budget_analysis": budget_analysis
    }
