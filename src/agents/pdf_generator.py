from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime


def generate_evaluation_report_pdf(evaluation_data: dict) -> BytesIO:
    """
    Generate a comprehensive PDF report for grant evaluation
    Returns a BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#374151'),
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1f2937'),
        alignment=TA_JUSTIFY
    )
    
    # Title
    elements.append(Paragraph("Grant Evaluation Report", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # File Information
    elements.append(Paragraph("Document Information", heading_style))
    file_info_data = [
        ['File Name:', evaluation_data.get('file_name', 'N/A')],
        ['File Size:', f"{evaluation_data.get('file_size', 0) / 1024:.2f} KB"],
        ['Evaluation Date:', datetime.fromisoformat(evaluation_data.get('created_at', datetime.now().isoformat())).strftime('%Y-%m-%d %H:%M:%S')],
    ]
    
    file_info_table = Table(file_info_data, colWidths=[4*cm, 13*cm])
    file_info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
    ]))
    elements.append(file_info_table)
    elements.append(Spacer(1, 1*cm))
    
    # Final Decision Banner
    decision = evaluation_data.get('decision', 'PENDING')
    decision_colors = {
        'ACCEPT': colors.HexColor('#10b981'),
        'REJECT': colors.HexColor('#ef4444'),
        'REVISE': colors.HexColor('#f59e0b'),
        'CONDITIONALLY ACCEPT': colors.HexColor('#06b6d4')
    }
    decision_color = decision_colors.get(decision, colors.grey)
    
    decision_data = [[Paragraph(f"<b>DECISION: {decision}</b>", ParagraphStyle(
        'DecisionStyle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.white,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))]]
    
    decision_table = Table(decision_data, colWidths=[17*cm])
    decision_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), decision_color),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    elements.append(decision_table)
    elements.append(Spacer(1, 1*cm))
    
    # Overall Score
    overall_score = evaluation_data.get('overall_score', 0)
    elements.append(Paragraph(f"Overall Score: {overall_score:.1f}/100", heading_style))
    
    # Score visualization
    score_bar_data = [['']]
    score_bar = Table(score_bar_data, colWidths=[17*cm], rowHeights=[0.8*cm])
    
    # Determine color based on score
    if overall_score >= 80:
        bar_color = colors.HexColor('#10b981')
    elif overall_score >= 60:
        bar_color = colors.HexColor('#f59e0b')
    else:
        bar_color = colors.HexColor('#ef4444')
    
    # Create gradient effect with multiple cells
    score_percentage = overall_score / 100
    filled_width = 17 * score_percentage
    
    score_bar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e5e7eb')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    
    elements.append(score_bar)
    elements.append(Spacer(1, 0.3*cm))
    
    # Score text
    elements.append(Paragraph(f"<i>{overall_score:.1f}% - {get_score_description(overall_score)}</i>", normal_style))
    elements.append(Spacer(1, 1*cm))
    
    # Detailed Scores
    elements.append(Paragraph("Detailed Score Breakdown", heading_style))
    scores = evaluation_data.get('scores', [])
    
    if scores:
        score_data = [['Category', 'Score', 'Max', 'Percentage']]
        for score_item in scores:
            category = score_item.get('category', 'N/A')
            score = score_item.get('score', 0)
            max_score = score_item.get('maxScore', 10)
            percentage = (score / max_score * 100) if max_score > 0 else 0
            score_data.append([category, str(score), str(max_score), f"{percentage:.1f}%"])
        
        score_table = Table(score_data, colWidths=[8*cm, 3*cm, 3*cm, 3*cm])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ]))
        elements.append(score_table)
        
        # Add strengths and weaknesses
        elements.append(Spacer(1, 0.8*cm))
        for score_item in scores:
            category = score_item.get('category', 'N/A')
            elements.append(Paragraph(f"<b>{category}</b>", subheading_style))
            
            strengths = score_item.get('strengths', [])
            if strengths:
                elements.append(Paragraph("<b>Strengths:</b>", normal_style))
                for strength in strengths:
                    elements.append(Paragraph(f"• {strength}", normal_style))
            
            weaknesses = score_item.get('weaknesses', [])
            if weaknesses:
                elements.append(Paragraph("<b>Weaknesses:</b>", normal_style))
                for weakness in weaknesses:
                    elements.append(Paragraph(f"• {weakness}", normal_style))
            
            elements.append(Spacer(1, 0.5*cm))
    
    elements.append(PageBreak())
    
    # Full Critique
    elements.append(Paragraph("Comprehensive Critique", heading_style))
    full_critique = evaluation_data.get('full_critique', {})
    
    if full_critique:
        # Summary
        summary = full_critique.get('summary', 'No summary available.')
        elements.append(Paragraph("<b>Executive Summary:</b>", subheading_style))
        elements.append(Paragraph(summary, normal_style))
        elements.append(Spacer(1, 0.8*cm))
        
        # Issues
        issues = full_critique.get('issues', [])
        if issues:
            elements.append(Paragraph("<b>Issues Identified:</b>", subheading_style))
            for issue in issues:
                severity = issue.get('severity', 'medium')
                severity_colors_map = {
                    'high': colors.HexColor('#ef4444'),
                    'medium': colors.HexColor('#f59e0b'),
                    'low': colors.HexColor('#3b82f6')
                }
                severity_color = severity_colors_map.get(severity, colors.grey)
                
                category = issue.get('category', 'General')
                description = issue.get('description', 'No description.')
                
                issue_text = f"<b>[{severity.upper()}]</b> <b>{category}:</b> {description}"
                elements.append(Paragraph(issue_text, normal_style))
                elements.append(Spacer(1, 0.3*cm))
            
            elements.append(Spacer(1, 0.5*cm))
        
        # Recommendations
        recommendations = full_critique.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("<b>Recommendations:</b>", subheading_style))
            for rec in recommendations:
                priority = rec.get('priority', 'medium')
                recommendation = rec.get('recommendation', 'No recommendation.')
                
                rec_text = f"<b>[{priority.upper()} Priority]</b> {recommendation}"
                elements.append(Paragraph(rec_text, normal_style))
                elements.append(Spacer(1, 0.3*cm))
    
    elements.append(Spacer(1, 1*cm))
    
    # Budget Analysis
    elements.append(Paragraph("Budget Analysis", heading_style))
    budget_analysis = evaluation_data.get('budget_analysis', {})
    
    if budget_analysis:
        total_budget = budget_analysis.get('totalBudget', 0)
        elements.append(Paragraph(f"<b>Total Budget:</b> ${total_budget:,.2f}", normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Budget breakdown
        breakdown = budget_analysis.get('breakdown', [])
        if breakdown:
            budget_data = [['Category', 'Amount', 'Percentage']]
            for item in breakdown:
                category = item.get('category', 'N/A')
                amount = item.get('amount', 0)
                percentage = item.get('percentage', 0)
                budget_data.append([category, f"${amount:,.2f}", f"{percentage:.1f}%"])
            
            budget_table = Table(budget_data, colWidths=[8*cm, 5*cm, 4*cm])
            budget_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ]))
            elements.append(budget_table)
            elements.append(Spacer(1, 0.8*cm))
        
        # Budget flags
        flags = budget_analysis.get('flags', [])
        if flags:
            elements.append(Paragraph("<b>Budget Flags:</b>", subheading_style))
            for flag in flags:
                flag_type = flag.get('type', 'info')
                message = flag.get('message', 'No message.')
                
                flag_colors_map = {
                    'error': colors.HexColor('#ef4444'),
                    'warning': colors.HexColor('#f59e0b'),
                    'info': colors.HexColor('#3b82f6')
                }
                
                flag_text = f"<b>[{flag_type.upper()}]</b> {message}"
                elements.append(Paragraph(flag_text, normal_style))
                elements.append(Spacer(1, 0.3*cm))
            
            elements.append(Spacer(1, 0.5*cm))
        
        # Budget summary
        budget_summary = budget_analysis.get('summary', '')
        if budget_summary:
            elements.append(Paragraph("<b>Budget Summary:</b>", subheading_style))
            elements.append(Paragraph(budget_summary, normal_style))
    
    # Build PDF
    doc.build(elements)
    
    # Reset buffer position to beginning
    buffer.seek(0)
    return buffer


def get_score_description(score: float) -> str:
    """Get a text description based on the score"""
    if score >= 90:
        return "Excellent - Highly Recommended"
    elif score >= 80:
        return "Very Good - Recommended"
    elif score >= 70:
        return "Good - Consider with Minor Revisions"
    elif score >= 60:
        return "Satisfactory - Major Revisions Needed"
    elif score >= 50:
        return "Below Average - Significant Concerns"
    else:
        return "Poor - Not Recommended"
