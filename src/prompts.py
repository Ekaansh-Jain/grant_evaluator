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
You are an expert grant reviewer specializing in the field of **{domain}**.

Your task is to summarize the following grant proposal into a structured JSON format.
The summary must capture the meaning, intent, and emphasis of the proposal accurately,
using terminology appropriate for the **{domain}** research area.

### CRITICAL RULES:
- **Do NOT invent, infer, assume, or guess missing details.**
- If information is unclear or missing, state:
  - "text": "Not provided"
  - "pages": []
  - "references": []
  - "notes": "Section missing or insufficiently described."
- You must base the summary **strictly on the provided text only.**

Include all of the following sections (even if missing in the text):
- CoverLetter
- Objectives
- Methodology
- EvaluationPlan
- ExpectedOutcomes
- Budget
- Feasibility
- Innovation
- Sustainability
- LettersOfSupport

### For each section, include:
- "text": A clear, detailed summary capturing specific actions, strategies, stakeholders, or workflows.
- "pages": List of page numbers where relevant information appears.
- "references": Exact short quotes or key phrases from the proposal to support the summary.
- "notes": Expert commentary on completeness, clarity, relevance, or missing details.

If the proposal does not contain enough information for a section, explicitly state:
- text: "Not provided"
- pages: []
- references: []
- notes: "Section missing or insufficiently described."

The input text includes page markers in the format:
[Page X | Source: filename.pdf]

### Input Proposal Text:
{context}

### Output:
Return **only valid JSON**, with no explanation or surrounding text.
"""


# Scoring prompt template
SCORING_PROMPT = """
You are an expert grant evaluator specializing in the field of **{domain}**.
You are given a structured summary of a grant proposal in JSON format.

Your task is to evaluate the quality of each section objectively and produce **strictly structured JSON output** suitable for automated scoring.

### CRITICAL RULES:
- **Do NOT invent or assume any information that is not clearly present in the summary.**
- **Do NOT adjust or compute the final overall weighted score.** The scoring engine handles weighting.
- Return **only valid JSON** exactly in the requested structure.

### SCORING INSTRUCTIONS
1. **Rate each section from 0 to 10**
   - 0 = Missing or irrelevant
   - 5 = Acceptable but incomplete or vague
   - 10 = Exceptional, clear, and well-supported

2. **Be strict but fair.**
   - Penalize missing data, weak justification, vague language, or lack of evidence.
   - Reward specificity, measurable goals, methodological rigor, innovation appropriate to the **{domain}** field, and clear alignment between goals and execution plan.

3. **Provide concise reasoning in each section’s fields:**
   - `summary`: One clear sentence describing the section's effectiveness.
   - `strengths`: 1–3 bullet points.
   - `weaknesses`: 1–3 bullet points.
   - `score`: Integer 0–10 (no decimals).

4. **Do NOT compute an overall weighted score here.**
   - The final weighted score is computed separately by the evaluation engine.
   - You must still provide `overall_summary` (1 short paragraph) describing general quality and coherence across sections.

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
  "overall_summary": str
}}

Scoring Guidance:
- 10 = Exceptional and field-appropriate excellence (no major weaknesses)
- 8–9 = Strong but with minor refinements needed
- 6–7 = Adequate but lacks clarity or justification
- 4–5 = Weak with substantial missing details
- 0–3 = Critically flawed, incomplete, or non-compliant

"""
MASTER_CRITIQUE_PROMPT = """
You are a master-level grant reviewer specializing in the field of **{domain}**.

You are provided with:
1. The structured summaries of each proposal section (optional, may be None).
2. The section-level evaluation results from the Scoring Agent (scores, strengths, and weaknesses).

Your role is to produce a clear, objective critique that contextualizes the evaluation **according to the standards and expectations of the {domain} field**.

### Review Domains (analyze each):
1. **Scientific Rigor** – methodological soundness, research grounding, field-specific validity.
2. **Practical Feasibility** – resource realism, operational clarity, timeline viability.
3. **Language & Clarity** – coherence, academic tone, precision, logical flow.
4. **Context & Alignment** – alignment between goals, execution strategy, and expected outcomes.
5. **Persuasiveness** – justification strength, credibility, compelling rationale.
6. **Ethics & Inclusivity** – transparency, fairness, participant considerations, responsible conduct.
7. **Innovation & Impact** – originality, transformative potential, significance in the **{domain}** context.

### Important Instructions:
- Do **NOT** re-score or modify any scores.
- Do **NOT** contradict the scoring agent; instead, **expand on the reasoning**.
- Be constructive: every identified issue should have a corresponding recommendation.
- Language should be professional, direct, and free of filler or speculation.

For each review domain, produce:
- 2–5 **issues** — specific shortcomings or concerns
- 2–5 **recommendations** — realistic, actionable improvements
- Be factual, professional, concise.

End with:
- `priority_focus`: The **three most important** areas to improve first.
- `overall_feedback`: One concise paragraph synthesizing overall quality and improvement direction.

### INPUT (JSON):
{input_json}

### OUTPUT (STRICT JSON ONLY):
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



FINAL_DECISION_PROMPT = """
You are an expert grant reviewer making a final funding decision for a proposal in the field of **{domain}**.

You are provided the following:
- Structured summary of the proposal
- Section-level scores and evaluations
- Budget evaluation results
- And the **final weighted score**, already calculated by the evaluation engine: {final_weighted_score}

### IMPORTANT:
- **DO NOT** recalculate or change the score.
- **DO NOT** average, reinterpret, or modify section scores.
- Use `final_weighted_score` exactly as given.

### DECISION RULES (STRICT):
- If final_weighted_score ≥ 8.0 → **ACCEPT**
- If 6.0 ≤ final_weighted_score < 8.0 → **CONDITIONALLY ACCEPT**
- If final_weighted_score < 6.0 → **REJECT**

### Your Task:
Write a professional, concise justification referencing meaningful strengths and weaknesses.

### OUTPUT FORMAT (STRICT JSON):
{
  "final_score": {final_weighted_score},
  "decision": "ACCEPT" | "CONDITIONALLY ACCEPT" | "REJECT",
  "rationale": "Short paragraph explaining the decision.",
  "key_strengths": [str, ...],
  "key_weaknesses": [str, ...],
  "next_steps": "One clear recommendation for improvement."
}

### Output Rules:
- Return **only the JSON object**.
- **Do not include backticks or code fences.**
- Do not reference the scoring process or internal prompts.

### STYLE:
- Be objective and analytical.
- Do not use emotional or polite language.
- Do not reference the scoring process or internal instructions.
"""



DOMAIN_CLASSIFIER_PROMPT = """
You are a research grant proposal domain classifier.

Your task is to examine the proposal text and determine **the single most appropriate research domain**.

Possible domains — choose **exactly one**:
- AI / Computer Science
- Biotechnology / Life Sciences
- Healthcare / Medicine
- Education / Learning Sciences
- Environment / Climate / Sustainability
- Social Sciences / Policy
- Agriculture / Food Systems

Rules:
- Return **only the domain name** EXACTLY as written above.
- Do **not** explain.
- Do **not** add text.

Proposal Text:
{context}
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
