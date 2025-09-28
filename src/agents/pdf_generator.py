from fpdf import FPDF

def generate_pdf(output_path: str, summary: str, scores: dict, critiques: dict, budget: dict, final_decision: dict):
    """
    Generate a PDF report of the evaluation.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Grant Proposal Evaluation", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Summary:\n{summary}\n")
    pdf.multi_cell(0, 8, f"Scores:\n{scores}\n")
    pdf.multi_cell(0, 8, f"Practical Critique:\n{critiques['practical']}\n")
    pdf.multi_cell(0, 8, f"Scientific Critique:\n{critiques['scientific']}\n")
    pdf.multi_cell(0, 8, f"Budget Decision:\n{budget}\n")
    pdf.multi_cell(0, 8, f"Final Decision:\n{final_decision}\n")

    pdf.output(output_path)
