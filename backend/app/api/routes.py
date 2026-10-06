import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlmodel import Session, select
from bs4 import BeautifulSoup

from app.database import get_session
from app.models import AuditRecord
from app.schemas import AnalyzeRequest, AuditResponse
from app.analyzer.fetcher import fetch_webpage
from app.analyzer.seo_analyzer import (
    analyze_metadata, analyze_headings, analyze_content,
    analyze_links, analyze_images, analyze_technical
)
from app.analyzer.aeo_analyzer import analyze_aeo
from app.analyzer.geo_analyzer import analyze_geo
from app.analyzer.schema_analyzer import analyze_schemas
from app.analyzer.scoring import calculate_scores
from app.analyzer.ai_engine import enrich_with_ai_insights
from app.analyzer.pdf_generator import generate_pdf_report

router = APIRouter()

@router.post("/analyze", response_model=AuditResponse)
async def analyze_url(req: AnalyzeRequest, db: Session = Depends(get_session)):
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    # Fetch webpage html & latency
    fetch_res = await fetch_webpage(url)
    if not fetch_res.get("success"):
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch webpage: {fetch_res.get('error', 'Network error or invalid domain')}"
        )

    html = fetch_res.get("html", "")
    domain = fetch_res.get("domain", "")
    final_url = fetch_res.get("final_url", url)

    soup = BeautifulSoup(html, "lxml")

    # Perform audits
    meta = analyze_metadata(soup, final_url)
    headings = analyze_headings(soup)
    content = analyze_content(soup)
    links = analyze_links(soup, final_url, domain)
    images = analyze_images(soup)
    tech = analyze_technical(fetch_res, soup)
    
    top_kw_list = [k.keyword for k in content.top_keywords]
    aeo = analyze_aeo(soup, meta.title or "", top_kw_list)
    geo = analyze_geo(soup, meta.title or "", domain)
    schemas = analyze_schemas(soup)

    # CalculateScores
    scores = calculate_scores(meta, headings, content, links, images, tech, aeo, geo, schemas)

    # AI Insights & Action Plan Recommendations
    recs, ai_powered = await enrich_with_ai_insights(
        url=final_url,
        meta_title=meta.title or "",
        scores=scores,
        missing_alt_count=images.missing_alt_count,
        h1_count=headings.h1_count,
        is_https=tech.is_https,
        has_viewport=tech.has_mobile_viewport,
        has_org_schema=schemas.has_organization_schema,
        has_faq_schema=schemas.has_faq_schema,
        word_count=content.word_count
    )

    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    audit_payload = {
        "url": final_url,
        "domain": domain,
        "analyzed_at": now_str,
        "scores": scores.model_dump(),
        "meta": meta.model_dump(),
        "headings": headings.model_dump(),
        "content": content.model_dump(),
        "links": links.model_dump(),
        "images": images.model_dump(),
        "technical": tech.model_dump(),
        "aeo": aeo.model_dump(),
        "geo": geo.model_dump(),
        "structured_data": schemas.model_dump(),
        "recommendations": [r.model_dump() for r in recs],
        "ai_powered": ai_powered
    }

    # Save into DB
    db_record = AuditRecord(
        url=final_url,
        domain=domain,
        title=meta.title,
        overall_score=scores.overall,
        seo_score=scores.seo,
        aeo_score=scores.aeo,
        geo_score=scores.geo,
        technical_score=scores.technical,
        content_score=scores.content,
        word_count=content.word_count,
        response_time_ms=tech.response_time_ms,
        data_json=json.dumps(audit_payload)
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    audit_payload["id"] = db_record.id
    return audit_payload

@router.get("/audits")
def get_audit_history(limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_session)):
    statement = select(AuditRecord).order_by(AuditRecord.created_at.desc()).limit(limit)
    records = db.exec(statement).all()
    return [
        {
            "id": r.id,
            "url": r.url,
            "domain": r.domain,
            "title": r.title,
            "overall_score": r.overall_score,
            "seo_score": r.seo_score,
            "aeo_score": r.aeo_score,
            "geo_score": r.geo_score,
            "technical_score": r.technical_score,
            "content_score": r.content_score,
            "word_count": r.word_count,
            "response_time_ms": r.response_time_ms,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for r in records
    ]

@router.get("/audit/{audit_id}")
def get_audit_by_id(audit_id: int, db: Session = Depends(get_session)):
    record = db.get(AuditRecord, audit_id)
    if not record:
        raise HTTPException(status_code=404, detail="Audit record not found")
    data = json.loads(record.data_json)
    data["id"] = record.id
    return data

@router.get("/audit/{audit_id}/pdf")
def download_audit_pdf(audit_id: int, db: Session = Depends(get_session)):
    record = db.get(AuditRecord, audit_id)
    if not record:
        raise HTTPException(status_code=404, detail="Audit record not found")
    data = json.loads(record.data_json)
    
    pdf_bytes = generate_pdf_report(data)
    filename = f"SEO_Intelligence_Report_{record.domain}_{audit_id}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
