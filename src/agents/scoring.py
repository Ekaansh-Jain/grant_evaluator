from src.llm_wrapper import gemini_llm
import json
from src.prompts import SCORING_PROMPT
import re

def strip_codeblock(text: str) -> str:
    """
    Remove Markdown-style code block wrappers (```json ... ```) if present.
    """
    return re.sub(r"^```(?:json)?\n|```$", "", text.strip(), flags=re.MULTILINE)


def run_grant_scoring(summary_json):
    """
    Pass a structured grant summary JSON to Gemini LLM and get section-wise scores and overall score.
    """
    # Convert summary to JSON string for the prompt
    grant_json_str = json.dumps(summary_json, indent=2)

    # Prepare full prompt
    prompt = SCORING_PROMPT.format(grant_json=grant_json_str)

    # Call Gemini LLM
    response = gemini_llm(prompt)

    cleaned_response = strip_codeblock(response)

    # Parse JSON safely
    try:
        scores_json = json.loads(cleaned_response)
    except json.JSONDecodeError:
        # If parsing fails, return raw response
        scores_json = {"raw_response": cleaned_response}

    # print("=== LLM Scoring Response ===")
    # print(response)
    return scores_json


