from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm

def generate_grant_pdf(grant_data: dict, output_path="grant_summary.pdf", title="Grant Evaluation"):
    width, height = A4
    c = canvas.Canvas(output_path, pagesize=A4)

    # --- Header ---
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 2*cm, title)

    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(2)
    c.line(2*cm, height-2.5*cm, width-2*cm, height-2.5*cm)

    y = height - 4*cm

    # --- Summary Section ---
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.black)
    c.drawString(2*cm, y, "Summary of Evaluation:")

    y -= 1*cm
    summary_sections = grant_data.get("Summary", {})

    for section, details in summary_sections.items():
        text = details.get("text", "")
        notes = details.get("notes", "")

        # Section Title
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkred)
        c.drawString(2*cm, y, f"■ {section}")

        # Section Text
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        text_lines = text.split("\n")
        for i, line in enumerate(text_lines):
            y -= 0.6*cm
            c.drawString(3*cm, y, line)

        # Notes
        if notes:
            y -= 0.6*cm
            c.setFont("Helvetica-Oblique", 10)
            c.setFillColor(colors.gray)
            c.drawString(3*cm, y, f"Notes: {notes}")

        y -= 1*cm  # spacing after each section

    # --- Overall Score (meter bar) ---
    score = grant_data.get("Score", 0)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(2*cm, y, "Overall Score:")

    bar_width, bar_height = 12*cm, 1*cm
    y_bar = y - 1.5*cm
    c.setStrokeColor(colors.black)
    c.rect(2*cm, y_bar, bar_width, bar_height)

    filled = bar_width * (score / 100)
    c.setFillColor(colors.green if score >= 80 else colors.orange if score >= 50 else colors.red)
    c.rect(2*cm, y_bar, filled, bar_height, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.black)
    c.drawString(2*cm + bar_width + 0.5*cm, y_bar + 0.2*cm, f"{score}/100")

    # --- Critique Section ---
    y = y_bar - 2*cm
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawString(2*cm, y, "Critique & Recommendations:")

    critique_points = grant_data.get("Critique", [])
    c.setFont("Helvetica", 12)
    for point in critique_points:
        y -= 0.8*cm
        c.drawString(2.5*cm, y, f"- {point}")

    # --- Final Decision Banner ---
    decision = grant_data.get("Decision", "Pending")
    banner_color = colors.green if decision.lower() == "accepted" else colors.red
    c.setFillColor(banner_color)
    c.rect(0, 0, width, 2*cm, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.white)
    c.drawCentredString(width/2, 0.7*cm, f"FINAL DECISION: {decision.upper()}")

    c.save()
    print(f"PDF saved to {output_path}")
