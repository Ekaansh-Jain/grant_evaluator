from src.agents.pdf_generator import generate_grant_pdf

sample_summary = {
    "Objectives": {
        "text": "Increase public safety by improving officer fitness.",
        "notes": "Clear measurable objective.",
        "score": 90,
        "status": "Accepted"
    },
    "Methodology": {
        "text": "Evaluate officers before fitness program, ensure 3x/week workouts, collect data every 6 weeks.",
        "notes": "Detailed evaluation plan.",
        "score": 85,
        "status": "Accepted"
    },
    "ExpectedOutcomes": {
        "text": "Improve officer fitness and reduce time off work.",
        "notes": "Linked directly to objectives.",
        "score": 80,
        "status": "Accepted"
    },
    "Innovation": {
        "text": "Approach improves public safety through officer fitness.",
        "notes": "Moderate innovation.",
        "score": 70,
        "status": "Accepted"
    },
    "Feasibility": {
        "text": "City Council and Friends of Police Department support project funding.",
        "notes": "Strong feasibility.",
        "score": 95,
        "status": "Accepted"
    }
}

generate_grant_pdf(sample_summary, output_path="test_grant_advanced4.pdf", title="Sample Grant Evaluation")
