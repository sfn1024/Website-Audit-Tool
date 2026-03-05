# BLUEPRINT — AI-Powered Website Audit Tool

> **Version:** 1.0
> **Date:** 2026-03-05
> **Stack:** Python + FastAPI · React + Vite + Plain CSS · Gemini 2.5 Flash

---

## Table of Contents

1. [High-Level Architecture](#1-high-level-architecture)
2. [Folder Structure](#2-folder-structure)
3. [API Contract](#3-api-contract)
4. [Module Design](#4-module-design)
5. [Dependencies](#5-dependencies)
6. [Edge Cases & Gotchas](#6-edge-cases--gotchas)
7. [Data Flow Diagram](#7-data-flow-diagram)

---

## 1. High-Level Architecture

```
┌──────────────┐      HTTP POST       ┌──────────────────────────────────────────────┐
│              │  ─────────────────►   │  FastAPI Backend                             │
│   React UI   │                      │                                              │
│  (Vite SPA)  │  ◄─────────────────  │  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│              │    JSON Response      │  │ Scraper  │─►│ Metrics  │─►│ AI Module │  │
└──────────────┘                      │  │ Module   │  │ Extractor│  │ (Gemini)  │  │
                                      │  └──────────┘  └──────────┘  └───────────┘  │
                                      └──────────────────────────────────────────────┘
```

**Flow:** User enters a URL → Frontend sends `POST /api/audit` → Backend scrapes the page → Extracts factual metrics → Sends metrics + content to Gemini 2.5 Flash → Returns structured JSON → Frontend renders the audit report.

---

## 2. Folder Structure

```
Assessment-2/
├── docs/
│   └── BLUEPRINT.md              # This document — architecture reference
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app entry point, CORS config
│   │   ├── config.py             # Environment variables, API keys, settings
│   │   ├── models.py             # Pydantic request/response schemas
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── audit.py          # /api/audit endpoint
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── scraper.py        # URL fetching and HTML retrieval
│   │       ├── metrics.py        # Factual metrics extraction from HTML
│   │       └── analyzer.py       # Gemini 2.5 Flash integration
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Template for environment variables
│   └── .env                      # Local env vars (gitignored)
│
├── frontend/
│   ├── index.html                # Vite entry HTML
│   ├── package.json
│   ├── vite.config.js
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── main.jsx              # React DOM mount
│   │   ├── App.jsx               # Root component, routing (if any)
│   │   ├── index.css             # Global styles, CSS variables, reset
│   │   ├── components/
│   │   │   ├── UrlInput.jsx      # URL input form
│   │   │   ├── UrlInput.css
│   │   │   ├── AuditReport.jsx   # Full audit result display
│   │   │   ├── AuditReport.css
│   │   │   ├── MetricsCard.jsx   # Individual metric display card
│   │   │   ├── MetricsCard.css
│   │   │   ├── InsightSection.jsx # AI insight category display
│   │   │   ├── InsightSection.css
│   │   │   ├── Loader.jsx        # Loading state / skeleton
│   │   │   └── Loader.css
│   │   └── utils/
│   │       └── api.js            # Fetch wrapper for /api/audit
│   └── .env                      # VITE_API_URL (gitignored)
│
├── .gitignore
└── README.md
```

---

## 3. API Contract

### `POST /api/audit`

#### Request Body

```json
{
  "url": "https://example.com/landing-page"
}
```

| Field | Type   | Required | Validation                                      |
| ----- | ------ | -------- | ------------------------------------------------ |
| `url` | string | ✅        | Must be a valid HTTP/HTTPS URL, max 2048 chars   |

#### Success Response — `200 OK`

```json
{
  "url": "https://example.com/landing-page",
  "scraped_at": "2026-03-05T12:00:00Z",
  "metrics": {
    "word_count": 1245,
    "heading_counts": {
      "h1": 1,
      "h2": 5,
      "h3": 8
    },
    "cta_count": 4,
    "links": {
      "internal": 12,
      "external": 7
    },
    "images": {
      "total": 9,
      "missing_alt_pct": 33.3
    },
    "meta": {
      "title": "Example — Best Landing Page",
      "description": "A great landing page for your needs.",
      "title_length": 34,
      "description_length": 42
    }
  },
  "ai_analysis": {
    "seo_structure": {
      "score": "Good",
      "summary": "The page has a proper H1 and logical heading hierarchy...",
      "details": ["Only one H1 tag present — correct.", "H2s used for major sections..."]
    },
    "messaging_clarity": {
      "score": "Needs Improvement",
      "summary": "The value proposition is buried below the fold...",
      "details": ["Headline is vague...", "Subheadline restates the headline..."]
    },
    "cta_usage": {
      "score": "Good",
      "summary": "4 CTAs found with reasonable placement...",
      "details": ["Primary CTA is above the fold...", "Consider differentiating secondary CTAs..."]
    },
    "content_depth": {
      "score": "Moderate",
      "summary": "1245 words is adequate for a landing page...",
      "details": ["Content covers features but lacks social proof...", "FAQ section is missing..."]
    },
    "ux_structural_concerns": {
      "score": "Needs Improvement",
      "summary": "33% of images lack alt text, harming accessibility...",
      "details": ["Add descriptive alt text to all images...", "Consider lazy-loading below-fold images..."]
    },
    "recommendations": [
      {
        "priority": 1,
        "title": "Add alt text to all images",
        "description": "33% of images are missing alt text. This hurts SEO and accessibility."
      },
      {
        "priority": 2,
        "title": "Strengthen the hero headline",
        "description": "The current H1 is generic. Make it specific to the value proposition."
      },
      {
        "priority": 3,
        "title": "Add social proof section",
        "description": "The page lacks testimonials, case studies, or trust badges."
      }
    ]
  }
}
```

#### Error Responses

| Status | Body                                                     | Scenario                            |
| ------ | -------------------------------------------------------- | ----------------------------------- |
| `422`  | `{ "detail": "Invalid URL format" }`                     | Malformed URL                       |
| `400`  | `{ "detail": "Unable to fetch the URL" }`                | Connection error, DNS failure, etc. |
| `408`  | `{ "detail": "Request timed out while fetching the URL" }` | Scrape exceeds timeout threshold  |
| `500`  | `{ "detail": "AI analysis failed" }`                     | Gemini API error                    |

---

## 4. Module Design

The backend is split into **three isolated service modules**, each with a single responsibility. They communicate through well-defined Python data models (Pydantic).

### 4.1 `scraper.py` — URL Fetching

**Responsibility:** Accept a URL, fetch the raw HTML, handle network errors.

| Concern              | Approach                                                               |
| -------------------- | ---------------------------------------------------------------------- |
| HTTP client          | `httpx` (async-native, timeout support)                                |
| User-Agent           | Rotate a realistic User-Agent string to avoid bot blocks               |
| Timeout              | 15-second hard timeout for the HTTP request                            |
| Redirects            | Follow up to 5 redirects                                               |
| Encoding             | Detect charset from headers/meta, fallback to `utf-8`                  |
| Error handling       | Raise custom `ScrapeError` with descriptive message                    |

```python
# Signature
async def scrape_url(url: str) -> ScrapeResult:
    """Returns ScrapeResult(html=str, final_url=str, status_code=int)"""
```

### 4.2 `metrics.py` — Factual Metrics Extraction

**Responsibility:** Parse HTML with BeautifulSoup, extract all factual metrics. **No AI involved here — purely deterministic.**

| Metric                  | Extraction Logic                                                            |
| ----------------------- | --------------------------------------------------------------------------- |
| Word count              | Strip all tags → split on whitespace → count                                |
| H1 / H2 / H3 counts    | `soup.find_all('h1')`, etc.                                                 |
| CTA count               | Count `<button>` elements + `<a>` tags with CTA-like classes/text patterns  |
| Internal vs external    | Compare each `<a href>` domain against the input URL's domain               |
| Image count             | `soup.find_all('img')`                                                      |
| Images missing alt (%)  | Filter images where `alt` attr is missing or empty → percentage             |
| Meta title              | `soup.find('title')` → `.string`                                            |
| Meta description        | `soup.find('meta', attrs={'name': 'description'})` → `['content']`         |

```python
# Signature
def extract_metrics(html: str, base_url: str) -> PageMetrics:
    """Returns a PageMetrics Pydantic model with all factual data."""
```

### 4.3 `analyzer.py` — Gemini AI Integration

**Responsibility:** Build a structured prompt from the metrics + page content, send to Gemini 2.5 Flash, parse the structured response.

| Concern               | Approach                                                                    |
| ---------------------- | --------------------------------------------------------------------------- |
| SDK                    | `google-generativeai` (official Gemini Python SDK)                         |
| Prompt design          | System prompt defines the audit persona; user message includes metrics JSON + truncated page text |
| Structured output      | Instruct Gemini to respond in a strict JSON schema; parse with Pydantic     |
| Content truncation     | Truncate page text to ~8,000 words to stay within token limits              |
| Retry logic            | Retry up to 2 times on transient Gemini API errors                          |
| Error handling         | Raise custom `AnalysisError` on failure after retries                       |

```python
# Signature
async def analyze_page(metrics: PageMetrics, page_text: str) -> AIAnalysis:
    """Returns an AIAnalysis Pydantic model with all AI insights."""
```

### 4.4 `audit.py` (Router) — Orchestration

The router ties the three services together:

```python
@router.post("/api/audit")
async def audit_url(request: AuditRequest) -> AuditResponse:
    # 1. Scrape
    scrape_result = await scrape_url(request.url)

    # 2. Extract metrics
    metrics = extract_metrics(scrape_result.html, request.url)

    # 3. Get visible text for AI
    page_text = extract_visible_text(scrape_result.html)

    # 4. AI analysis
    ai_analysis = await analyze_page(metrics, page_text)

    # 5. Return combined response
    return AuditResponse(
        url=request.url,
        scraped_at=datetime.utcnow(),
        metrics=metrics,
        ai_analysis=ai_analysis
    )
```

---

## 5. Dependencies

### 5.1 Python (`backend/requirements.txt`)

| Package                    | Purpose                                    |
| -------------------------- | ------------------------------------------ |
| `fastapi`                  | Web framework                              |
| `uvicorn[standard]`       | ASGI server                                |
| `httpx`                    | Async HTTP client for scraping             |
| `beautifulsoup4`           | HTML parsing and metrics extraction        |
| `lxml`                     | Fast HTML parser backend for BeautifulSoup |
| `google-generativeai`     | Official Gemini Python SDK                 |
| `pydantic`                 | Data validation (bundled with FastAPI)      |
| `pydantic-settings`        | Environment variable management            |
| `python-dotenv`            | `.env` file loading                        |

### 5.2 Node (`frontend/package.json`)

| Package              | Purpose                         |
| -------------------- | ------------------------------- |
| `react`              | UI library                      |
| `react-dom`          | React DOM rendering             |
| `vite`               | Build tool and dev server       |
| `@vitejs/plugin-react` | Vite plugin for React/JSX     |

> **No additional UI libraries.** Styling is done with plain CSS as specified. No Tailwind, no component library.

---

## 6. Edge Cases & Gotchas

### 6.1 Scraping

| Issue                        | Mitigation                                                                 |
| ---------------------------- | -------------------------------------------------------------------------- |
| **JS-rendered pages (SPAs)** | `httpx` fetches raw HTML only. JS-rendered content will be incomplete. Document this limitation to users. A future enhancement could use Playwright for JS rendering. |
| **Bot protection / CAPTCHAs** | Some sites block scrapers. Return a clear `400` error with a message like "Unable to access this page — it may be blocking automated requests." |
| **Very large pages**         | Cap HTML processing at 5 MB. Truncate page text for Gemini at ~8,000 words. |
| **Non-HTML responses**       | Check `Content-Type` header; reject PDFs, images, etc., with a `400` error. |
| **Encoding issues**          | Detect charset from HTTP headers and `<meta charset>`. Fallback to `utf-8`. |
| **Redirect loops**           | Cap redirects at 5; raise error on loop.                                    |
| **Slow responses**           | 15-second timeout on the HTTP fetch, 30-second timeout on Gemini API call.  |

### 6.2 Metrics Extraction

| Issue                         | Mitigation                                                                |
| ----------------------------- | ------------------------------------------------------------------------- |
| **Missing meta tags**         | Return `null` for `meta.title` and `meta.description` if absent; note "Missing" in the response. |
| **Missing `<h1>`**            | Report `h1: 0`. The AI analysis will flag this as an SEO issue.           |
| **Relative URLs in links**    | Resolve all `href` values against the base URL before classifying internal vs external. |
| **mailto: / tel: / javascript: links** | Exclude non-HTTP schemes from internal/external link counts.     |
| **CTA detection heuristics**  | Use a combination of: `<button>` tags, `<a>` tags with classes containing words like `btn`, `cta`, `button`, `action`, and `<a>` tags with role="button". Also match link text patterns like "Get Started", "Sign Up", "Buy Now", "Try Free", etc. |
| **`<img>` alt detection**     | Count `alt=""` (empty string) as missing alt text, same as absent `alt`.  |

### 6.3 AI / Gemini

| Issue                         | Mitigation                                                                |
| ----------------------------- | ------------------------------------------------------------------------- |
| **Rate limiting**             | Implement retry with exponential backoff (2 retries, 1s → 2s).           |
| **Malformed JSON from AI**    | Wrap Gemini response parsing in try/except. On parse failure, retry once with a stricter prompt. If still failing, return a generic error. |
| **Token limit exceeded**      | Truncate page text to ~8,000 words before sending. Metrics JSON is compact and won't hit limits. |
| **API key exposure**          | Store `GEMINI_API_KEY` in backend `.env` only. Never send to frontend. `.env` is gitignored. |

### 6.4 Frontend / Integration

| Issue                         | Mitigation                                                                |
| ----------------------------- | ------------------------------------------------------------------------- |
| **CORS**                      | Configure FastAPI `CORSMiddleware` to allow the Vite dev server origin (`http://localhost:5173`) in development and the production domain in production. |
| **Long processing time**      | Show a loading/skeleton state in the UI. The combined scrape + AI can take 10–20 seconds. Display a clear progress indicator. |
| **URL validation (frontend)** | Validate the URL format on the client side before sending to avoid unnecessary API calls. |
| **Error display**             | Map backend error codes to user-friendly messages in the UI.              |

---

## 7. Data Flow Diagram

```
User enters URL
       │
       ▼
┌──────────────────┐
│  UrlInput.jsx    │  Client-side URL validation
│  (Frontend)      │
└───────┬──────────┘
        │ POST /api/audit { "url": "..." }
        ▼
┌──────────────────┐
│  audit.py        │  Router / Orchestrator
│  (Backend)       │
└───────┬──────────┘
        │
        ├──────────────────────┐
        ▼                      │
┌──────────────────┐           │
│  scraper.py      │           │
│  Fetch raw HTML  │           │
└───────┬──────────┘           │
        │ raw HTML             │
        ▼                      │
┌──────────────────┐           │
│  metrics.py      │           │
│  Extract metrics │           │
└───────┬──────────┘           │
        │ PageMetrics +        │
        │ visible text         │
        ▼                      │
┌──────────────────┐           │
│  analyzer.py     │           │
│  Gemini 2.5 Flash│           │
└───────┬──────────┘           │
        │ AIAnalysis           │
        ▼                      │
┌──────────────────┐           │
│  Combine into    │◄──────────┘
│  AuditResponse   │
└───────┬──────────┘
        │ JSON
        ▼
┌──────────────────┐
│  AuditReport.jsx │  Render metrics cards + AI insights
│  (Frontend)      │
└──────────────────┘
```

---

## 8. Pydantic Models Reference

```python
# models.py — key schemas

class AuditRequest(BaseModel):
    url: HttpUrl

class HeadingCounts(BaseModel):
    h1: int
    h2: int
    h3: int

class LinkCounts(BaseModel):
    internal: int
    external: int

class ImageStats(BaseModel):
    total: int
    missing_alt_pct: float

class MetaInfo(BaseModel):
    title: str | None
    description: str | None
    title_length: int | None
    description_length: int | None

class PageMetrics(BaseModel):
    word_count: int
    heading_counts: HeadingCounts
    cta_count: int
    links: LinkCounts
    images: ImageStats
    meta: MetaInfo

class AnalysisCategory(BaseModel):
    score: str             # "Good", "Moderate", "Needs Improvement"
    summary: str
    details: list[str]

class Recommendation(BaseModel):
    priority: int
    title: str
    description: str

class AIAnalysis(BaseModel):
    seo_structure: AnalysisCategory
    messaging_clarity: AnalysisCategory
    cta_usage: AnalysisCategory
    content_depth: AnalysisCategory
    ux_structural_concerns: AnalysisCategory
    recommendations: list[Recommendation]  # 3–5 items

class AuditResponse(BaseModel):
    url: str
    scraped_at: datetime
    metrics: PageMetrics
    ai_analysis: AIAnalysis
```

---

## 9. Running the Project

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # Add your GEMINI_API_KEY
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                 # Runs on http://localhost:5173
```

### Environment Variables

| Variable          | Location         | Description                     |
| ----------------- | ---------------- | ------------------------------- |
| `GEMINI_API_KEY`  | `backend/.env`   | Google Gemini API key           |
| `VITE_API_URL`    | `frontend/.env`  | Backend URL (default: `http://localhost:8000`) |

---

> **This document is the single source of truth for the project's architecture. Reference it during implementation.**
