# src/agents/summarizer_agent.py
from src.llm_wrapper import gemini_llm
import json
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
        return {}

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
        # If LLM fails to give valid JSON, return raw response for inspection
        summary_json = {"raw_response": response}

    print("=== LLM Raw Response ===")
    print(response)
    return summary_json
