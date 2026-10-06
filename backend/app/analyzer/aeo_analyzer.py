import re
from bs4 import BeautifulSoup
from typing import List, Tuple
from app.schemas import AEOAnalysis, AEOQuestion

QUESTION_PATTERNS = [
    r'^(what|how|why|when|where|who|which|can|is|are|does|do|should|could|would)\b',
    r'\?$'
]

def analyze_aeo(soup: BeautifulSoup, meta_title: str, top_keywords: List[str]) -> AEOAnalysis:
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
    question_headings = []
    
    for h in headings:
        text = h.get_text(strip=True)
        if any(re.search(pat, text, re.IGNORECASE) for pat in QUESTION_PATTERNS):
            question_headings.append(h)

    # FAQ Section detection
    faq_sections = soup.find_all(attrs={'class': re.compile(r'faq', re.I)}) + soup.find_all('details')
    faq_count = len(faq_sections)

    # Concise answer paragraphs (under 60 words following question headings)
    concise_paragraphs = 0
    generated_questions = []

    for qh in question_headings:
        q_text = qh.get_text(strip=True)
        sibling = qh.find_next_sibling()
        existing_answer = None
        ans_quality = 40
        
        while sibling and sibling.name not in ['h1', 'h2', 'h3', 'h4']:
            if sibling.name == 'p':
                p_text = sibling.get_text(strip=True)
                words = p_text.split()
                if 10 <= len(words) <= 65:
                    concise_paragraphs += 1
                    existing_answer = p_text
                    ans_quality = 88
                    break
                elif len(words) > 65:
                    existing_answer = p_text[:180] + "..."
                    ans_quality = 65
                    break
            elif sibling.name in ['ul', 'ol']:
                items = [li.get_text(strip=True) for li in sibling.find_all('li')[:3]]
                existing_answer = " • ".join(items)
                ans_quality = 82
                break
            sibling = sibling.find_next_sibling()

        generated_questions.append(AEOQuestion(
            question=q_text,
            existing_answer_found=existing_answer is not None,
            existing_answer_snippet=existing_answer,
            answer_quality_score=ans_quality if existing_answer else 25,
            recommended_answer=build_recommended_answer(q_text, meta_title, top_keywords),
            priority="High" if not existing_answer else "Medium"
        ))

    # Supplemental Question Generation if page has few question headers
    if len(generated_questions) < 4:
        topic = meta_title or (top_keywords[0] if top_keywords else "this topic")
        additional_qs = [
            f"What is {topic} and how does it work?",
            f"What are the main benefits of {topic}?",
            f"How much does {topic} cost or require to implement?",
            f"Who is {topic} best suited for?"
        ]
        for q in additional_qs:
            if not any(g.question.lower() == q.lower() for g in generated_questions):
                generated_questions.append(AEOQuestion(
                    question=q,
                    existing_answer_found=False,
                    existing_answer_snippet=None,
                    answer_quality_score=15,
                    recommended_answer=build_recommended_answer(q, meta_title, top_keywords),
                    priority="High"
                ))

    # Lists, Tables, Definitions count
    lists_count = len(soup.find_all(['ul', 'ol']))
    tables_count = len(soup.find_all('table'))
    definitions_count = len(soup.find_all('dl'))

    # Featured snippet opportunities
    opps = []
    if concise_paragraphs == 0:
        opps.append("Add direct 40-50 word answer paragraphs immediately below question headings to target Google Featured Snippets and AI overviews.")
    if lists_count == 0:
        opps.append("Incorporate ordered/unordered lists (<ol>/<ul>) for step-by-step processes or key feature summaries.")
    if tables_count == 0:
        opps.append("Use structured HTML <table> elements for comparison metrics, pricing, or spec sheets.")
    if faq_count == 0:
        opps.append("Implement an explicit FAQ section with FAQPage schema.org structured data.")

    # AEO Readiness score calculation
    readiness = 30
    if len(question_headings) >= 2:
        readiness += 25
    if concise_paragraphs >= 2:
        readiness += 20
    if lists_count >= 2:
        readiness += 15
    if tables_count >= 1:
        readiness += 10
    readiness = min(100, readiness)

    return AEOAnalysis(
        question_count=len(generated_questions),
        faq_sections_count=faq_count,
        concise_paragraphs_count=concise_paragraphs,
        lists_count=lists_count,
        tables_count=tables_count,
        definitions_count=definitions_count,
        featured_snippet_opportunities=opps,
        questions=generated_questions[:8],
        aeo_readiness_score=readiness
    )

def build_recommended_answer(question: str, title: str, keywords: List[str]) -> str:
    kw_str = ", ".join(keywords[:3]) if keywords else "key features and specifications"
    return f"{question.replace('?', '')} is clearly defined through {title or 'this page'}. It covers {kw_str} with concise, verified facts formatted for instant search retrieval."
