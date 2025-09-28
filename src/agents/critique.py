from src.llm_wrapper import gemini_llm
from src.prompts import SCIENTIFIC_CRITIQUE_PROMPT
from src.prompts import PRACTICAL_CRITIQUE_PROMPT

def run_critique(summary: str):
    """
    Return both practical and scientific critiques of the summary.
    """
    practical = gemini_llm(PRACTICAL_CRITIQUE_PROMPT.format(summary=summary))
    scientific = gemini_llm(SCIENTIFIC_CRITIQUE_PROMPT.format(summary=summary))
    return {"practical": practical, "scientific": scientific}
