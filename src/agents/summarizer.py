# # src/agents/summarizer_agent.py
# from src.llm_wrapper import gemini_llm
# import json
# from src.prompts import SUMMARY_PROMPT

# def run_summarizer_extended(retriever_fn, query="Provide a structured summary of this grant proposal"):
#     """
#     Fetch chunks via retriever_fn and return structured summary JSON with:
#     - pages
#     - references
#     - notes
#     """

#     retrieved_docs = retriever_fn(query)

#     if not retrieved_docs:
#         return {}

#     # Combine text with page numbers for LLM
#     context_text = ""
#     for doc in retrieved_docs:
#         page_num = doc.get("page_number", "Unknown")
#         text = doc.get("text", "")
#         source = doc.get("source", "Unknown")
#         context_text += f"[Page {page_num} | Source: {source}]\n{text}\n\n"

#     # Prompt LLM
#     prompt = SUMMARY_PROMPT.format(context=context_text)
#     response = gemini_llm(prompt)

#     # Parse JSON safely
#     try:
#         summary_json = json.loads(response)
#     except json.JSONDecodeError:
#         # If LLM fails to give valid JSON, return raw response for inspection
#         summary_json = {"raw_response": response}

#     print("=== LLM Raw Response ===")
#     print(response)
#     return summary_json

# src/agents/summarizer_agent.py
from src.llm_wrapper import gemini_llm
import json
import re
from src.prompts import SUMMARY_PROMPT

# Define all key grant sections
GRANT_SECTIONS = [
    "CoverLetter",
    "Objectives",
    "Methodology",
    "EvaluationPlan",
    "ExpectedOutcomes",
    "Budget",
    "Feasibility",
    "Innovation",
    "Sustainability",
    "LettersOfSupport"
]

def strip_codeblock(text: str) -> str:
    """
    Remove Markdown-style code block wrappers (```json ... ```) if present.
    """
    return re.sub(r"^```(?:json)?\n|```$", "", text.strip(), flags=re.MULTILINE)

def run_summarizer_extended(retriever_fn):
    """
    Fetch chunks via retriever_fn for each grant section and return
    a complete structured summary JSON with:
    - text
    - pages
    - references
    - notes
    """
    context_text = ""
    
    # Retrieve chunks for each section individually
    for section in GRANT_SECTIONS:
        docs = retriever_fn(f"Find the {section} section of this grant proposal, including metrics, responsibilities, and relevant details")
        if not docs:
            continue
        for doc in docs:
            page_num = doc.get("page_number", "Unknown")
            text = doc.get("text", "")
            source = doc.get("source", "Unknown")
            context_text += f"[Page {page_num} | Source: {source} | Section: {section}]\n{text}\n\n"

    if not context_text:
        return {}

    # Prepare full prompt
    prompt = SUMMARY_PROMPT.format(context=context_text)

    # Call Gemini LLM
    response = gemini_llm(prompt)

    # Strip code block if present
    clean_response = strip_codeblock(response)

    # Parse JSON safely
    try:
        summary_json = json.loads(clean_response)
    except json.JSONDecodeError:
        summary_json = {"raw_response": response}

    return summary_json