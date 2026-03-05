"""
Metrics extraction module — extracts factual, deterministic metrics from HTML.

No AI involved. Purely parses the DOM using BeautifulSoup and returns
structured data matching the PageMetrics Pydantic model.
"""

import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from app.models import (
    HeadingCounts,
    ImageStats,
    LinkCounts,
    MetaInfo,
    PageMetrics,
)


# ── CTA Detection Heuristics ────────────────────────────────────────────────

# CSS class substrings that typically indicate a CTA element
CTA_CLASS_KEYWORDS = {"btn", "cta", "button", "action", "primary"}

# Link text patterns that indicate a call-to-action
CTA_TEXT_PATTERNS = re.compile(
    r"\b(get started|sign up|sign in|register|subscribe|buy now|shop now|"
    r"try free|start free|download|learn more|contact us|book a demo|"
    r"request demo|join now|apply now|add to cart|enroll|donate)\b",
    re.IGNORECASE,
)


def _is_cta_link(tag) -> bool:
    """Check if an <a> tag looks like a CTA based on classes or text."""
    # Check CSS classes
    classes = " ".join(tag.get("class", [])).lower()
    if any(keyword in classes for keyword in CTA_CLASS_KEYWORDS):
        return True

    # Check role="button"
    if tag.get("role", "").lower() == "button":
        return True

    # Check link text against CTA patterns
    text = tag.get_text(strip=True)
    if CTA_TEXT_PATTERNS.search(text):
        return True

    return False


# ── Main Extraction Function ────────────────────────────────────────────────

def extract_metrics(html: str, base_url: str) -> PageMetrics:
    """
    Parse HTML and extract all factual page metrics.

    Args:
        html: Raw HTML string of the page.
        base_url: The original URL, used to distinguish internal vs external links.

    Returns:
        A PageMetrics model with all extracted data.
    """
    soup = BeautifulSoup(html, "lxml")
    base_domain = urlparse(str(base_url)).netloc

    # ── Word count ───────────────────────────────────────────────────────
    # Get visible text only (strip all tags), split on whitespace, count
    visible_text = soup.get_text(separator=" ", strip=True)
    word_count = len(visible_text.split())

    # ── Heading counts ───────────────────────────────────────────────────
    heading_counts = HeadingCounts(
        h1=len(soup.find_all("h1")),
        h2=len(soup.find_all("h2")),
        h3=len(soup.find_all("h3")),
    )

    # ── CTA count ────────────────────────────────────────────────────────
    # Count all <button> elements
    buttons = soup.find_all("button")
    cta_count = len(buttons)

    # Count <a> tags that look like CTAs (by class, role, or text)
    for a_tag in soup.find_all("a", href=True):
        if _is_cta_link(a_tag):
            cta_count += 1

    # ── Link counts (internal vs external) ───────────────────────────────
    internal_links = 0
    external_links = 0

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()

        # Skip non-HTTP schemes (mailto:, tel:, javascript:, #anchors)
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue

        # Resolve relative URLs against the base URL
        absolute_url = urljoin(str(base_url), href)
        link_domain = urlparse(absolute_url).netloc

        if link_domain == base_domain:
            internal_links += 1
        else:
            external_links += 1

    links = LinkCounts(internal=internal_links, external=external_links)

    # ── Image stats ──────────────────────────────────────────────────────
    images = soup.find_all("img")
    total_images = len(images)

    # Count images where alt is missing or empty string
    missing_alt = sum(
        1 for img in images
        if not img.get("alt", "").strip()
    )

    missing_alt_pct = round(
        (missing_alt / total_images * 100) if total_images > 0 else 0.0,
        1,
    )

    image_stats = ImageStats(total=total_images, missing_alt_pct=missing_alt_pct)

    # ── Meta tags ────────────────────────────────────────────────────────
    # Meta title — from <title> tag
    title_tag = soup.find("title")
    meta_title = title_tag.get_text(strip=True) if title_tag else None

    # Meta description — from <meta name="description">
    desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    meta_description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else None

    meta = MetaInfo(
        title=meta_title,
        description=meta_description,
        title_length=len(meta_title) if meta_title else None,
        description_length=len(meta_description) if meta_description else None,
    )

    # ── Assemble and return ──────────────────────────────────────────────
    return PageMetrics(
        word_count=word_count,
        heading_counts=heading_counts,
        cta_count=cta_count,
        links=links,
        images=image_stats,
        meta=meta,
    )
