def run_budget(requested_amount: int, professor_limit: int):
    """
    Input: requested amount + limit
    Output: accepted/rejected amount + notes
    """
    if requested_amount <= professor_limit:
        decision = "Accepted"
        assigned_amount = requested_amount
        notes = "Within limit"
    else:
        decision = "Rejected"
        assigned_amount = 0
        notes = f"Requested amount exceeds limit of {professor_limit}"

    return {"decision": decision, "amount": assigned_amount, "notes": notes}
