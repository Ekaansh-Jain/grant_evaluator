from langchain.prompts import PromptTemplate

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["context"],
    template="""
You are an expert grant reviewer. Your task is to provide a structured summary 
STRICTLY based only on the provided text. 

⚠️ Do not add assumptions, interpretations, or guesses.  
⚠️ If some detail is missing, write exactly: "Not provided".  

Text:
{context}

Return the summary in this format:
- Objectives
- Methodology
- Expected Outcomes
- Innovation / Novelty
- Feasibility
"""
)

SCORING_PROMPT = PromptTemplate(
    input_variables=["summary"],
    template="""
You are an expert grant evaluator. 
Score the following proposal summary STRICTLY on a scale of 1–5 
(1 = Poor, 5 = Excellent). 

Return ONLY a JSON object with these exact keys:

{{
  "Objectives": int,
  "Methodology": int,
  "ExpectedOutcomes": int,
  "Innovation": int,
  "Feasibility": int,
  "Overall": int
}}

The "Overall" score should be the sum of the 5 criteria.

Summary:
{summary}
"""
)
