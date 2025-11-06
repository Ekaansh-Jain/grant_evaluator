from src.llm_wrapper import gemini_llm
import json
from src.prompts import SCORING_PROMPT
import re

def strip_codeblock(text: str) -> str:
    """
    Remove Markdown-style code block wrappers (```json ... ```) if present.
    """
    return re.sub(r"^```(?:json)?\n|```$", "", text.strip(), flags=re.MULTILINE)


def run_grant_scoring(summary_json, domain: str):
    """
    Pass a structured grant summary JSON to Gemini LLM and get section-wise scores.
    NOTE: These scores are *raw* — adaptive weighting happens later in backend.
    """
    # Convert summary to JSON string for the prompt
    grant_json_str = json.dumps(summary_json, indent=2)

    # Prepare full prompt WITH DOMAIN CONTEXT
    prompt = SCORING_PROMPT.format(grant_json=grant_json_str, domain=domain)

    # Call Gemini LLM
    response = gemini_llm(prompt)

    cleaned_response = strip_codeblock(response)

    # Parse JSON safely
    try:
        scores_json = json.loads(cleaned_response)
    except json.JSONDecodeError:
        # If parsing fails, return raw response
        scores_json = {"raw_response": cleaned_response}

    return scores_json


from src.config.domain_weights import DOMAIN_WEIGHTS

def compute_weighted_score(section_scores: dict, domain: str) -> float:
    weights = DOMAIN_WEIGHTS.get(domain)
    if not weights:
        raise ValueError(f"No weight configuration found for domain: {domain}")

    score = 0
    for section, data in section_scores.items():
        if section in weights:
            score += data["score"] * weights[section]

    return round(score, 2)
