from src.agents.input_agent import input_agent
from src.agents.vectorstore_agent import vectorstore_agent
from src.agents.summarizer import run_summarizer_extended
import json

SAMPLE_FILE = "/Users/ekaanshjain/Desktop/ocjs_sample_grant.pdf"

# Load document
pages = input_agent(SAMPLE_FILE)

# Create vectorstore and retriever
vs = vectorstore_agent(pages)

# Generate structured summary
summary = run_summarizer_extended(vs["ask"])
from src.agents.scoring import run_grant_scoring

# After generating summary
scores = run_grant_scoring(summary)
print(json.dumps(scores, indent=2))