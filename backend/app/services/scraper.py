"""
Scraper module — fetches raw HTML from a given URL.

Handles:
- Async HTTP requests with timeout
- Redirect following (capped at 5)
- Content-Type validation (rejects non-HTML)
- HTML size capping (5 MB max)
- Encoding detection with utf-8 fallback
"""

import httpx
from app.config import settings


# Custom exception for scraper-specific errors
class ScrapeError(Exception):
    """Raised when scraping fails for any reason."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# Realistic User-Agent to reduce bot-blocking
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


async def _fetch(url: str, verify_ssl: bool = True):
    """
    Internal helper — performs the actual HTTP GET request.

    Returns the httpx.Response on success, or None if an SSL error occurs
    (so the caller can retry without SSL verification).

    Raises ScrapeError for non-SSL failures (timeout, redirects, network).
    """
    try:
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(settings.scrape_timeout),
            follow_redirects=True,
            max_redirects=settings.max_redirects,
            headers={"User-Agent": USER_AGENT},
            verify=verify_ssl,
        ) as client:
            return await client.get(str(url))

    except httpx.TimeoutException:
        raise ScrapeError(
            "Request timed out while fetching the URL.",
            status_code=408,
        )
    except httpx.TooManyRedirects:
        raise ScrapeError(
            "Too many redirects — possible redirect loop.",
            status_code=400,
        )
    except Exception as e:
        # If it's an SSL-related error, return None so caller can retry
        error_str = str(e).lower()
        if "ssl" in error_str or "certificate" in error_str:
            return None
        raise ScrapeError(
            f"Unable to fetch the URL: {str(e)}",
            status_code=400,
        )


async def scrape_url(url: str) -> str:
    """
    Fetch the raw HTML content of a URL.

    Args:
        url: The URL to scrape (must be http/https).

    Returns:
        The HTML content as a string.

    Raises:
        ScrapeError: If the URL is unreachable, times out,
                     returns non-HTML, or exceeds size limits.
    """
    response = await _fetch(url, verify_ssl=True)
    if response is None:
        # SSL failed — retry without verification (common in dev environments)
        response = await _fetch(url, verify_ssl=False)

    if response is None:
        raise ScrapeError("Unable to fetch the URL.", status_code=400)

    # --- Validate the response ---

    # Check for HTTP errors (4xx, 5xx)
    if response.status_code >= 400:
        raise ScrapeError(
            f"The server returned HTTP {response.status_code}.",
            status_code=400,
        )

    # Ensure the response is HTML, not a PDF/image/etc.
    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type and "application/xhtml" not in content_type:
        raise ScrapeError(
            f"The URL returned non-HTML content (Content-Type: {content_type}).",
            status_code=400,
        )

    # Cap HTML size to prevent processing massive pages
    if len(response.content) > settings.max_html_size:
        raise ScrapeError(
            "The page is too large to process (exceeds 5 MB).",
            status_code=400,
        )

    # Decode the HTML — httpx handles encoding detection automatically,
    # but we fallback to utf-8 if it fails
    try:
        html = response.text
    except Exception:
        html = response.content.decode("utf-8", errors="replace")

    return html
