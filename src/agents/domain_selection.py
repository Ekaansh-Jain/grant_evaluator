# src/agents/domain_classifier.py

from src.llm_wrapper import gemini_llm
from src.prompts import DOMAIN_CLASSIFIER_PROMPT
import re

def strip_response(text: str) -> str:
    """
    Clean LLM output to extract a simple string domain label.
    """
    text = text.strip()
    text = re.sub(r"```(?:.*)?```", "", text)  # remove accidental codeblocks
    return text.split("\n")[0].strip()  # only keep first non-empty line

def classify_domain(proposal_text: str) -> str:
    """
    Classify proposal into a domain using the LLM.
    """
    prompt = DOMAIN_CLASSIFIER_PROMPT.format(context=proposal_text)
    response = gemini_llm(prompt)

    domain = strip_response(response)

    # Optional: safety fallback if model outputs garbage
    allowed_domains = [
        "AI / Computer Science",
        "Biotechnology / Life Sciences",
        "Healthcare / Medicine",
        "Education / Learning Sciences",
        "Environment / Climate / Sustainability",
        "Social Sciences / Policy",
        "Agriculture / Food Systems"
    ]

    if domain not in allowed_domains:
        domain = "Social Sciences / Policy"  # default safest domain

    return domain
