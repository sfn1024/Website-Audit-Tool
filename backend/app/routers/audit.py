"""
Audit router — the single POST /audit endpoint.

Orchestrates the scraping → metrics extraction → AI analysis pipeline.
"""

from datetime import datetime, timezone

from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException

from app.models import AuditRequest, AuditResponse, AIInsights
from app.services.scraper import ScrapeError, scrape_url
from app.services.metrics import extract_metrics
from app.services.ai_analyzer import AnalysisError, analyze_page

router = APIRouter()


def _extract_visible_text(html: str) -> str:
    """Extract visible text from HTML for the AI analyzer."""
    soup = BeautifulSoup(html, "lxml")

    # Remove script and style elements
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text(separator=" ", strip=True)


@router.post("/audit", response_model=AuditResponse)
async def audit_url(request: AuditRequest):
    """
    Audit a single URL.

    1. Scrapes the page HTML
    2. Extracts factual metrics
    3. Sends metrics + page text to Gemini for AI analysis
    4. Returns structured JSON with metrics and insights
    """

    # ── Step 1: Scrape the page ──────────────────────────────────────────
    try:
        scrape_result = await scrape_url(str(request.url))
        html = scrape_result["html"]
    except ScrapeError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    # ── Step 2: Extract metrics ──────────────────────────────────────────
    try:
        metrics = extract_metrics(html, str(request.url))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract metrics: {str(e)}",
        )

    # ── Step 3: AI analysis via Gemini ───────────────────────────────────
    page_text = _extract_visible_text(html)
    insights = None

    try:
        insights_dict = await analyze_page(metrics, page_text, str(request.url))
        insights = AIInsights(**insights_dict)
    except AnalysisError as e:
        # AI failure is non-fatal — return metrics without insights
        print(f"[WARN] AI analysis failed: {e.message}")
    except Exception as e:
        print(f"[WARN] Unexpected AI error: {str(e)}")

    # ── Step 4: Build and return the response ────────────────────────────
    return AuditResponse(
        url=str(request.url),
        scraped_at=datetime.now(timezone.utc),
        metrics=metrics,
        insights=insights,
    )
