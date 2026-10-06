import json
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from app.schemas import StructuredDataAnalysis, SchemaItem

COMMON_SCHEMAS = ['Organization', 'WebSite', 'Article', 'FAQPage', 'Product', 'BreadcrumbList', 'LocalBusiness', 'SoftwareApplication']

def analyze_schemas(soup: BeautifulSoup) -> StructuredDataAnalysis:
    script_tags = soup.find_all('script', type='application/ld+json')
    detected_schemas: List[SchemaItem] = []
    schema_types = []
    
    has_org = False
    has_faq = False
    has_article = False
    errors = []

    for tag in script_tags:
        if not tag.string:
            continue
        try:
            raw_data = json.loads(tag.string)
            items = raw_data if isinstance(raw_data, list) else [raw_data]
            
            for item in items:
                stype = item.get('@type', 'Unknown')
                if isinstance(stype, list):
                    stype = stype[0]
                
                schema_types.append(stype)
                warnings = []

                if stype in ['Organization', 'Corporation', 'LocalBusiness']:
                    has_org = True
                    if 'name' not in item:
                        warnings.append("Missing required 'name' property in Organization schema.")
                    if 'url' not in item:
                        warnings.append("Missing 'url' property in Organization schema.")

                elif stype == 'FAQPage':
                    has_faq = True
                    if 'mainEntity' not in item:
                        warnings.append("FAQPage schema missing 'mainEntity' question array.")

                elif stype in ['Article', 'NewsArticle', 'BlogPosting']:
                    has_article = True
                    if 'headline' not in item:
                        warnings.append("Article schema missing 'headline'.")
                    if 'author' not in item:
                        warnings.append("Article schema missing 'author'.")

                detected_schemas.append(SchemaItem(
                    type=stype,
                    raw_json=item if isinstance(item, dict) else {"content": str(item)},
                    warnings=warnings
                ))

        except Exception as e:
            errors.append(f"JSON-LD syntax error in script tag: {str(e)[:100]}")

    recommended = []
    if not has_org:
        recommended.append("Organization Schema - Essential for entity graph recognition and brand panel.")
    if not has_faq:
        recommended.append("FAQPage Schema - Enables rich snippet expanded FAQ dropdowns in SERP.")
    if not has_article:
        recommended.append("Article Schema - Enhances indexing speed, author attribution, and Google Discover visibility.")
    if 'BreadcrumbList' not in schema_types:
        recommended.append("BreadcrumbList Schema - Clarifies site architecture and URL hierarchy in search results.")

    return StructuredDataAnalysis(
        detected_schemas=detected_schemas,
        schema_types=list(set(schema_types)),
        has_organization_schema=has_org,
        has_faq_schema=has_faq,
        has_article_schema=has_article,
        schema_errors=errors,
        recommended_schemas=recommended
    )
