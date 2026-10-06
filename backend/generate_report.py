"""
SEO Intelligence — Project Documentation PDF Generator
Generates a professional project report PDF using ReportLab.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
import datetime

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'SEO_Intelligence_Project_Report.pdf')

# ── Color Palette ─────────────────────────────────────────────────────────────
BRAND_DARK   = colors.HexColor('#0f172a')   # slate-950
BRAND_MID    = colors.HexColor('#1e293b')   # slate-800
BRAND_CARD   = colors.HexColor('#1e293b')
BRAND_PURPLE = colors.HexColor('#6366f1')   # indigo-500
BRAND_CYAN   = colors.HexColor('#22d3ee')   # cyan-400
BRAND_GREEN  = colors.HexColor('#10b981')   # emerald-500
BRAND_AMBER  = colors.HexColor('#f59e0b')   # amber-500
BRAND_RED    = colors.HexColor('#ef4444')   # red-500
BRAND_TEXT   = colors.HexColor('#e2e8f0')   # slate-200
BRAND_MUTED  = colors.HexColor('#94a3b8')   # slate-400
WHITE        = colors.white
BLACK        = colors.black

# ── Styles ────────────────────────────────────────────────────────────────────
def build_styles():
    s = getSampleStyleSheet()

    custom = {
        'h1': ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=28,
                             textColor=WHITE, leading=36, spaceAfter=6),
        'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=18,
                             textColor=BRAND_CYAN, leading=24, spaceBefore=14, spaceAfter=8),
        'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=13,
                             textColor=BRAND_PURPLE, leading=18, spaceBefore=10, spaceAfter=5),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10,
                               textColor=BRAND_TEXT, leading=16, spaceAfter=6,
                               alignment=TA_JUSTIFY),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=10,
                                 textColor=BRAND_TEXT, leading=15, leftIndent=16,
                                 bulletIndent=4, spaceAfter=3),
        'code': ParagraphStyle('code', fontName='Courier', fontSize=9,
                               textColor=BRAND_CYAN, backColor=BRAND_MID,
                               leading=14, leftIndent=8, rightIndent=8,
                               spaceBefore=4, spaceAfter=4),
        'caption': ParagraphStyle('caption', fontName='Helvetica-Oblique', fontSize=8,
                                  textColor=BRAND_MUTED, alignment=TA_CENTER, spaceAfter=4),
        'tag': ParagraphStyle('tag', fontName='Helvetica-Bold', fontSize=8,
                              textColor=BRAND_PURPLE),
        'footer': ParagraphStyle('footer', fontName='Helvetica', fontSize=8,
                                 textColor=BRAND_MUTED, alignment=TA_CENTER),
        'cover_sub': ParagraphStyle('cover_sub', fontName='Helvetica', fontSize=13,
                                    textColor=BRAND_CYAN, alignment=TA_CENTER, leading=20),
        'cover_meta': ParagraphStyle('cover_meta', fontName='Helvetica', fontSize=10,
                                     textColor=BRAND_MUTED, alignment=TA_CENTER, leading=14),
        'section_label': ParagraphStyle('section_label', fontName='Helvetica-Bold', fontSize=9,
                                        textColor=BRAND_PURPLE, spaceBefore=4),
        'kv': ParagraphStyle('kv', fontName='Helvetica', fontSize=10,
                             textColor=BRAND_TEXT, leading=15),
    }
    return custom


# ── Canvas Callbacks ───────────────────────────────────────────────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page = self._pageNumber
        w, h = A4

        if page == 1:
            # Full dark cover background
            self.setFillColor(BRAND_DARK)
            self.rect(0, 0, w, h, fill=1, stroke=0)

            # Top gradient bar
            self.setFillColor(BRAND_PURPLE)
            self.rect(0, h - 8*mm, w, 8*mm, fill=1, stroke=0)

            # Decorative circles
            self.setFillColor(colors.HexColor('#6366f120'))
            self.setStrokeColor(colors.transparent)
            self.circle(w - 30*mm, h - 60*mm, 80, fill=1, stroke=0)
            self.circle(20*mm, 40*mm, 60, fill=1, stroke=0)

            # Bottom bar
            self.setFillColor(BRAND_MID)
            self.rect(0, 0, w, 22*mm, fill=1, stroke=0)
            self.setFont('Helvetica', 8)
            self.setFillColor(BRAND_MUTED)
            self.drawCentredString(w/2, 8*mm, '© 2024 Akshay Krishna  ·  SEO Intelligence Project  ·  Confidential Portfolio Document')
        else:
            # Background
            self.setFillColor(BRAND_DARK)
            self.rect(0, 0, w, h, fill=1, stroke=0)

            # Top bar
            self.setFillColor(BRAND_MID)
            self.rect(0, h - 12*mm, w, 12*mm, fill=1, stroke=0)
            self.setFillColor(BRAND_PURPLE)
            self.rect(0, h - 1.5*mm, w, 1.5*mm, fill=1, stroke=0)

            # Header text
            self.setFont('Helvetica-Bold', 8)
            self.setFillColor(BRAND_MUTED)
            self.drawString(15*mm, h - 8*mm, 'SEO INTELLIGENCE  ·  AI-POWERED SEO / GEO / AEO ANALYZER')
            self.drawRightString(w - 15*mm, h - 8*mm, f'Page {page} of {total_pages}')

            # Bottom bar
            self.setFillColor(BRAND_MID)
            self.rect(0, 0, w, 10*mm, fill=1, stroke=0)
            self.setFillColor(BRAND_PURPLE)
            self.rect(0, 0, w, 1.5*mm, fill=1, stroke=0)
            self.setFont('Helvetica', 7)
            self.setFillColor(BRAND_MUTED)
            self.drawCentredString(w/2, 3.5*mm, 'github.com/AKSHAYKRISHNA012/SEO  ·  Portfolio Project by Akshay Krishna')


# ── Helper Flowables ──────────────────────────────────────────────────────────
class ColorRect(Flowable):
    def __init__(self, width, height, fill_color, radius=4):
        super().__init__()
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.radius = radius

    def draw(self):
        self.canv.setFillColor(self.fill_color)
        self.canv.roundRect(0, 0, self.width, self.height, self.radius, fill=1, stroke=0)


class Divider(Flowable):
    def __init__(self, width, color=BRAND_PURPLE, thickness=1):
        super().__init__()
        self.width = width
        self.color = color
        self.thickness = thickness
        self.height = thickness + 4

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


def badge(text, color=BRAND_PURPLE):
    return Paragraph(
        f'<font color="#{color.hexval()[2:]}" size="8"><b> {text} </b></font>', 
        ParagraphStyle('badge', backColor=colors.HexColor(color.hexval()[:8]+'33'),
                       borderPadding=3, fontSize=8, leading=12)
    )


def section_header(title, styles, emoji=''):
    items = []
    items.append(Spacer(1, 8*mm))
    items.append(Paragraph(f'{emoji}  {title}', styles['h2']))
    items.append(Divider(170*mm, BRAND_PURPLE, 0.5))
    items.append(Spacer(1, 3*mm))
    return items


def info_card(rows, styles, col_widths=None):
    """Renders a dark info card table."""
    col_widths = col_widths or [55*mm, 115*mm]
    table = Table(rows, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BRAND_MID),
        ('TEXTCOLOR', (0, 0), (0, -1), BRAND_CYAN),
        ('TEXTCOLOR', (1, 0), (1, -1), BRAND_TEXT),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [BRAND_MID, colors.HexColor('#263044')]),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, colors.HexColor('#334155')),
    ]))
    return table


def score_bar_table(items_data, styles):
    """Renders score bars for each dimension."""
    rows = []
    for label, score, color in items_data:
        bar_width = int(score * 1.1)  # scale to mm
        bar_data = [
            [Paragraph(f'<b>{label}</b>', ParagraphStyle('sl', fontName='Helvetica-Bold',
                       fontSize=9, textColor=BRAND_TEXT)),
             Paragraph(f'<b>{score}/100</b>', ParagraphStyle('sv', fontName='Helvetica-Bold',
                       fontSize=9, textColor=color, alignment=TA_RIGHT))]
        ]
        bar_table = Table(bar_data, colWidths=[120*mm, 30*mm])
        bar_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        rows.append(bar_table)
    return rows


# ── Score Donut ────────────────────────────────────────────────────────────────
def make_score_donut(score, label, size=80):
    d = Drawing(size, size)
    cx, cy, r_outer, r_inner = size/2, size/2, size/2 - 4, size/2 - 16

    # Background ring
    d.add(Circle(cx, cy, r_outer, fillColor=BRAND_MID, strokeColor=colors.transparent))
    d.add(Circle(cx, cy, r_inner, fillColor=BRAND_DARK, strokeColor=colors.transparent))

    # Score arc (approximate with pie slice)
    p = Pie()
    p.x, p.y = cx - r_outer, cy - r_outer
    p.width = p.height = r_outer * 2
    p.data = [score, 100 - score]
    p.slices[0].fillColor = BRAND_PURPLE
    p.slices[1].fillColor = BRAND_MID
    p.slices[0].strokeColor = colors.transparent
    p.slices[1].strokeColor = colors.transparent
    p.startAngle = 90
    d.add(p)

    # Inner mask
    d.add(Circle(cx, cy, r_inner, fillColor=BRAND_DARK, strokeColor=colors.transparent))

    # Score text
    d.add(String(cx, cy + 3, str(score),
                 fontSize=18, fontName='Helvetica-Bold',
                 fillColor=WHITE, textAnchor='middle'))
    d.add(String(cx, cy - 10, label,
                 fontSize=6, fontName='Helvetica',
                 fillColor=BRAND_MUTED, textAnchor='middle'))
    return d


# ── Bar Chart ─────────────────────────────────────────────────────────────────
def make_bar_chart():
    d = Drawing(170*mm, 70*mm)
    bc = VerticalBarChart()
    bc.x, bc.y = 20*mm, 10*mm
    bc.width, bc.height = 140*mm, 50*mm
    bc.data = [[72, 68, 81, 75, 79]]
    bc.categoryAxis.categoryNames = ['SEO', 'AEO', 'GEO', 'Technical', 'Content']
    bc.bars[0].fillColor = BRAND_PURPLE
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 20
    bc.valueAxis.labels.fontName = 'Helvetica'
    bc.valueAxis.labels.fontSize = 7
    bc.valueAxis.labels.fillColor = BRAND_MUTED
    bc.categoryAxis.labels.fontName = 'Helvetica'
    bc.categoryAxis.labels.fontSize = 8
    bc.categoryAxis.labels.fillColor = BRAND_TEXT
    bc.categoryAxis.labels.angle = 0
    bc.barWidth = 15*mm
    bc.groupSpacing = 8*mm
    d.add(bc)
    return d


# ── Build PDF ─────────────────────────────────────────────────────────────────
def build_pdf():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=18*mm,
        bottomMargin=18*mm,
    )

    W = 170*mm  # usable width
    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 30*mm))

    # Main title
    story.append(Paragraph(
        '<font color="#6366f1">SEO</font> <font color="#22d3ee">Intelligence</font>',
        ParagraphStyle('cover_title', fontName='Helvetica-Bold', fontSize=36,
                       textColor=WHITE, alignment=TA_CENTER, leading=44)
    ))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('AI-Powered SEO / GEO / AEO Analyzer', styles['cover_sub']))
    story.append(Spacer(1, 6*mm))

    # Divider
    story.append(Divider(W, BRAND_PURPLE, 2))
    story.append(Spacer(1, 8*mm))

    # Description
    story.append(Paragraph(
        'A production-quality full-stack web application that analyzes any publicly accessible '
        'webpage and generates a comprehensive, actionable SEO, GEO, and AEO audit report '
        'with scoring, recommendations, and downloadable PDF exports.',
        ParagraphStyle('desc', fontName='Helvetica', fontSize=11, textColor=BRAND_MUTED,
                       alignment=TA_CENTER, leading=18)
    ))
    story.append(Spacer(1, 12*mm))

    # Tech badges
    tech_row = [['FastAPI', 'React 18', 'TypeScript', 'Vite', 'TailwindCSS',
                 'Python 3.11', 'SQLite', 'ReportLab']]
    t = Table(tech_row, colWidths=[W/8]*8)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BRAND_MID),
        ('TEXTCOLOR', (0, 0), (-1, -1), BRAND_CYAN),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#334155')),
    ]))
    story.append(t)
    story.append(Spacer(1, 16*mm))

    # Meta info table
    meta = [
        ['Project Name', 'SEO Intelligence — AI-Powered Analyzer'],
        ['Author', 'Akshay Krishna'],
        ['GitHub', 'github.com/AKSHAYKRISHNA012/SEO'],
        ['Email', 'akshaykrishna.a.2002@gmail.com'],
        ['Category', 'Portfolio Project — SEO / Digital Marketing / AI Engineering'],
        ['Status', 'Production Ready ✓'],
        ['Date', datetime.datetime.now().strftime('%B %d, %Y')],
        ['Version', '1.0.0'],
    ]
    story.append(info_card(meta, styles, col_widths=[45*mm, 125*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('Table of Contents', styles, '📋')

    toc_items = [
        ('1', 'Project Overview', '3'),
        ('2', 'Technology Stack', '3'),
        ('3', 'Architecture & System Design', '4'),
        ('4', 'Feature Deep-Dive', '4'),
        ('  4.1', 'Traditional SEO Analysis', '4'),
        ('  4.2', 'Technical SEO Analysis', '5'),
        ('  4.3', 'Answer Engine Optimization (AEO)', '5'),
        ('  4.4', 'Generative Engine Optimization (GEO)', '6'),
        ('  4.5', 'Structured Data & Schema Analysis', '6'),
        ('  4.6', 'Scoring Engine', '6'),
        ('5', 'API Reference', '7'),
        ('6', 'Frontend UI/UX Design', '7'),
        ('7', 'Database Design', '8'),
        ('8', 'Setup & Installation', '8'),
        ('9', 'Deployment Guide', '9'),
        ('10', 'SEO / Portfolio Impact', '9'),
    ]
    toc_data = [[Paragraph(f'<b>{n}</b>', ParagraphStyle('tn', fontName='Helvetica-Bold',
                           fontSize=9, textColor=BRAND_CYAN)),
                 Paragraph(title, ParagraphStyle('tt', fontName='Helvetica', fontSize=9,
                           textColor=BRAND_TEXT)),
                 Paragraph(pg, ParagraphStyle('tp', fontName='Helvetica', fontSize=9,
                           textColor=BRAND_MUTED, alignment=TA_RIGHT))]
                for n, title, pg in toc_items]

    toc_table = Table(toc_data, colWidths=[15*mm, 140*mm, 15*mm])
    toc_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, colors.HexColor('#1e293b')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [BRAND_DARK, colors.HexColor('#111827')]),
    ]))
    story.append(toc_table)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1 — PROJECT OVERVIEW
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('1. Project Overview', styles, '🎯')

    story.append(Paragraph(
        'SEO Intelligence is a production-quality, full-stack web application built as a '
        'professional portfolio project for an aspiring SEO Analyst, Digital Marketer, and '
        'AI Engineer. The application analyzes any publicly accessible webpage URL and '
        'generates a comprehensive, multi-dimensional audit report covering five key pillars:',
        styles['body']
    ))

    pillars = [
        ('🔍 Traditional SEO', 'Meta tags, headings, content quality, link equity, SERP preview'),
        ('⚙️ Technical SEO', 'Response time, SSL, robots.txt, sitemaps, image optimization'),
        ('🤖 AEO (Answer Engine)', 'Featured snippet readiness, FAQ extraction, Q&A detection'),
        ('🌐 GEO (Generative Engine)', 'AI citation readiness, entity extraction, fact density'),
        ('📊 Structured Data', 'JSON-LD schemas, Microdata, RDFa, rich result potential'),
    ]

    for icon_title, desc in pillars:
        story.append(Paragraph(
            f'<b><font color="#22d3ee">{icon_title}:</font></b>  {desc}',
            styles['bullet']
        ))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        'The application demonstrates genuine technical depth across full-stack development, '
        'web scraping, NLP heuristics, REST API design, modern React UI patterns, and '
        'emerging AI search optimization strategies.',
        styles['body']
    ))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2 — TECH STACK
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('2. Technology Stack', styles, '🛠️')

    stack_data = [
        ['Layer', 'Technology', 'Purpose'],
        ['Frontend', 'React 18 + TypeScript + Vite', 'SPA with type-safe components'],
        ['Styling', 'TailwindCSS 3 + Custom Design System', 'Dark-mode glassmorphism UI'],
        ['Charts', 'Recharts', 'Score visualizations & bar charts'],
        ['Icons', 'Lucide React', 'Consistent iconography'],
        ['PDF Export', 'jsPDF + html2canvas', 'Client-side PDF generation'],
        ['Backend', 'FastAPI + Python 3.11', 'Async REST API'],
        ['HTTP Client', 'httpx (async)', 'Webpage fetching with redirect handling'],
        ['HTML Parser', 'BeautifulSoup4 + lxml', 'DOM analysis & content extraction'],
        ['Database', 'SQLModel (SQLite / PostgreSQL)', 'Audit history persistence'],
        ['PDF Backend', 'ReportLab', 'Server-side PDF report generation'],
        ['Deployment', 'Vercel (FE) + Render (BE)', 'Free-tier cloud hosting'],
    ]

    stack_table = Table(stack_data, colWidths=[35*mm, 75*mm, 60*mm])
    stack_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('TEXTCOLOR', (0, 1), (0, -1), BRAND_CYAN),
        ('TEXTCOLOR', (1, 1), (-1, -1), BRAND_TEXT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRAND_MID, colors.HexColor('#263044')]),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.HexColor('#334155')),
    ]))
    story.append(stack_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3 — ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('3. Architecture & System Design', styles, '🏗️')

    story.append(Paragraph(
        'The application follows a clean client-server architecture with a React SPA frontend '
        'communicating with a FastAPI backend via RESTful JSON APIs. The analysis pipeline is '
        'fully asynchronous, using httpx for non-blocking HTTP requests and Python async/await '
        'throughout the analyzer modules.',
        styles['body']
    ))

    arch_text = [
        ('User Browser', 'React 18 SPA (Vite)', 'TypeScript Components'),
        ('HTTP POST /api/analyze', '⬇  JSON Response', ''),
        ('FastAPI Router', 'routes.py', 'Pydantic validation'),
        ('Analysis Pipeline', 'Parallel analyzer modules', 'async execution'),
        ('Fetcher (httpx)', 'BeautifulSoup4 parser', 'lxml engine'),
        ('SEO Analyzer', 'AEO Analyzer', 'GEO + Schema Analyzers'),
        ('Scoring Engine', 'Recommendations Engine', 'PDF Generator'),
        ('SQLModel ORM', 'SQLite / PostgreSQL', 'Audit history'),
    ]

    for row in arch_text:
        cols = [Paragraph(cell, ParagraphStyle('ac', fontName='Helvetica', fontSize=8.5,
                textColor=BRAND_TEXT, alignment=TA_CENTER)) for cell in row]
        t = Table([cols], colWidths=[W/3]*3)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), BRAND_MID),
            ('BOX', (0, 0), (-1, -1), 0.3, colors.HexColor('#334155')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 1*mm))

    story.append(Spacer(1, 4*mm))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4 — FEATURES
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('4. Feature Deep-Dive', styles, '✨')

    # 4.1 Traditional SEO
    story.append(Paragraph('4.1  Traditional SEO Analysis', styles['h3']))
    seo_features = [
        ('Title Tag', 'Validates length (50–60 chars optimal), keyword presence, truncation risk'),
        ('Meta Description', 'Length check (120–160 chars), call-to-action detection'),
        ('Canonical URL', 'Detects canonical tag presence and self-referencing'),
        ('Robots Directives', 'noindex / nofollow detection and implications'),
        ('Open Graph', 'og:title, og:description, og:image for social sharing'),
        ('Twitter Cards', 'twitter:card type, image, description validation'),
        ('Heading Structure', 'H1 count, H1–H6 hierarchy validation, keyword usage'),
        ('Content Quality', 'Word count, paragraph count, Flesch readability score'),
        ('Keyword Density', 'Top-10 keyword extraction with frequency analysis'),
        ('Link Equity', 'Internal/external link counts, do-follow ratio'),
        ('SERP Preview', 'Live Google snippet simulation with pixel-accurate title/desc'),
        ('Image Audit', 'Missing alt text, lazy loading detection, image count'),
    ]
    seo_data = [[Paragraph(f'<b><font color="#22d3ee">{k}</font></b>', styles['kv']),
                 Paragraph(v, styles['kv'])] for k, v in seo_features]
    story.append(Table(seo_data, colWidths=[45*mm, 125*mm],
                       style=TableStyle([
                           ('ROWBACKGROUNDS', (0, 0), (-1, -1), [BRAND_MID, colors.HexColor('#1a2640')]),
                           ('TOPPADDING', (0, 0), (-1, -1), 4),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                           ('LEFTPADDING', (0, 0), (-1, -1), 7),
                           ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
                           ('FONTSIZE', (0, 0), (-1, -1), 8.5),
                       ])))

    story.append(Spacer(1, 5*mm))

    # 4.2 Technical SEO
    story.append(Paragraph('4.2  Technical SEO Analysis', styles['h3']))
    tech_items = [
        'HTTP status code & redirect chain detection',
        'Response latency measurement (ms) with performance grade',
        'SSL/HTTPS enforcement check',
        'robots.txt accessibility & disallow rule inspection',
        'XML sitemap detection (sitemap.xml, sitemap_index.xml)',
        'Viewport meta tag for mobile-friendliness',
        'Image optimization: alt text compliance, lazy loading',
        'Page size estimation and load weight analysis',
    ]
    for item in tech_items:
        story.append(Paragraph(f'• {item}', styles['bullet']))

    story.append(PageBreak())

    # 4.3 AEO
    story.append(Paragraph('4.3  Answer Engine Optimization (AEO)', styles['h3']))
    story.append(Paragraph(
        'AEO focuses on optimizing content to appear in direct answer boxes, featured snippets, '
        'and voice search results. The analyzer detects:',
        styles['body']
    ))
    aeo_items = [
        ('Question Headings', 'Detects H1–H4 starting with What/How/Why/When/Where/Who'),
        ('FAQ Schema', 'Validates FAQPage JSON-LD or native FAQ HTML patterns'),
        ('Direct Answer Blocks', 'Identifies paragraph-level direct answers following questions'),
        ('Ordered Lists', 'Step-by-step lists ideal for how-to snippets'),
        ('Definition Content', '"X is a..." style definitional sentences'),
        ('Table Data', 'Tabular content for comparison snippets'),
        ('Snippet Simulator', 'Generates AI-simulated featured snippet for each question'),
        ('AEO Score (0–100)', 'Composite score weighted across all AEO signals'),
    ]
    aeo_data = [[Paragraph(f'<b><font color="#22d3ee">{k}</font></b>', styles['kv']),
                 Paragraph(v, styles['kv'])] for k, v in aeo_items]
    story.append(Table(aeo_data, colWidths=[45*mm, 125*mm],
                       style=TableStyle([
                           ('ROWBACKGROUNDS', (0, 0), (-1, -1), [BRAND_MID, colors.HexColor('#1a2640')]),
                           ('TOPPADDING', (0, 0), (-1, -1), 4),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                           ('LEFTPADDING', (0, 0), (-1, -1), 7),
                           ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
                           ('FONTSIZE', (0, 0), (-1, -1), 8.5),
                       ])))

    story.append(Spacer(1, 5*mm))

    # 4.4 GEO
    story.append(Paragraph('4.4  Generative Engine Optimization (GEO)', styles['h3']))
    story.append(Paragraph(
        'GEO analyzes how well a page will be cited and referenced by AI language models '
        'including ChatGPT Search, Perplexity, Google Gemini, and Claude. It evaluates:',
        styles['body']
    ))
    geo_items = [
        '• Named Entity Recognition — People, Organizations, Locations, Dates',
        '• Statistical Claims — Percentage figures, numeric facts, citations',
        '• Author & Byline Signals — E-E-A-T trust indicators',
        '• External Link Quality — References to authoritative domains',
        '• Fact Density Score — Quantifiable data points per 100 words',
        '• AI Citation Score — Overall likelihood of being cited by LLM search',
        '• Freshness Indicators — Publication dates, "updated" signals',
        '• Brand Entity Detection — Company/product name prominence',
    ]
    for item in geo_items:
        story.append(Paragraph(item, styles['bullet']))

    story.append(Spacer(1, 5*mm))

    # 4.5 Schema
    story.append(Paragraph('4.5  Structured Data & Schema Analysis', styles['h3']))
    schema_items = [
        ('JSON-LD Detection', 'Parses all script[type="application/ld+json"] blocks'),
        ('Microdata', 'Detects itemscope / itemtype HTML attributes'),
        ('RDFa', 'Identifies typeof / property RDFa attributes'),
        ('Schema Validation', 'Validates against 20+ common schema.org types'),
        ('Rich Result Types', 'FAQPage, Article, Product, BreadcrumbList, LocalBusiness, HowTo'),
        ('Gap Analysis', 'Identifies missing schemas with implementation code snippets'),
        ('Coverage Score', 'Percentage of recommended schemas implemented'),
    ]
    schema_data = [[Paragraph(f'<b><font color="#22d3ee">{k}</font></b>', styles['kv']),
                    Paragraph(v, styles['kv'])] for k, v in schema_items]
    story.append(Table(schema_data, colWidths=[45*mm, 125*mm],
                       style=TableStyle([
                           ('ROWBACKGROUNDS', (0, 0), (-1, -1), [BRAND_MID, colors.HexColor('#1a2640')]),
                           ('TOPPADDING', (0, 0), (-1, -1), 4),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                           ('LEFTPADDING', (0, 0), (-1, -1), 7),
                           ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
                           ('FONTSIZE', (0, 0), (-1, -1), 8.5),
                       ])))

    story.append(Spacer(1, 5*mm))

    # 4.6 Scoring
    story.append(Paragraph('4.6  Scoring Engine', styles['h3']))
    story.append(Paragraph(
        'All scores are normalized to 0–100. The composite overall score uses weighted averaging:',
        styles['body']
    ))
    score_data = [
        ['Dimension', 'Weight', 'Key Signals'],
        ['Traditional SEO', '30%', 'Meta, headings, content, links'],
        ['Technical SEO', '25%', 'Speed, SSL, robots, sitemap'],
        ['AEO Readiness', '20%', 'Questions, FAQ, snippets'],
        ['GEO Readiness', '15%', 'Entities, facts, authority'],
        ['Structured Data', '10%', 'JSON-LD, rich results'],
    ]
    score_table = Table(score_data, colWidths=[50*mm, 25*mm, 95*mm])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (0, -1), BRAND_CYAN),
        ('TEXTCOLOR', (1, 1), (1, -1), BRAND_AMBER),
        ('TEXTCOLOR', (2, 1), (2, -1), BRAND_TEXT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRAND_MID, colors.HexColor('#263044')]),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.HexColor('#334155')),
    ]))
    story.append(score_table)

    # Score bar chart
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph('Sample Score Distribution (demo analysis):', styles['caption']))
    story.append(make_bar_chart())
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5 — API
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('5. API Reference', styles, '📡')

    endpoints = [
        ('POST', '/api/analyze', 'Analyze a URL — full SEO/AEO/GEO audit'),
        ('GET', '/api/history', 'Retrieve paginated audit history'),
        ('GET', '/api/audit/{id}', 'Fetch a specific past audit by ID'),
        ('GET', '/api/health', 'Health check endpoint'),
        ('GET', '/docs', 'Swagger interactive API documentation'),
    ]
    ep_data = [['Method', 'Endpoint', 'Description']] + \
              [[Paragraph(f'<b><font color="{("#10b981" if m=="GET" else "#f59e0b")}">{m}</font></b>',
                          ParagraphStyle('m', fontName='Helvetica-Bold', fontSize=8.5)),
                Paragraph(f'<font face="Courier">{ep}</font>',
                          ParagraphStyle('ep', fontName='Courier', fontSize=8, textColor=BRAND_CYAN)),
                Paragraph(desc, styles['kv'])]
               for m, ep, desc in endpoints]

    ep_table = Table(ep_data, colWidths=[20*mm, 60*mm, 90*mm])
    ep_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRAND_MID, colors.HexColor('#263044')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.HexColor('#334155')),
    ]))
    story.append(ep_table)

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph('Request / Response Schema (POST /api/analyze):', styles['h3']))

    req_json = '''{
  "url": "https://example.com",
  "force_fresh": false
}'''
    story.append(Paragraph(req_json.replace('\n', '<br/>').replace(' ', '&nbsp;'),
                           styles['code']))

    res_json = '''{
  "url": "https://example.com",
  "domain": "example.com",
  "overall_score": 78,
  "seo": { "meta": {...}, "headings": {...}, "content": {...}, "links": {...} },
  "aeo": { "score": 68, "questions": [...], "snippet_ready": true },
  "geo": { "score": 81, "entities": [...], "fact_density": 2.4 },
  "technical": { "score": 75, "response_time_ms": 342, "https": true },
  "structured_data": { "score": 79, "schemas": [...], "missing": [...] },
  "recommendations": [
    { "priority": "critical", "category": "SEO", "title": "Add H1 tag", "action": "..." }
  ],
  "analyzed_at": "2024-01-01T00:00:00Z"
}'''
    story.append(Paragraph(res_json.replace('\n', '<br/>').replace(' ', '&nbsp;'),
                           styles['code']))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 6 — UI/UX
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('6. Frontend UI/UX Design', styles, '🎨')

    story.append(Paragraph(
        'The frontend is built with a premium dark-mode aesthetic using TailwindCSS with a '
        'custom design system. Key design decisions:',
        styles['body']
    ))

    ui_items = [
        ('Color Palette', 'slate-950 background, indigo-500 accent, cyan-400 highlights'),
        ('Typography', 'Inter (Google Fonts) — clean, modern, highly readable'),
        ('Glassmorphism', 'backdrop-blur cards with semi-transparent backgrounds'),
        ('Micro-animations', 'Progress bars, score counter animations, hover effects'),
        ('Tab Navigation', '7 tabs: Overview, SEO, AEO, GEO, Technical, Schema, History'),
        ('Score Gauge', 'Animated SVG circular gauge with color-coded scoring'),
        ('SERP Preview', 'Pixel-accurate Google snippet simulation with live URL/title/desc'),
        ('Recharts', 'Spider/radar chart for dimension comparison, bar charts'),
        ('Priority Cards', 'Color-coded critical/warning/info recommendation cards'),
        ('PDF Export', 'jsPDF + html2canvas client-side PDF generation'),
        ('Responsive', 'Mobile-first responsive layout with Tailwind breakpoints'),
        ('Dark Mode', 'Full dark-mode with class-based Tailwind configuration'),
    ]
    ui_data = [[Paragraph(f'<b><font color="#22d3ee">{k}</font></b>', styles['kv']),
                Paragraph(v, styles['kv'])] for k, v in ui_items]
    story.append(Table(ui_data, colWidths=[45*mm, 125*mm],
                       style=TableStyle([
                           ('ROWBACKGROUNDS', (0, 0), (-1, -1), [BRAND_MID, colors.HexColor('#1a2640')]),
                           ('TOPPADDING', (0, 0), (-1, -1), 4),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                           ('LEFTPADDING', (0, 0), (-1, -1), 7),
                           ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
                           ('FONTSIZE', (0, 0), (-1, -1), 8.5),
                       ])))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 7 — DATABASE
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('7. Database Design', styles, '🗄️')

    story.append(Paragraph(
        'The application uses SQLModel (built on SQLAlchemy + Pydantic) for ORM. '
        'SQLite is used in development; PostgreSQL is supported in production via environment variable.',
        styles['body']
    ))

    db_schema = [
        ['Column', 'Type', 'Description'],
        ['id', 'INTEGER PK', 'Auto-increment primary key'],
        ['url', 'VARCHAR (indexed)', 'Analyzed webpage URL'],
        ['domain', 'VARCHAR', 'Extracted domain name'],
        ['overall_score', 'INTEGER', 'Composite score 0–100'],
        ['seo_score', 'INTEGER', 'Traditional SEO pillar score'],
        ['aeo_score', 'INTEGER', 'AEO pillar score'],
        ['geo_score', 'INTEGER', 'GEO pillar score'],
        ['technical_score', 'INTEGER', 'Technical SEO pillar score'],
        ['schema_score', 'INTEGER', 'Structured data pillar score'],
        ['full_report_json', 'TEXT', 'Full analysis JSON payload'],
        ['analyzed_at', 'DATETIME', 'UTC timestamp of analysis'],
    ]
    db_table = Table(db_schema, colWidths=[45*mm, 35*mm, 90*mm])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('TEXTCOLOR', (0, 1), (0, -1), BRAND_CYAN),
        ('TEXTCOLOR', (1, 1), (1, -1), BRAND_AMBER),
        ('TEXTCOLOR', (2, 1), (2, -1), BRAND_TEXT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRAND_MID, colors.HexColor('#263044')]),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.HexColor('#334155')),
    ]))
    story.append(db_table)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 8 — SETUP
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('8. Setup & Installation', styles, '⚙️')

    story.append(Paragraph('Backend:', styles['h3']))
    backend_cmds = [
        'git clone https://github.com/AKSHAYKRISHNA012/SEO.git',
        'cd SEO/backend',
        'python -m venv venv && venv\\Scripts\\activate',
        'pip install -r requirements.txt',
        'python -m uvicorn app.main:app --port 8000 --reload',
    ]
    for cmd in backend_cmds:
        story.append(Paragraph(f'$ {cmd}',
                               ParagraphStyle('cmd', fontName='Courier', fontSize=8.5,
                                              textColor=BRAND_GREEN, backColor=BRAND_MID,
                                              leftIndent=8, leading=14, spaceAfter=2)))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('Frontend:', styles['h3']))
    frontend_cmds = [
        'cd SEO/frontend',
        'npm install',
        'npm run dev',
    ]
    for cmd in frontend_cmds:
        story.append(Paragraph(f'$ {cmd}',
                               ParagraphStyle('cmd', fontName='Courier', fontSize=8.5,
                                              textColor=BRAND_GREEN, backColor=BRAND_MID,
                                              leftIndent=8, leading=14, spaceAfter=2)))

    story.append(Spacer(1, 4*mm))
    req_table = [
        ['Requirement', 'Minimum Version'],
        ['Python', '3.11+'],
        ['Node.js', '18+'],
        ['npm', '9+'],
        ['Git', 'Any'],
    ]
    rt = Table(req_table, colWidths=[80*mm, 90*mm])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (0, -1), BRAND_CYAN),
        ('TEXTCOLOR', (1, 1), (1, -1), BRAND_TEXT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRAND_MID, colors.HexColor('#263044')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.HexColor('#334155')),
    ]))
    story.append(rt)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 9 — DEPLOYMENT
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('9. Deployment Guide', styles, '🌐')

    deploy_data = [
        ['Platform', 'Service', 'Config', 'URL Pattern'],
        ['Render.com', 'Backend (FastAPI)', 'render.yaml', 'https://seo-intelligence-api.onrender.com'],
        ['Vercel', 'Frontend (React)', 'vercel.json', 'https://seo-*.vercel.app'],
        ['GitHub', 'Source Code', '.github/', 'github.com/AKSHAYKRISHNA012/SEO'],
    ]
    deploy_table = Table(deploy_data, colWidths=[30*mm, 40*mm, 30*mm, 70*mm])
    deploy_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('TEXTCOLOR', (0, 1), (0, -1), BRAND_CYAN),
        ('TEXTCOLOR', (1, 1), (-1, -1), BRAND_TEXT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRAND_MID, colors.HexColor('#263044')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.HexColor('#334155')),
    ]))
    story.append(deploy_table)

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        'Environment variables required for production deployment:',
        styles['body']
    ))
    env_data = [
        ['Variable', 'Service', 'Value'],
        ['VITE_API_URL', 'Vercel (Frontend)', 'https://seo-intelligence-api.onrender.com'],
        ['DATABASE_URL', 'Render (Backend)', 'sqlite:///./seo_intelligence.db OR postgresql://...'],
        ['ENVIRONMENT', 'Render (Backend)', 'production'],
    ]
    env_table = Table(env_data, colWidths=[45*mm, 40*mm, 85*mm])
    env_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 1), (0, -1), BRAND_AMBER),
        ('TEXTCOLOR', (1, 1), (1, -1), BRAND_MUTED),
        ('TEXTCOLOR', (2, 1), (2, -1), BRAND_CYAN),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRAND_MID, colors.HexColor('#263044')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.HexColor('#334155')),
    ]))
    story.append(env_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 10 — PORTFOLIO IMPACT
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header('10. SEO / Portfolio Impact', styles, '🏆')

    story.append(Paragraph(
        'This project demonstrates a broad and deep skill set that aligns with roles in '
        'SEO Analysis, Digital Marketing, AI Engineering, and Full-Stack Development:',
        styles['body']
    ))

    skills_data = [
        ['Skill Area', 'Demonstrated By'],
        ['Full-Stack Development', 'React + FastAPI end-to-end application'],
        ['SEO Expertise', 'Comprehensive 5-pillar SEO audit implementation'],
        ['GEO Strategy', 'AI search readiness analysis (ChatGPT, Perplexity, Gemini)'],
        ['AEO Strategy', 'Featured snippet & FAQ optimization detection'],
        ['Web Scraping', 'Async httpx + BeautifulSoup4 HTML parsing pipeline'],
        ['API Design', 'RESTful FastAPI with Pydantic schema validation'],
        ['Database Design', 'SQLModel ORM with SQLite/PostgreSQL support'],
        ['UI/UX Design', 'Premium Tailwind dark-mode with glassmorphism'],
        ['Data Visualization', 'Recharts spider/bar charts for score analysis'],
        ['PDF Generation', 'ReportLab server-side + jsPDF client-side reports'],
        ['Cloud Deployment', 'Vercel + Render CI/CD from GitHub'],
        ['TypeScript', 'Full type safety across React components'],
        ['Python', '3.11 async patterns throughout backend'],
    ]
    sk_table = Table(skills_data, colWidths=[65*mm, 105*mm])
    sk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BRAND_PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (0, -1), BRAND_CYAN),
        ('TEXTCOLOR', (1, 1), (1, -1), BRAND_TEXT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BRAND_MID, colors.HexColor('#263044')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('BOX', (0, 0), (-1, -1), 0.5, BRAND_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.2, colors.HexColor('#334155')),
    ]))
    story.append(sk_table)

    # Final divider
    story.append(Spacer(1, 12*mm))
    story.append(Divider(W, BRAND_PURPLE, 1.5))
    story.append(Spacer(1, 6*mm))

    # Contact & links
    contact_data = [
        ['👤 Author', 'Akshay Krishna'],
        ['📧 Email', 'akshaykrishna.a.2002@gmail.com'],
        ['💻 GitHub', 'github.com/AKSHAYKRISHNA012'],
        ['🚀 Project Repo', 'github.com/AKSHAYKRISHNA012/SEO'],
        ['📄 License', 'MIT License'],
    ]
    story.append(info_card(contact_data, styles, col_widths=[40*mm, 130*mm]))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(
        f'Generated on {datetime.datetime.now().strftime("%B %d, %Y at %H:%M")} IST  ·  '
        'SEO Intelligence v1.0.0  ·  Portfolio Project',
        styles['footer']
    ))

    # ── Build ──────────────────────────────────────────────────────────────────
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f'PDF generated successfully: {OUTPUT_PATH}')
    return OUTPUT_PATH


if __name__ == '__main__':
    build_pdf()
