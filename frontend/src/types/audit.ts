export interface ScoreBreakdown {
  overall: number;
  seo: number;
  aeo: number;
  geo: number;
  technical: number;
  content: number;
}

export interface MetaDataAnalysis {
  title: string | null;
  title_length: number;
  title_status: 'Optimal' | 'Too Short' | 'Too Long' | 'Missing';
  description: string | null;
  description_length: number;
  description_status: 'Optimal' | 'Too Short' | 'Too Long' | 'Missing';
  canonical_url: string | null;
  canonical_matches: boolean;
  robots_meta: string | null;
  is_indexable: boolean;
  open_graph: Record<string, string>;
  twitter_card: Record<string, string>;
  lang?: string;
  charset?: string;
}

export interface HeadingItem {
  tag: string;
  text: string;
  level: number;
}

export interface HeadingAnalysis {
  h1_count: number;
  h1_list: string[];
  h2_count: number;
  h3_count: number;
  total_headings: number;
  hierarchy_issues: string[];
  headings_tree: HeadingItem[];
}

export interface KeywordFrequency {
  keyword: string;
  count: number;
  density_percent: number;
}

export interface ContentAnalysis {
  word_count: number;
  paragraph_count: number;
  reading_ease_score: number;
  reading_difficulty: 'Easy' | 'Medium' | 'Hard' | 'Very Hard';
  top_keywords: KeywordFrequency[];
  has_repeated_text: boolean;
  freshness_signals: string[];
  content_structure_score: number;
}

export interface LinkItem {
  href: string;
  text: string;
  is_internal: boolean;
  is_nofollow: boolean;
}

export interface LinkAnalysis {
  total_links: number;
  internal_links_count: number;
  external_links_count: number;
  nofollow_count: number;
  sample_links: LinkItem[];
  top_anchor_texts: { anchor: string; count: number }[];
  internal_linking_opportunities: string[];
}

export interface ImageAnalysis {
  total_images: number;
  missing_alt_count: number;
  empty_alt_count: number;
  images_with_alt_count: number;
  sample_missing_alt: string[];
}

export interface TechnicalSEOAnalysis {
  is_https: boolean;
  status_code: number;
  response_time_ms: number;
  redirect_count: number;
  final_url: string;
  has_mobile_viewport: boolean;
  robots_txt_found: boolean;
  sitemap_xml_found: boolean;
  has_canonical: boolean;
  server_header?: string;
  cache_control?: string;
}

export interface AEOQuestion {
  question: string;
  existing_answer_found: boolean;
  existing_answer_snippet: string | null;
  answer_quality_score: number;
  recommended_answer: string;
  priority: 'High' | 'Medium' | 'Low';
}

export interface AEOAnalysis {
  question_count: number;
  faq_sections_count: number;
  concise_paragraphs_count: number;
  lists_count: number;
  tables_count: number;
  definitions_count: number;
  featured_snippet_opportunities: string[];
  questions: AEOQuestion[];
  aeo_readiness_score: number;
}

export interface EntityItem {
  name: string;
  category: string;
  confidence: number;
}

export interface GEOAnalysis {
  entities: EntityItem[];
  organization_found: boolean;
  author_info_found: boolean;
  about_page_linked: boolean;
  contact_page_linked: boolean;
  trust_signals: string[];
  external_citations_count: number;
  factual_density_score: number;
  ai_readability_score: number;
  geo_recommendations: string[];
}

export interface SchemaItem {
  type: string;
  raw_json: Record<string, any>;
  warnings: string[];
}

export interface StructuredDataAnalysis {
  detected_schemas: SchemaItem[];
  schema_types: string[];
  has_organization_schema: boolean;
  has_faq_schema: boolean;
  has_article_schema: boolean;
  schema_errors: string[];
  recommended_schemas: string[];
}

export interface RecommendationItem {
  id: string;
  category: 'SEO' | 'AEO' | 'GEO' | 'Technical' | 'Content';
  priority: 'Critical' | 'Warning' | 'Tip';
  title: string;
  description: string;
  action_step: string;
  code_example?: string;
}

export interface AuditResponse {
  id?: number;
  url: string;
  domain: string;
  analyzed_at: string;
  scores: ScoreBreakdown;
  meta: MetaDataAnalysis;
  headings: HeadingAnalysis;
  content: ContentAnalysis;
  links: LinkAnalysis;
  images: ImageAnalysis;
  technical: TechnicalSEOAnalysis;
  aeo: AEOAnalysis;
  geo: GEOAnalysis;
  structured_data: StructuredDataAnalysis;
  recommendations: RecommendationItem[];
  ai_powered: boolean;
}

export interface HistoricalAuditItem {
  id: number;
  url: string;
  domain: string;
  title?: string;
  overall_score: number;
  seo_score: number;
  aeo_score: number;
  geo_score: number;
  technical_score: number;
  content_score: number;
  word_count: number;
  response_time_ms: number;
  created_at: string;
}
