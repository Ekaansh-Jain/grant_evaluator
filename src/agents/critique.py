from src.llm_wrapper import gemini_llm
import json
import re
from src.prompts import MASTER_CRITIQUE_PROMPT


def strip_codeblock(text: str) -> str:
    """
    Remove Markdown-style code block wrappers (```json ... ```) if present.
    """
    return re.sub(r"^```(?:json)?\n|```$", "", text.strip(), flags=re.MULTILINE)


def run_grant_critique(scorer_json, summaries_json=None):
    """
    Pass the Scorer Agent's JSON output (and optionally Summary Agent output)
    to Gemini LLM for a comprehensive multi-domain critique.
    
    This Master Critique Agent evaluates the grant across seven lenses:
      1. Scientific Rigor
      2. Practical Feasibility
      3. Language & Clarity
      4. Context & Alignment
      5. Persuasiveness
      6. Ethics & Inclusivity
      7. Innovation & Impact

    Parameters
    ----------
    scorer_json : dict
        The structured output from the Scorer Agent, including scores, strengths, and weaknesses.
    summaries_json : dict, optional
        The structured summaries from the Summary Agent for deeper context.

    Returns
    -------
    dict
        A structured critique JSON with identified issues, recommendations, and top priorities.
    """

    # Combine inputs into a single structured payload
    combined_input = {
        "summaries": summaries_json if summaries_json else {},
        "scorer_output": scorer_json,
    }

    # Convert to string for prompt formatting
    input_json_str = json.dumps(combined_input, indent=2)

    # Prepare the full prompt
    prompt = MASTER_CRITIQUE_PROMPT.format(input_json=input_json_str)

    # Call Gemini LLM
    response = gemini_llm(prompt)

    # Clean Markdown wrappers
    cleaned_response = strip_codeblock(response)

    # Parse safely to JSON
    try:
        critique_json = json.loads(cleaned_response)
    except json.JSONDecodeError:
        critique_json = {"error": "Invalid JSON output", "raw_response": cleaned_response}

    return critique_json
