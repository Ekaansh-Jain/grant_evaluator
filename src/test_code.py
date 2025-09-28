# test_prompt.py
from src.llm_wrapper import gemini_llm
from src.prompts import SUMMARY_PROMPT

# Sample text from retriever (take 2–3 pages for testing)
sample_context = """
Page 1: SAMPLE GRANT PROPOSAL
Over the years the Ohio Office of Criminal Justice Services (OCJS) has received requests from grant applicants...

Page 2: EVALUATION
To determine whether project objectives are being met, Dr. N. Cruncher of the Department of Statistics will evaluate the project...

Page 3: Cover Letter
Mr. Fred Brown, MacAllister Foundation...
"""

# Fill the prompt
prompt = SUMMARY_PROMPT.format(context=sample_context)

# Send to LLM
response = gemini_llm(prompt)

print("LLM Response:")
print(response)
