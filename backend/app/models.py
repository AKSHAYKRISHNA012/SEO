from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class AuditRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True)
    domain: str = Field(index=True)
    title: Optional[str] = None
    overall_score: int
    seo_score: int
    aeo_score: int
    geo_score: int
    technical_score: int
    content_score: int
    word_count: int = 0
    response_time_ms: int = 0
    created_at: datetime = Field(default_factory=get_utc_now)
    data_json: str
