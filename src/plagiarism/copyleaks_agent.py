from copyleaks import Copyleaks
import time

def run_plagiarism_check(proposal_text: str):
    copier = Copyleaks()
    email = "ekaanshjain13@gmail.com"
    api_key = "48a7e397-c717-464c-a370-b84d0ac4acaa"
    copier.login(email, api_key)

    scan_result = copier.submit_text_scan(proposal_text, sandbox=True)

    scan_id = list(scan_result["scanned"].keys())[0]

    print("[INFO] Waiting for plagiarism scan results...")
    time.sleep(15)  # Copyleaks needs processing time

    result = copier.get_scan_result(scan_id)
    
    return {
        "similarity_score": result["results"]["totalScore"],
        "matched_sources_count": len(result["results"]["internet"]),
        "matched_sources": [
            src["url"] for src in result["results"]["internet"][:5]
        ]
    }
