from langchain.prompts import PromptTemplate

# src/prompts.py

# src/prompts.py

SUMMARY_PROMPT = """
You are an expert grant reviewer. Summarize the following grant proposal strictly in JSON.
Include the following sections: Objectives, Methodology, ExpectedOutcomes, Innovation, Feasibility.

Each section should contain:
- "text": concise summary of that section
- "pages": list of page numbers where the information appears
- "references": include page numbers and sources for cited information
- "notes": brief commentary or confidence about the information

The input text has page numbers and sources in this format: [Page X | Source: filename.pdf]

Context:
{context}

Return **only valid JSON**, no extra text.
"""



SCIENTIFIC_CRITIQUE_PROMPT = """
You are a scientific critique agent. Critique the proposal on novelty, 
methodology, and scientific rigor. Max 150 words.
Summary:
{summary_json}
"""

PRACTICAL_CRITIQUE_PROMPT = """
You are a practical critique agent. Critique the proposal on feasibility, 
resources, and applicability. Max 150 words.
Summary:
{summary_json}
"""

DECISION_PROMPT = """
You are a decision agent. Given the scores, critiques, and budget, 
decide Accept or Reject. Return JSON:
{
  "decision": "Accept/Reject",
  "rationale": "..."
}
"""

CROSSCHECK_PROMPT = """
You are a cross-checking agent. Verify consistency between 
summary, scores, critiques, and budget. 
Return JSON:
{
  "consistent": true/false,
  "issues": ["..."]
}
"""

PDF_FORMAT_PROMPT = """
You are a PDF formatter. Convert the grant evaluation results 
into Markdown with sections, tables, and clear highlights.

Constraints:
- Max 1000 words
- Highlight Accept in green, Reject in red
- Use tables for scores
Inputs:
{all_results}
"""
