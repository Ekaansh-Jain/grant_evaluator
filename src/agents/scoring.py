import json
from src.llm_wrapper import gemini_llm
from src.prompts import SCORING_PROMPT

def run_scorer(summary: str):
    """
    Input: summary JSON (or text)
    Output: JSON scores
    """
    prompt = SCORING_PROMPT.format(summary=summary)
    response = gemini_llm(prompt)
    
    try:
        scores = json.loads(response)
    except json.JSONDecodeError:
        import re
        match = re.search(r"\{.*\}", response, re.DOTALL)
        scores = json.loads(match.group(0)) if match else {}
    
    return scores
