# src/agents/summarizer_agent.py
from src.llm_wrapper import gemini_llm
import json

# You will define SUMMARY_PROMPT separately (see below)
from src.prompts import SUMMARY_PROMPT

def run_summarizer_extended(retriever_fn, query="Provide a structured summary of this grant proposal"):
    """
    Fetch chunks via retriever_fn and return structured summary JSON with:
    - pages
    - references
    - notes
    """

    retrieved_docs = retriever_fn(query)

    if not retrieved_docs:
        return {
            key: {"text": "Not provided", "pages": [], "references": [], "notes": "No content found"}
            for key in ["Objectives", "Methodology", "ExpectedOutcomes", "Innovation", "Feasibility"]
        }

    # Combine text with page numbers for LLM
    context_text = ""
    for doc in retrieved_docs:
        page_num = doc.get("page_number", "Unknown")
        text = doc.get("text", "")
        source = doc.get("source", "Unknown")
        context_text += f"[Page {page_num} | Source: {source}]\n{text}\n\n"

    # Prompt LLM
    prompt = SUMMARY_PROMPT.format(context=context_text)
    response = gemini_llm(prompt)

    # Parse JSON safely
    try:
        summary_json = json.loads(response)
    except json.JSONDecodeError:
        # fallback structure if LLM fails
        summary_json = {
            key: {"text": "Not provided", "pages": [], "references": [], "notes": "Failed to parse LLM output"}
            for key in ["Objectives", "Methodology", "ExpectedOutcomes", "Innovation", "Feasibility"]
        }

    # Fill missing metadata if needed
    for key in summary_json.keys():
        # ensure required keys exist
        if "pages" not in summary_json[key]:
            summary_json[key]["pages"] = []
        if "references" not in summary_json[key]:
            summary_json[key]["references"] = []
        if "notes" not in summary_json[key]:
            summary_json[key]["notes"] = "Confidence: High"

    return summary_json
