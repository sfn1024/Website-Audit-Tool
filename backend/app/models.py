"""
Pydantic models for request/response schemas.
Defines the exact shape of data flowing through the API.
"""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, HttpUrl


# ── Request ──────────────────────────────────────────────────────────────────

class AuditRequest(BaseModel):
    """Incoming audit request — just a URL."""
    url: HttpUrl


# ── Metrics sub-models ───────────────────────────────────────────────────────

class HeadingCounts(BaseModel):
    """Count of each heading level on the page."""
    h1: int
    h2: int
    h3: int


class LinkCounts(BaseModel):
    """Internal vs external link breakdown."""
    internal: int
    external: int


class ImageStats(BaseModel):
    """Image statistics including accessibility gaps."""
    total: int
    missing_alt_pct: float


class MetaInfo(BaseModel):
    """Meta tag information extracted from <head>."""
    title: str | None = None
    description: str | None = None
    title_length: int | None = None
    description_length: int | None = None


class PageMetrics(BaseModel):
    """All factual metrics extracted from the page."""
    word_count: int
    heading_counts: HeadingCounts
    cta_count: int
    links: LinkCounts
    images: ImageStats
    meta: MetaInfo


# ── AI Insights sub-models ───────────────────────────────────────────────────

class Recommendation(BaseModel):
    """A single prioritized recommendation from the AI."""
    priority: int
    title: str
    reasoning: str
    action: str


class AIInsights(BaseModel):
    """Structured AI analysis output from Gemini."""
    seo_analysis: str
    messaging_clarity: str
    cta_usage: str
    content_depth: str
    ux_concerns: str
    recommendations: list[Recommendation]


# ── Response ─────────────────────────────────────────────────────────────────

class AuditResponse(BaseModel):
    """Full audit response returned to the frontend."""
    url: str
    scraped_at: datetime
    metrics: PageMetrics
    insights: AIInsights | None = None
