import json
from typing import Dict, Any
from src.llm_wrapper import gemini_llm
from src.prompts import SCORING_PROMPT

def calculate_research_impact(summary: Dict[str, Any]) -> tuple[float, str]:
    """Calculate score for research impact (0-25 points)"""
    score = 0
    feedback = []
    
    objectives = summary.get("Objectives", {})
    outcomes = summary.get("ExpectedOutcomes", {})
    
    # Score based on clarity of objectives (0-10)
    if objectives.get("text"):
        score += min(10, len(objectives["text"].split()) / 10)
        feedback.append("Clear objectives defined")
    
    # Score based on potential impact (0-15)
    if outcomes.get("text"):
        impact_words = ['impact', 'advance', 'improve', 'novel', 'breakthrough']
        impact_score = sum(1 for word in impact_words if word.lower() in outcomes["text"].lower())
        score += min(15, impact_score * 3)
        feedback.append(f"Impact potential: {impact_score * 3}/15")
    
    return min(25, score), "; ".join(feedback)

def calculate_methodology_score(summary: Dict[str, Any]) -> tuple[float, str]:
    """Calculate score for methodology (0-25 points)"""
    score = 0
    feedback = []
    
    methodology = summary.get("Methodology", {})
    
    if methodology.get("text"):
        # Score for methodology completeness (0-15)
        words = len(methodology["text"].split())
        score += min(15, words / 20)
        feedback.append(f"Methodology detail: {min(15, words / 20)}/15")
        
        # Score for scientific rigor (0-10)
        rigor_terms = ['control', 'replicate', 'validate', 'analyze', 'measure']
        rigor_score = sum(2 for term in rigor_terms if term.lower() in methodology["text"].lower())
        score += min(10, rigor_score)
        feedback.append(f"Scientific rigor: {min(10, rigor_score)}/10")
    
    return min(25, score), "; ".join(feedback)

def calculate_innovation_score(summary: Dict[str, Any]) -> tuple[float, str]:
    """Calculate score for innovation (0-20 points)"""
    score = 0
    feedback = []
    
    innovation = summary.get("Innovation", {})
    
    if innovation.get("text"):
        # Score for novelty (0-12)
        novelty_terms = ['novel', 'innovative', 'unique', 'breakthrough', 'original']
        novelty_score = sum(2.4 for term in novelty_terms if term.lower() in innovation["text"].lower())
        score += min(12, novelty_score)
        feedback.append(f"Novelty: {min(12, novelty_score)}/12")
        
        # Score for advancement over state-of-the-art (0-8)
        advance_terms = ['improve', 'advance', 'beyond', 'current', 'existing']
        advance_score = sum(1.6 for term in advance_terms if term.lower() in innovation["text"].lower())
        score += min(8, advance_score)
        feedback.append(f"Advancement: {min(8, advance_score)}/8")
    
    return min(20, score), "; ".join(feedback)

def calculate_feasibility_score(summary: Dict[str, Any]) -> tuple[float, str]:
    """Calculate score for feasibility (0-20 points)"""
    score = 0
    feedback = []
    
    feasibility = summary.get("Feasibility", {})
    methodology = summary.get("Methodology", {})
    
    if feasibility.get("text"):
        # Score for resource assessment (0-10)
        resource_terms = ['resources', 'equipment', 'facility', 'team', 'expertise']
        resource_score = sum(2 for term in resource_terms if term.lower() in feasibility["text"].lower())
        score += min(10, resource_score)
        feedback.append(f"Resources: {min(10, resource_score)}/10")
        
    if methodology.get("text"):
        # Score for timeline and planning (0-10)
        planning_terms = ['timeline', 'schedule', 'plan', 'phase', 'milestone']
        planning_score = sum(2 for term in planning_terms if term.lower() in methodology["text"].lower())
        score += min(10, planning_score)
        feedback.append(f"Planning: {min(10, planning_score)}/10")
    
    return min(20, score), "; ".join(feedback)

def calculate_budget_score(summary: Dict[str, Any]) -> tuple[float, str]:
    """Calculate score for budget justification (0-10 points)"""
    score = 0
    feedback = []
    
    # Look for budget information across all sections
    all_text = " ".join(section.get("text", "") for section in summary.values())
    
    budget_terms = ['budget', 'cost', 'funding', 'expense', 'resource']
    budget_score = sum(2 for term in budget_terms if term.lower() in all_text.lower())
    score = min(10, budget_score)
    feedback.append(f"Budget justification: {score}/10")
    
    return score, "; ".join(feedback)

def run_scorer(summary: str) -> Dict[str, Any]:
    """
    Input: summary JSON (or text)
    Output: Detailed scores with feedback
    
    Scoring Criteria:
    - Research Impact: 25 points
    - Methodology & Approach: 25 points
    - Innovation & Novelty: 20 points
    - Feasibility & Resources: 20 points
    - Budget Justification: 10 points
    """
    if isinstance(summary, str):
        try:
            summary_dict = json.loads(summary)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON input", "total_score": 0}
    else:
        summary_dict = summary
        
    # Calculate individual scores
    impact_score, impact_feedback = calculate_research_impact(summary_dict)
    method_score, method_feedback = calculate_methodology_score(summary_dict)
    innovation_score, innovation_feedback = calculate_innovation_score(summary_dict)
    feasibility_score, feasibility_feedback = calculate_feasibility_score(summary_dict)
    budget_score, budget_feedback = calculate_budget_score(summary_dict)
    
    # Calculate total score
    total_score = sum([impact_score, method_score, innovation_score, 
                      feasibility_score, budget_score])
    
    # Prepare result
    result = {
        "total_score": round(total_score, 2),
        "max_score": 100,
        "categories": {
            "research_impact": {
                "score": round(impact_score, 2),
                "max_score": 25,
                "feedback": impact_feedback
            },
            "methodology": {
                "score": round(method_score, 2),
                "max_score": 25,
                "feedback": method_feedback
            },
            "innovation": {
                "score": round(innovation_score, 2),
                "max_score": 20,
                "feedback": innovation_feedback
            },
            "feasibility": {
                "score": round(feasibility_score, 2),
                "max_score": 20,
                "feedback": feasibility_feedback
            },
            "budget": {
                "score": round(budget_score, 2),
                "max_score": 10,
                "feedback": budget_feedback
            }
        },
        "recommendation": "Strong Accept" if total_score >= 85 else
                         "Accept" if total_score >= 75 else
                         "Borderline" if total_score >= 65 else
                         "Reject"
    }
    
    return result
