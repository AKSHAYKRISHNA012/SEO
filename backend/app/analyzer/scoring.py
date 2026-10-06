from app.schemas import (
    MetaDataAnalysis, HeadingAnalysis, ContentAnalysis, LinkAnalysis,
    ImageAnalysis, TechnicalSEOAnalysis, AEOAnalysis, GEOAnalysis, StructuredDataAnalysis,
    ScoreBreakdown
)

def calculate_scores(
    meta: MetaDataAnalysis,
    headings: HeadingAnalysis,
    content: ContentAnalysis,
    links: LinkAnalysis,
    images: ImageAnalysis,
    technical: TechnicalSEOAnalysis,
    aeo: AEOAnalysis,
    geo: GEOAnalysis,
    schema: StructuredDataAnalysis
) -> ScoreBreakdown:
    # 1. Traditional SEO Score (0-100)
    seo_pts = 0
    if meta.title_status == "Optimal":
        seo_pts += 25
    elif meta.title_status in ["Too Short", "Too Long"]:
        seo_pts += 15

    if meta.description_status == "Optimal":
        seo_pts += 25
    elif meta.description_status in ["Too Short", "Too Long"]:
        seo_pts += 15

    if meta.canonical_matches:
        seo_pts += 15
    if meta.is_indexable:
        seo_pts += 15

    if headings.h1_count == 1:
        seo_pts += 10
    elif headings.h1_count > 1:
        seo_pts += 5

    if images.total_images > 0:
        alt_pct = images.images_with_alt_count / images.total_images
        seo_pts += int(alt_pct * 10)
    else:
        seo_pts += 10

    seo_score = min(100, max(10, seo_pts))

    # 2. Technical Score (0-100)
    tech_pts = 0
    if technical.is_https:
        tech_pts += 25
    if technical.has_mobile_viewport:
        tech_pts += 25
    if technical.robots_txt_found:
        tech_pts += 15
    if technical.sitemap_xml_found:
        tech_pts += 15
    if technical.response_time_ms < 800:
        tech_pts += 20
    elif technical.response_time_ms < 2000:
        tech_pts += 12
    else:
        tech_pts += 5

    technical_score = min(100, max(10, tech_pts))

    # 3. Content Score (0-100)
    cnt_pts = 0
    if content.word_count >= 1000:
        cnt_pts += 30
    elif content.word_count >= 500:
        cnt_pts += 20
    else:
        cnt_pts += 10

    if content.reading_ease_score >= 50:
        cnt_pts += 25
    else:
        cnt_pts += 15

    if content.paragraph_count >= 5:
        cnt_pts += 25
    else:
        cnt_pts += 15

    if not content.has_repeated_text:
        cnt_pts += 10
    if content.freshness_signals:
        cnt_pts += 10

    content_score = min(100, max(10, cnt_pts))

    # 4. AEO Score (0-100)
    aeo_score = aeo.aeo_readiness_score

    # 5. GEO Score (0-100)
    geo_pts = int((geo.ai_readability_score * 0.4) + (geo.factual_density_score * 0.4))
    if geo.trust_signals:
        geo_pts += len(geo.trust_signals) * 5
    if schema.has_organization_schema:
        geo_pts += 10
    geo_score = min(100, max(10, geo_pts))

    # 6. Overall Weighted Score (0-100)
    overall = int(
        (seo_score * 0.25) +
        (aeo_score * 0.20) +
        (geo_score * 0.20) +
        (technical_score * 0.20) +
        (content_score * 0.15)
    )

    return ScoreBreakdown(
        overall=overall,
        seo=seo_score,
        aeo=aeo_score,
        geo=geo_score,
        technical=technical_score,
        content=content_score
    )
