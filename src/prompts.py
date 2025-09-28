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

SCORING_PROMPT = """
You are an expert grant evaluator. Score this grant proposal based on the provided summary.
Evaluate the following criteria:

1. Research Impact (25 points):
   - Clarity and significance of objectives
   - Potential impact on the field
   
2. Methodology & Approach (25 points):
   - Soundness of methodology
   - Scientific rigor
   
3. Innovation & Novelty (20 points):
   - Originality of approach
   - Advancement over state-of-the-art
   
4. Feasibility & Resources (20 points):
   - Resource availability
   - Timeline and planning
   
5. Budget Justification (10 points):
   - Clear and reasonable budget allocation

Summary to evaluate:
{summary}

Return a JSON object with scores and feedback for each category.
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
