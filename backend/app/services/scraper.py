import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

from app.config import settings


# Custom exception for scraper-specific errors
class ScrapeError(Exception):
    """Raised when scraping fails for any reason."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


async def scrape_url(url: str) -> dict:
    """
    Fetch the fully rendered HTML content and network stats of a URL using Playwright.
    
    This handles:
    - JavaScript execution
    - Network request monitoring (for accurate image counts)
    - Network idle waiting
    - Automated scrolling for lazy-loaded content

    Returns:
        A dictionary containing "html" (str) and "network_image_count" (int).
    """
    image_urls = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            # Create a context with a realistic User-Agent
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            # Monitor network requests to count images accurately
            async def handle_request(request):
                if request.resource_type == "image":
                    image_urls.add(request.url)

            page.on("request", handle_request)

            # Navigate with a specific timeout
            try:
                # 1. Initial navigation (wait for DOM)
                await page.goto(str(url), wait_until="domcontentloaded", timeout=60000)
                
                # 2. Try to wait for network to be idle, but fall back if it takes too long
                try:
                    await page.wait_for_load_state("networkidle", timeout=60000)
                except PlaywrightTimeoutError:
                    print(f"[WARN] Networkidle timed out for {url}, proceeding with DOM content.")
                    
            except PlaywrightTimeoutError:
                raise ScrapeError("Request timed out while fetching the URL (60s limit).", status_code=408)
            except Exception as e:
                raise ScrapeError(f"Unable to fetch the URL: {str(e)}", status_code=400)

            # --- Handle Lazy-loaded Content ---
            # Scroll in steps of 800px to trigger all lazy-loaded images
            current_pos = 0
            while True:
                # Get current scroll height
                total_height = await page.evaluate("document.body.scrollHeight")
                if current_pos >= total_height:
                    break
                
                current_pos += 800
                await page.evaluate(f"window.scrollTo(0, {current_pos})")
                await asyncio.sleep(0.5) # Wait for images to trigger

            # Wait 2 seconds at the bottom for final loads
            await asyncio.sleep(2)

            # Scroll back to top
            await page.evaluate("window.scrollTo(0, 0)")
            
            # Final settle time for images/scripts to render
            await asyncio.sleep(2)

            # Extract the fully rendered HTML
            html = await page.content()

            # --- Basics Validations ---
            if not html or len(html.strip()) == 0:
                raise ScrapeError("The page returned empty content.", status_code=400)

            # Cap HTML size to prevent processing massive pages
            if len(html.encode("utf-8")) > settings.max_html_size:
                raise ScrapeError(
                    "The page is too large to process (exceeds 15 MB).",
                    status_code=400,
                )

            return {
                "html": html,
                "network_image_count": len(image_urls)
            }

        finally:
            await browser.close()
