from src.prompts import SUMMARY_PROMPT

def run_summarizer(llm, docs, max_chars=10000):
    """
    Summarize the entire document into grant-review format.
    
    Args:
        llm: function that takes a prompt string and returns LLM output.
        docs: list of Document objects (already chunked).
        max_chars: maximum characters to pass to the LLM (to avoid token overflow).
    """
    # Combine all chunks into one big context
    full_text = "\n\n".join([d.page_content for d in docs])
    context = full_text[:max_chars]  # truncate if too long for the model

    # Format with structured prompt
    prompt = SUMMARY_PROMPT.format(context=context)

    # Call LLM
    return llm(prompt)