import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from typing import Dict, Any

def generate_pdf_report(audit_data: Dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15
    )

    heading2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    elements = []

    # Title & Header
    url = audit_data.get('url', 'N/A')
    date_str = audit_data.get('analyzed_at', 'N/A')
    scores = audit_data.get('scores', {})

    elements.append(Paragraph("SEO Intelligence — Comprehensive Audit Report", title_style))
    elements.append(Paragraph(f"Analyzed URL: <b>{url}</b> &nbsp;|&nbsp; Generated: {date_str}", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceAfter=15))

    # Overall Scorecard Banner
    overall = scores.get('overall', 0)
    overall_color = '#10b981' if overall >= 80 else ('#f59e0b' if overall >= 60 else '#f43f5e')

    score_data = [
        ['Overall Audit Score', 'SEO Score', 'AEO Score', 'GEO Score', 'Tech Score', 'Content Score'],
        [f"{overall}/100", f"{scores.get('seo', 0)}/100", f"{scores.get('aeo', 0)}/100", f"{scores.get('geo', 0)}/100", f"{scores.get('technical', 0)}/100", f"{scores.get('content', 0)}/100"]
    ]

    score_table = Table(score_data, colWidths=[90, 85, 85, 85, 85, 85])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0,1), (0,1), colors.HexColor(overall_color)),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 12),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))

    elements.append(score_table)
    elements.append(Spacer(1, 15))

    # Metadata & Tech Summary
    elements.append(Paragraph("1. Technical & Metadata Summary", heading2_style))
    meta = audit_data.get('meta', {})
    tech = audit_data.get('technical', {})

    tech_matrix = [
        [Paragraph("<b>Page Title:</b>", body_style), Paragraph(str(meta.get('title') or 'Missing'), body_style)],
        [Paragraph("<b>Meta Description:</b>", body_style), Paragraph(str(meta.get('description') or 'Missing'), body_style)],
        [Paragraph("<b>HTTPS Secured:</b>", body_style), Paragraph("Yes" if tech.get('is_https') else "No (Critical)", body_style)],
        [Paragraph("<b>Mobile Viewport:</b>", body_style), Paragraph("Yes" if tech.get('has_mobile_viewport') else "No", body_style)],
        [Paragraph("<b>Robots.txt / Sitemap:</b>", body_style), Paragraph(f"Robots: {'Found' if tech.get('robots_txt_found') else 'Missing'} | Sitemap: {'Found' if tech.get('sitemap_xml_found') else 'Missing'}", body_style)],
        [Paragraph("<b>Response Time:</b>", body_style), Paragraph(f"{tech.get('response_time_ms', 0)} ms", body_style)]
    ]

    t_table = Table(tech_matrix, colWidths=[140, 400])
    t_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f1f5f9')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_table)
    elements.append(Spacer(1, 15))

    # Key Action Plan Recommendations
    elements.append(Paragraph("2. Actionable Optimization Action Plan", heading2_style))
    recs = audit_data.get('recommendations', [])

    rec_rows = [['Category', 'Priority', 'Issue & Action Step']]
    for r in recs[:8]:
        prio = r.get('priority', 'Tip')
        cat = r.get('category', 'General')
        title = r.get('title', '')
        action = r.get('action_step', '')
        
        detail_p = Paragraph(f"<b>{title}</b><br/>{action}", body_style)
        rec_rows.append([cat, prio, detail_p])

    r_table = Table(rec_rows, colWidths=[70, 65, 405])
    r_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('ALIGN', (0,0), (1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(r_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
