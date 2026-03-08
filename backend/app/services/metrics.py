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
    r"request demo|join now|apply now|add to cart|enroll|donate|"
    r"get in touch|let's talk|lets talk|book a call|get a quote|"
    r"schedule a call|free trial|view demo|see pricing|talk to us|"
    r"get access|request a quote|watch demo|explore now)\b",
    re.IGNORECASE,
)


def _is_cta_link(tag) -> bool:
    """Check if an <a>, <div>, or <span> tag looks like a CTA."""
    # Check CSS classes
    classes = " ".join(tag.get("class", [])).lower()
    if any(keyword in classes for keyword in CTA_CLASS_KEYWORDS):
        return True

    # Check role="button" (works for <a>, <div>, <span>)
    if tag.get("role", "").lower() == "button":
        return True

    # For <a> tags, check href for "contact"
    if tag.name == "a":
        href = tag.get("href", "").lower()
        if "contact" in href:
            return True

    # Check text against CTA patterns
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
        base_url: The original URL.

    Returns:
        A PageMetrics model with all extracted data.
    """
    soup = BeautifulSoup(html, "lxml")
    base_domain = urlparse(str(base_url)).netloc

    # ── Word count (Cleaned) ─────────────────────────────────────────────
    # Create a copy for cleaning to avoid affecting other metrics
    clean_soup = BeautifulSoup(html, "lxml")
    
    # 1. Remove non-content tags
    for tag in clean_soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.decompose()
    
    # 2. Remove aria-hidden elements
    for tag in clean_soup.find_all(attrs={"aria-hidden": "true"}):
        tag.decompose()
        
    # 3. Remove inline-hidden elements (display:none or visibility:hidden)
    for tag in clean_soup.find_all(style=re.compile(r"display\s*:\s*none|visibility\s*:\s*hidden", re.I)):
        tag.decompose()

    visible_text = clean_soup.get_text(separator=" ", strip=True)
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

    # Count <a> tags that look like CTAs
    for a_tag in soup.find_all("a", href=True):
        if _is_cta_link(a_tag):
            cta_count += 1
            
    # Count <div> and <span> tags with role="button"
    for tag in soup.find_all(["div", "span"], role="button"):
        if _is_cta_link(tag): # Avoid double counting if already caught by other logic
            cta_count += 1

    # ── Link counts (internal vs external) ───────────────────────────────
    internal_links = 0
    external_links = 0

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        absolute_url = urljoin(str(base_url), href)
        link_domain = urlparse(absolute_url).netloc
        if link_domain == base_domain:
            internal_links += 1
        else:
            external_links += 1

    links = LinkCounts(internal=internal_links, external=external_links)

    # ── Image stats ──────────────────────────────────────────────────────
    img_tags = soup.find_all("img")

    excluded_parents = {"template", "noscript"}
    tracking_keywords = {"pixel", "tracking", "beacon"}
    
    clean_img_tags = []
    for img in img_tags:
        # 1. Skip if inside <template> or <noscript>
        if any(p.name in excluded_parents for p in img.parents):
            continue
        
        # Get dimensions and attributes for filtering
        width = img.get("width", "").strip()
        height = img.get("height", "").strip()
        src = img.get("src", "").lower()
        style = img.get("style", "").lower()
        
        # 2. Skip tracking pixels (1x1 or 0x0)
        if width in ("0", "1") or height in ("0", "1"):
            continue
            
        # 3. Skip images with tracking keywords in URL
        if any(kw in src for kw in tracking_keywords):
            continue
            
        # 4. Skip hidden images
        if "display:none" in style.replace(" ", "") or "visibility:hidden" in style.replace(" ", ""):
            continue
            
        clean_img_tags.append(img)

    total_images = len(clean_img_tags)
    missing_alt = sum(
        1 for img in clean_img_tags
        if not img.get("alt", "").strip()
    )

    missing_alt_pct = round(
        (missing_alt / total_images * 100) if total_images > 0 else 0.0,
        1,
    )

    image_stats = ImageStats(total=total_images, missing_alt_pct=missing_alt_pct)

    # ── Meta tags ────────────────────────────────────────────────────────
    title_tag = soup.find("title")
    meta_title = title_tag.get_text(strip=True) if title_tag else None
    desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    meta_description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else None

    meta = MetaInfo(
        title=meta_title,
        description=meta_description,
        title_length=len(meta_title) if meta_title else None,
        description_length=len(meta_description) if meta_description else None,
    )

    return PageMetrics(
        word_count=word_count,
        heading_counts=heading_counts,
        cta_count=cta_count,
        links=links,
        images=image_stats,
        meta=meta,
    )
