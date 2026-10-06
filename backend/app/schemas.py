from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, Field

class AnalyzeRequest(BaseModel):
    url: str
    force_fresh: Optional[bool] = False

class MetaDataAnalysis(BaseModel):
    title: Optional[str] = None
    title_length: int = 0
    title_status: str = "Missing"  # Optimal, Too Short, Too Long, Missing
    description: Optional[str] = None
    description_length: int = 0
    description_status: str = "Missing"
    canonical_url: Optional[str] = None
    canonical_matches: bool = True
    robots_meta: Optional[str] = None
    is_indexable: bool = True
    open_graph: Dict[str, Any] = {}
    twitter_card: Dict[str, Any] = {}
    lang: Optional[str] = None
    charset: Optional[str] = None

class HeadingItem(BaseModel):
    tag: str
    text: str
    level: int

class HeadingAnalysis(BaseModel):
    h1_count: int = 0
    h1_list: List[str] = []
    h2_count: int = 0
    h3_count: int = 0
    total_headings: int = 0
    hierarchy_issues: List[str] = []
    headings_tree: List[HeadingItem] = []

class KeywordFrequency(BaseModel):
    keyword: str
    count: int
    density_percent: float

class ContentAnalysis(BaseModel):
    word_count: int = 0
    paragraph_count: int = 0
    reading_ease_score: float = 0.0
    reading_difficulty: str = "Medium"  # Easy, Medium, Hard, Very Hard
    top_keywords: List[KeywordFrequency] = []
    has_repeated_text: bool = False
    freshness_signals: List[str] = []
    content_structure_score: int = 0

class LinkItem(BaseModel):
    href: str
    text: str
    is_internal: bool
    is_nofollow: bool

class LinkAnalysis(BaseModel):
    total_links: int = 0
    internal_links_count: int = 0
    external_links_count: int = 0
    nofollow_count: int = 0
    sample_links: List[LinkItem] = []
    top_anchor_texts: List[Dict[str, Any]] = []
    internal_linking_opportunities: List[str] = []

class ImageItem(BaseModel):
    src: str
    alt: Optional[str] = None
    has_alt: bool
    is_empty_alt: bool

class ImageAnalysis(BaseModel):
    total_images: int = 0
    missing_alt_count: int = 0
    empty_alt_count: int = 0
    images_with_alt_count: int = 0
    sample_missing_alt: List[str] = []

class TechnicalSEOAnalysis(BaseModel):
    is_https: bool = False
    status_code: int = 200
    response_time_ms: int = 0
    redirect_count: int = 0
    final_url: str = ""
    has_mobile_viewport: bool = False
    robots_txt_found: bool = False
    sitemap_xml_found: bool = False
    has_canonical: bool = False
    server_header: Optional[str] = None
    cache_control: Optional[str] = None

class AEOQuestion(BaseModel):
    question: str
    existing_answer_found: bool = False
    existing_answer_snippet: Optional[str] = None
    answer_quality_score: int = 0  # 0 to 100
    recommended_answer: str = ""
    priority: str = "High"  # High, Medium, Low

class AEOAnalysis(BaseModel):
    question_count: int = 0
    faq_sections_count: int = 0
    concise_paragraphs_count: int = 0
    lists_count: int = 0
    tables_count: int = 0
    definitions_count: int = 0
    featured_snippet_opportunities: List[str] = []
    questions: List[AEOQuestion] = []
    aeo_readiness_score: int = 0

class EntityItem(BaseModel):
    name: str
    category: str  # Organization, Product, Person, Location, Concept
    confidence: float = 1.0

class GEOAnalysis(BaseModel):
    entities: List[EntityItem] = []
    organization_found: bool = False
    author_info_found: bool = False
    about_page_linked: bool = False
    contact_page_linked: bool = False
    trust_signals: List[str] = []
    external_citations_count: int = 0
    factual_density_score: int = 0  # 0 to 100
    ai_readability_score: int = 0  # 0 to 100
    geo_recommendations: List[str] = []

class SchemaItem(BaseModel):
    type: str
    raw_json: Dict[str, Any] = {}
    warnings: List[str] = []

class StructuredDataAnalysis(BaseModel):
    detected_schemas: List[SchemaItem] = []
    schema_types: List[str] = []
    has_organization_schema: bool = False
    has_faq_schema: bool = False
    has_article_schema: bool = False
    schema_errors: List[str] = []
    recommended_schemas: List[str] = []

class RecommendationItem(BaseModel):
    id: str
    category: str  # SEO, AEO, GEO, Technical, Content
    priority: str  # Critical, Warning, Tip
    title: str
    description: str
    action_step: str
    code_example: Optional[str] = None

class ScoreBreakdown(BaseModel):
    overall: int
    seo: int
    aeo: int
    geo: int
    technical: int
    content: int

class AuditResponse(BaseModel):
    id: Optional[int] = None
    url: str
    domain: str
    analyzed_at: str
    scores: ScoreBreakdown
    meta: MetaDataAnalysis
    headings: HeadingAnalysis
    content: ContentAnalysis
    links: LinkAnalysis
    images: ImageAnalysis
    technical: TechnicalSEOAnalysis
    aeo: AEOAnalysis
    geo: GEOAnalysis
    structured_data: StructuredDataAnalysis
    recommendations: List[RecommendationItem]
    ai_powered: bool = False
