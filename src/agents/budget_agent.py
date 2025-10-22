import json
import re
from src.llm_wrapper import gemini_llm  # your LLM wrapper
from src.prompts import BUDGET_PROMPT  # your prompt template


def strip_codeblock(text: str) -> str:
    """
    Remove Markdown-style code block wrappers (```json ... ```) if present.
    """
    return re.sub(r"^```(?:json)?\n|```$", "", text.strip(), flags=re.MULTILINE)


def run_budget_agent(budget_input, max_budget=None):
    """
    Evaluate the Budget section of a grant using LLM.

    Args:
        budget_input (dict): Combined Budget info from summarizer and scorer.
            Expected keys: text, notes, references, score, summary, strengths, weaknesses
        max_budget (float, optional): Maximum allowed budget to flag overages.

    Returns:
        dict: LLM output with budget_score, budget_summary, flags, recommendations
    """
    # Convert input to JSON string
    budget_json_str = json.dumps(budget_input, indent=2)

    # Prepare prompt
    prompt = BUDGET_PROMPT.format(budget_json=budget_json_str, max_budget=max_budget or "N/A")

    # Call LLM
    response = gemini_llm(prompt)

    cleaned_response = strip_codeblock(response)

    # Parse JSON safely
    try:
        budget_result = json.loads(cleaned_response)
    except json.JSONDecodeError:
        budget_result = {"raw_response": cleaned_response}

    return budget_result
