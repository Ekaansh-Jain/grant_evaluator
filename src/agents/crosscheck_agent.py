from src.llm_wrapper import gemini_llm
from src.prompts import CROSSCHECK_PROMPT

def run_crosscheck(summary: str, scores: dict, critiques: dict, budget: dict, retriever):
    """
    Use AI to verify consistency and hallucinations.
    
    Args:
        summary: structured summary from Summary Agent
        scores: JSON from Scoring Agent
        critiques: dict with 'practical' and 'scientific'
        budget: dict from Budget Agent
        retriever: retriever from Vectorstore Agent to fetch relevant docs
    
    Returns:
        dict: consistent (bool), issues (list)
    """
    # Fetch top relevant docs again
    query = "Verify the grant proposal content"
    docs = retriever.get_relevant_documents(query)
    context_text = "\n\n".join([d.page_content for d in docs])

    # Build prompt for LLM to verify outputs
    prompt = CROSSCHECK_PROMPT.format(
        context=context_text,
        summary=summary,
        scores=scores,
        practical_critiques=critiques.get("practical", ""),
        scientific_critiques=critiques.get("scientific", ""),
        budget=budget
    )

    response = gemini_llm(prompt)
    # LLM should return JSON: {"consistent": bool, "issues": [str, ...]}
    import json
    try:
        result = json.loads(response)
    except:
        # Fallback if LLM outputs extra text
        import re
        match = re.search(r"\{.*\}", response, re.DOTALL)
        result = json.loads(match.group(0)) if match else {"consistent": False, "issues": ["Invalid LLM response"]}
    
    return result
