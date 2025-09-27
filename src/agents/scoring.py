import json
from src.prompts import SCORING_PROMPT
def run_scorer(llm, summary: str):
    """Run scoring on the summary and return a dict."""
    prompt = SCORING_PROMPT.format(summary=summary)
    response = llm(prompt)

    # Try parsing JSON
    try:
        scores = json.loads(response)
    except json.JSONDecodeError:
        # If LLM outputs extra text, fix it
        import re
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            scores = json.loads(match.group(0))
        else:
            raise ValueError("Invalid response format from LLM")

    return scores