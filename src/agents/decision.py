def run_decision(scores: dict, critiques: dict, budget: dict):
    """
    Combine scores + critiques + budget to produce Accept/Reject decision.
    """
    overall = scores.get("Overall", 0)
    if overall >= 15 and budget["decision"] == "Accepted":
        decision = "Accepted"
        rationale = "High scores, critiques acceptable, budget within limit"
    else:
        decision = "Rejected"
        rationale = "Scores or budget do not meet criteria"

    return {"decision": decision, "rationale": rationale}
