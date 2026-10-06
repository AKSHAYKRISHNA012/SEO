import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from app.schemas import GEOAnalysis, EntityItem

ORGANIZATION_INDICATORS = ['inc', 'corp', 'llc', 'company', 'ltd', 'gmbh', 'technologies', 'group', 'software']

def analyze_geo(soup: BeautifulSoup, meta_title: str, domain: str) -> GEOAnalysis:
    text = soup.get_text(separator=' ')
    
    # 1. Entity Extraction
    entities: List[EntityItem] = []
    
    # Organization entity
    org_name = None
    title_parts = meta_title.split('|') if meta_title else []
    if len(title_parts) > 1:
        potential_org = title_parts[-1].strip()
        if len(potential_org) > 2:
            org_name = potential_org

    if not org_name:
        domain_parts = domain.replace('www.', '').split('.')
        org_name = domain_parts[0].capitalize()

    entities.append(EntityItem(name=org_name, category="Organization", confidence=0.95))

    # Industry / Category entity from title or headings
    headings_text = " ".join([h.get_text(strip=True) for h in soup.find_all(['h1', 'h2'])])
    
    cat_keywords = ['software', 'platform', 'service', 'agency', 'tools', 'analytics', 'e-commerce', 'solution', 'ai', 'cloud', 'security']
    found_cats = [c.capitalize() for c in cat_keywords if c in headings_text.lower()]
    for c in found_cats[:3]:
        entities.append(EntityItem(name=c, category="Industry", confidence=0.85))

    # Product / Service entities from H2s
    h2s = [h.get_text(strip=True) for h in soup.find_all('h2') if len(h.get_text(strip=True)) < 50]
    for h in h2s[:3]:
        entities.append(EntityItem(name=h, category="Product/Feature", confidence=0.80))

    # 2. Authority Signals
    author_found = bool(soup.find(attrs={'class': re.compile(r'author|byline', re.I)}) or soup.find(attrs={'rel': 'author'}))
    
    links = [a.get('href', '').lower() for a in soup.find_all('a', href=True)]
    about_linked = any('about' in l for l in links)
    contact_linked = any('contact' in l for l in links)

    trust_signals = []
    if author_found:
        trust_signals.append("Author bio / byline present")
    if about_linked:
        trust_signals.append("Link to About page detected")
    if contact_linked:
        trust_signals.append("Link to Contact page detected")

    privacy_terms = any('privacy' in l or 'terms' in l for l in links)
    if privacy_terms:
        trust_signals.append("Privacy Policy / Terms of Service links present")

    external_links = [l for l in links if l.startswith('http') and domain not in l]
    ext_citations_count = len(external_links)

    # 3. Content Structure & AI Readability
    paragraphs = soup.find_all('p')
    fact_statements = 0
    total_words = 0

    for p in paragraphs:
        p_text = p.get_text(strip=True)
        total_words += len(p_text.split())
        # Check for numbers, statistics, percentages, currency, dates
        if re.search(r'(\d+%|\$\d+|\b202[0-6]\b|\b\d+ (users|customers|percent|billion|million)\b)', p_text, re.IGNORECASE):
            fact_statements += 1

    factual_density_score = min(100, int((fact_statements / max(1, len(paragraphs))) * 100) + 40) if paragraphs else 50
    ai_readability_score = 75

    if headings_text and len(paragraphs) > 3:
        ai_readability_score += 10
    if trust_signals:
        ai_readability_score += 10
    ai_readability_score = min(100, ai_readability_score)

    # 4. GEO Recommendations
    recs = []
    if not author_found:
        recs.append("Add explicit author attributions (Author Name, Bio, and Credentials) to establish E-E-A-T for generative AI models.")
    if not about_linked:
        recs.append("Ensure clear navigational links to an 'About Us' page containing founding date, headquarters, and core mission.")
    if factual_density_score < 60:
        recs.append("Increase factual density: include concrete data points, statistics, official research citations, and exact specifications.")
    recs.append(f"Structure a clear 2-sentence entity summary defining '{org_name}' at the top of the main content section for Perplexity & ChatGPT Search indexing.")
    recs.append("Implement JSON-LD Organization schema with sameAs links to official Wikipedia, Crunchbase, LinkedIn, and social profiles.")

    return GEOAnalysis(
        entities=entities,
        organization_found=bool(org_name),
        author_info_found=author_found,
        about_page_linked=about_linked,
        contact_page_linked=contact_linked,
        trust_signals=trust_signals,
        external_citations_count=ext_citations_count,
        factual_density_score=factual_density_score,
        ai_readability_score=ai_readability_score,
        geo_recommendations=recs
    )
