from sentence_transformers import SentenceTransformer
import numpy as np
from .reference_loader import load_reference_corpus

model = SentenceTransformer("all-MiniLM-L6-v2")

def detect_plagiarism(proposal_text: str):
    reference_texts = load_reference_corpus()

    proposal_emb = model.encode([proposal_text], convert_to_numpy=True)
    ref_embs = model.encode(reference_texts, convert_to_numpy=True)

    # Cosine Similarity
    sims = (proposal_emb @ ref_embs.T) / (
        np.linalg.norm(proposal_emb) * np.linalg.norm(ref_embs, axis=1)
    )

    best_match_idx = int(np.argmax(sims))
    best_score = float(sims[0][best_match_idx])

    return {
        "similarity_score": round(best_score, 3),
        "matched_reference_text": reference_texts[best_match_idx],
        "risk_level": (
            "HIGH" if best_score > 0.75 else
            "MEDIUM" if best_score > 0.55 else
            "LOW"
        )
    }
