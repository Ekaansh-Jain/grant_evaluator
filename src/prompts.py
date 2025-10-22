from langchain.prompts import PromptTemplate

# src/prompts.py

# src/prompts.py

# SUMMARY_PROMPT = """
# You are an expert grant reviewer. Summarize the following grant proposal strictly in JSON.
# Include the following sections: Objectives, Methodology, ExpectedOutcomes, Innovation, Feasibility.

# Each section should contain:
# - "text": concise summary of that section
# - "pages": list of page numbers where the information appears
# - "references": include page numbers and sources for cited information
# - "notes": brief commentary or confidence about the information

# The input text has page numbers and sources in this format: [Page X | Source: filename.pdf]

# Context:
# {context}

# Return **only valid JSON**, no extra text.
# """

SUMMARY_PROMPT = """
You are an expert grant reviewer. Summarize the following grant proposal strictly in JSON.
Include all of the following sections: CoverLetter, Objectives, Methodology, EvaluationPlan, ExpectedOutcomes,
Budget, Feasibility, Innovation, Sustainability, LettersOfSupport.

Each section should contain:
- "text": detailed summary of that section including key actions, metrics, responsibilities, or processes where relevant
- "pages": list of page numbers where the information appears
- "references": exact quotes or key phrases from the pages to support the summary
- "notes": expert commentary, confidence, or observations about missing details

Do not omit any section. If information for a section is missing, explicitly state it.

The input text includes page numbers and sources in this format: [Page X | Source: filename.pdf]

Context:
{context}
"""

# Scoring prompt template
SCORING_PROMPT = """
You are an expert grant evaluator. You are given a structured summary of a grant proposal in JSON format.

Your task is to evaluate the quality of each section objectively and produce **strictly structured JSON output** suitable for downstream automated analysis.

### SCORING INSTRUCTIONS
1. **Rate each section from 0 to 10**
   - 0 = Missing or irrelevant
   - 5 = Acceptable but incomplete or vague
   - 10 = Exceptional, clear, and well-supported
2. **Be strict but fair.**
   - Penalize missing data, weak justification, vague language, or lack of evidence.
   - Reward specificity, measurable goals, innovation, and clear alignment with the proposal’s aims.
3. **Provide concise reasoning in each section’s fields:**
   - `summary`: One line summarizing the section’s effectiveness.
   - `strengths`: List of 1–3 short bullet points describing what is done well.
   - `weaknesses`: List of 1–3 short bullet points describing what is missing or weak.
   - `score`: Integer 0–10 (no decimals).
4. **Provide an `overall_score` (0–10)** reflecting the weighted average performance across all sections.
5. **Tone:** Use concise, analytical, and professional language. Avoid polite or vague wording (e.g., no "would be improved by" — use "missing", "unclear", "incomplete").

### INPUT
Input JSON (the structured proposal summary):
{grant_json}

### OUTPUT FORMAT (STRICTLY JSON)
{{
  "scores": {{
    "CoverLetter": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }},
    "Objectives": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }},
    "Methodology": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }},
    "EvaluationPlan": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }},
    "ExpectedOutcomes": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }},
    "Budget": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }},
    "Feasibility": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }},
    "Innovation": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }},
    "Sustainability": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }},
    "LettersOfSupport": {{
      "score": int,
      "summary": str,
      "strengths": [str, ...],
      "weaknesses": [str, ...]
    }}
  }},
  "overall_summary": str,
  "overall_score": int
}}
Scoring Guidance:
- 10 = Exceptional and flawless (meets all professional grant standards; only stylistic improvements possible)
- 8–9 = Strong and well-justified with minor refinements suggested
- 6–7 = Adequate but missing key justifications or clarity
- 4–5 = Weak, with significant issues in structure, justification, or realism
- 0–3 = Unacceptable or non-compliant budget
Use the full range honestly. Do not give high scores unless the budget is genuinely exemplary.

"""
MASTER_CRITIQUE_PROMPT = """
You are a master grant reviewer.

You are provided with:
1. The structured summaries of each section (optional, may be None).
2. The scored evaluation (including scores, strengths, and weaknesses) from the Scorer Agent.

Your task is to produce a *comprehensive, professional critique* across seven review domains:

1. **Scientific Rigor** – accuracy, research quality, evaluation design.
2. **Practical Feasibility** – real-world viability, funding realism, operational soundness.
3. **Language & Clarity** – grammar, readability, conciseness, tone.
4. **Context & Alignment** – logical consistency between sections, coherence of goals.
5. **Persuasiveness** – strength of justification, urgency, credibility.
6. **Ethics & Inclusivity** – fairness, transparency, and ethical research design.
7. **Innovation & Impact** – originality, creativity, scalability, and potential impact.

### Important Instructions:
- Be detailed but concise in critiques.
- For each domain, include 2–5 key issues and 2–5 recommendations.
- End with a "priority_focus" (top 3 areas that most need improvement) and a single "overall_feedback" paragraph.

### INPUT JSON
{input_json}

### OUTPUT FORMAT (STRICT JSON)
{{
  "scientific_critique": {{
    "issues": [str, ...],
    "recommendations": [str, ...]
  }},
  "practical_critique": {{
    "issues": [str, ...],
    "recommendations": [str, ...]
  }},
  "language_critique": {{
    "issues": [str, ...],
    "recommendations": [str, ...]
  }},
  "context_critique": {{
    "issues": [str, ...],
    "recommendations": [str, ...]
  }},
  "persuasiveness_critique": {{
    "issues": [str, ...],
    "recommendations": [str, ...]
  }},
  "ethical_critique": {{
    "issues": [str, ...],
    "recommendations": [str, ...]
  }},
  "innovation_critique": {{
    "issues": [str, ...],
    "recommendations": [str, ...]
  }},
  "priority_focus": [str, ...],
  "overall_feedback": str
}}
"""

BUDGET_PROMPT = """
You are a Grant Budget Analyst. Evaluate the following Budget section of a grant proposal. 
The input includes the original text, notes, references, and the scorer's evaluation (score, summary, strengths, weaknesses).

Budget JSON:
{budget_json}

Maximum allowed budget: {max_budget}

Your task:
1. Review the budget carefully for accuracy, completeness, and fiscal soundness.
2. Identify any issues, risks, or missing justifications, including unclear calculations or unsupported line items.
3. Check if the total requested exceeds the max_budget and flag it if so.
4. Assess whether the budget aligns with standard grant budgeting practices (e.g., fringe rates, indirect costs, contingencies).
5. Suggest **constructive, actionable recommendations** — even for high-quality budgets — that improve clarity, compliance, or real-world feasibility.
6. Produce a final JSON output in the following format:

{{
    "budget_score": 0-10,
    "budget_summary": "Concise, professional summary of budget quality and justification strength.",
    "budget_flags": ["Over budget", "Missing justification", "Inconsistent totals", ...],
    "recommendations": ["Add contingency plan", "Justify consultant fees", "Clarify fringe benefit calculation", ...]
}}

Scoring Guidance:
- 10 = Exceptional and flawless (meets all professional grant standards; only stylistic improvements possible)
- 8–9 = Strong and well-justified with minor refinements suggested
- 6–7 = Adequate but missing key justifications or clarity
- 4–5 = Weak, with significant issues in structure, justification, or realism
- 0–3 = Unacceptable or non-compliant budget
Use the full range honestly. Do not give high scores unless the budget is genuinely exemplary.

Guidelines:
- Be precise, balanced, and professional.
- High scores (9–10) should still include small, value-added recommendations (e.g., transparency, formatting, or compliance enhancements).
- Respond ONLY in valid JSON format.
"""


FINAL_DECISION_PROMPT = """
You are an expert grant reviewer responsible for making a final funding decision.

You are provided with:
- Structured summary of the proposal
- Section-level scores and evaluations
- Notes on potential issues or weaknesses
- Budget evaluation results

Your task:
1. Review all inputs and identify critical weaknesses.
2. Evaluate the proposal strictly based on quality, feasibility, methodology, objectives, expected outcomes, and budget realism.
3. Compute a final_score (0–10) reflecting the overall merit; do not adjust score based on politeness, style, or superficial presentation.
4. Decide between:
   - "ACCEPT" → Strong proposal with no critical weaknesses
   - "CONDITIONALLY ACCEPT" → Promising proposal needing limited clarification or revision
   - "REJECT" → Serious weaknesses in feasibility, justification, or compliance
5. Provide a rationale explaining your decision, highlighting key strengths and weaknesses.
6. Suggest next steps for the applicant to improve the proposal.

Output format (strict JSON):
{{
  "final_score": float,          // weighted or reasoned average of all section scores, 0–10
  "decision": "ACCEPT" | "CONDITIONALLY ACCEPT" | "REJECT",
  "rationale": str,              // concise justification of the decision
  "key_strengths": [str, ...],   // highlights of the proposal
  "key_weaknesses": [str, ...],  // critical weaknesses to address
  "next_steps": str              // guidance for improvements
}}

Guidelines:
- Do not mention any internal agent names.
- Focus on proposal content, scientific merit, feasibility, and budget.
- Respond only in valid JSON format.
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
