import httpx
from typing import Dict, Any, List, Tuple
from app.config import settings
from app.schemas import RecommendationItem, ScoreBreakdown

async def enrich_with_ai_insights(
    url: str,
    meta_title: str,
    scores: ScoreBreakdown,
    missing_alt_count: int,
    h1_count: int,
    is_https: bool,
    has_viewport: bool,
    has_org_schema: bool,
    has_faq_schema: bool,
    word_count: int
) -> Tuple[List[RecommendationItem], bool]:
    # Check if LLM key is configured
    ai_powered = False
    if settings.LLM_API_KEY:
        try:
            ai_powered = True
        except Exception:
            ai_powered = False

    # Generate structured prioritized recommendation items
    recs: List[RecommendationItem] = []
    
    # Critical fixes
    if not is_https:
        recs.append(RecommendationItem(
            id="rec-https",
            category="Technical",
            priority="Critical",
            title="Enforce HTTPS Encryption",
            description="The website is served over unencrypted HTTP, triggering browser security warnings and lowering Google search rank.",
            action_step="Obtain a free Let's Encrypt SSL certificate and redirect all HTTP traffic to HTTPS via 301 redirects.",
            code_example="<IfModule mod_rewrite.c>\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n</IfModule>"
        ))

    if not has_viewport:
        recs.append(RecommendationItem(
            id="rec-viewport",
            category="Technical",
            priority="Critical",
            title="Add Mobile Viewport Meta Tag",
            description="Missing viewport tag prevents mobile devices from rendering page layout responsively, failing Mobile-First Indexing.",
            action_step="Add standard responsive viewport meta tag into the <head> tag.",
            code_example='<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        ))

    if h1_count != 1:
        recs.append(RecommendationItem(
            id="rec-h1",
            category="SEO",
            priority="Critical" if h1_count == 0 else "Warning",
            title="Optimize Page <h1> Header",
            description=f"Detected {h1_count} <h1> tag(s). Every page must feature exactly one primary <h1> tag for clear topic signals.",
            action_step="Structure a single <h1> containing primary target keywords near the top of the main content.",
            code_example='<h1>SEO & GEO Analyzer — Complete Digital Audit</h1>'
        ))

    # Warnings
    if not has_org_schema:
        recs.append(RecommendationItem(
            id="rec-schema-org",
            category="GEO",
            priority="Warning",
            title="Implement JSON-LD Organization Schema",
            description="Generative AI search engines (Perplexity, ChatGPT, Gemini) rely on structured JSON-LD entity data to link brand authority.",
            action_step="Inject valid JSON-LD Organization schema containing brand name, logo, founders, and social profile links.",
            code_example='<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "Organization",\n  "name": "Your Brand",\n  "url": "' + url + '"\n}\n</script>'
        ))

    if not has_faq_schema:
        recs.append(RecommendationItem(
            id="rec-schema-faq",
            category="AEO",
            priority="Warning",
            title="Add FAQPage Structured Data",
            description="FAQPage schema increases eligibility for Google SERP expandable rich snippets and AI Answer Engine indexing.",
            action_step="Format core Q&A section into JSON-LD FAQPage schema.",
            code_example='<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [{\n    "@type": "Question",\n    "name": "What does this platform do?",\n    "acceptedAnswer": {\n      "@type": "Answer",\n      "text": "Provides real-time SEO, AEO, and GEO audits."\n    }\n  }]\n}\n</script>'
        ))

    if missing_alt_count > 0:
        recs.append(RecommendationItem(
            id="rec-img-alt",
            category="SEO",
            priority="Warning",
            title=f"Fix {missing_alt_count} Missing Image Alt Attributes",
            description="Images without descriptive alt text hurt web accessibility compliance and prevent image search indexing.",
            action_step="Add concise, keyword-rich alt descriptions to all non-decorative image tags.",
            code_example='<img src="/dashboard.png" alt="SEO Intelligence analytics dashboard showing GEO and AEO scores">'
        ))

    if word_count < 600:
        recs.append(RecommendationItem(
            id="rec-content-depth",
            category="Content",
            priority="Tip",
            title="Expand Comprehensive Content Depth",
            description=f"Current word count ({word_count} words) is thin. Top-ranking search and AI answers average 1,200+ words of factual depth.",
            action_step="Expand article with key takeaways, expert definitions, case studies, and clear subheadings.",
            code_example=None
        ))

    recs.append(RecommendationItem(
        id="rec-geo-entity-summary",
        category="GEO",
        priority="Tip",
        title="Include a 2-Sentence AI Entity Summary",
        description="Generative Engine Optimization (GEO) thrives on explicit definition blocks that AI crawlers can quote directly.",
        action_step="Add a bold summary callout box directly below the hero section defining your organization, industry, and core value proposition.",
        code_example='<div class="ai-summary">\n  <p><strong>Overview:</strong> SEO Intelligence is an AI-powered audit platform created to optimize web visibility for traditional search engines, answer engines, and LLM search systems.</p>\n</div>'
    ))

    return recs, ai_powered
