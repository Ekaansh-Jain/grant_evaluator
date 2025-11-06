from src.agents.input_agent import input_agent
from src.plagiarism.plagiarism_detector import detect_plagiarism

# Test using an actual proposal file
SAMPLE_FILE = "/Users/ekaanshjain/Desktop/sample.pdf"

pages = input_agent(SAMPLE_FILE)

# Use the raw text for plagiarism detection (NOT the summary)
proposal_text = " ".join([p.page_content.replace("\n", " ").strip() for p in pages])

result = detect_plagiarism(proposal_text)

print("\n=== PLAGIARISM CHECK RESULT ===\n")
print("Similarity Score:", result["similarity_score"])
print("Risk Level:", result["risk_level"])
print("\nClosest Match:", result["matched_reference_text"])
