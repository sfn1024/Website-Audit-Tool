# Backend Test Results — Website Audit Tool

This document outlines the validation tests performed on the FastAPI backend (v1.0.0).

## 1. Environment Details
- **OS:** Linux
- **Python:** 3.x
- **Host:** `http://localhost:8000`
- **Scraper:** httpx (with SSL fallback)
- **Parser:** BeautifulSoup4 (lxml)

## 2. Successful Audits

### 2.1 HTTPS Audit: `https://example.com`
- **Result:** Pass ✅ (SSL fallback verified)
- **Response Shape:**
```json
{
    "url": "https://example.com/",
    "scraped_at": "2026-03-05T12:00:12.596225Z",
    "metrics": {
        "word_count": 21,
        "heading_counts": { "h1": 1, "h2": 0, "h3": 0 },
        "cta_count": 1,
        "links": { "internal": 0, "external": 1 },
        "images": { "total": 0, "missing_alt_pct": 0.0 },
        "meta": { "title": "Example Domain", "description": null }
    }
}
```

### 2.2 HTTP Audit: `http://info.cern.ch`
- **Result:** Pass ✅
- **Observations:** Correctly identified early web page structure (1 H1, specific link counts).

### 2.3 Health Check: `GET /`
- **Result:** Pass ✅
- **Response:** `{"status": "ok", "message": "Website Audit Tool API is running."}`

---

## 3. Error Handling Verification

| Test Case | Expected Status | Actual Status | Response Detail |
|-----------|-----------------|---------------|-----------------|
| Invalid URL Format | `422` | `422` ✅ | Pydantic validation error |
| Non-existent Domain | `400` | `400` ✅ | "[Errno -2] Name or service not known" |
| Timeout (Simulated) | `408` | N/A | Logged in code via `httpx.TimeoutException` |
| Non-HTML Content | `400` | N/A | Logged in code via `Content-Type` check |

---

## 4. Performance
- **Avg. Response Time:** 1.2s – 2.5s (Network bound)
- **Memory Usage:** Stable during concurrent scrapes.

---

## 5. AI Analysis Verification (Gemini 2.5 Flash)

### 5.1 Real-World Audit: `https://zero-loop.netlify.app/`
- **Result:** Pass ✅
- **Observations:** The AI successfully grounded its insights in the 790-word page content. It correctly identified high CTA density (25 CTAs) and recommended specific H1 refinements and internal linking strategies.

### 5.2 Graceful Fallback
- **Test:** API call with invalid/mock API key.
- **Result:** Pass ✅. System returns factual metrics with `insights: null` and logs a warning, ensuring the tool remains functional even if the AI layer fails.

### 5.3 Prompt Logging
- **Result:** Pass ✅. All prompt cycles (system, user, and raw AI response) are successfully recorded in `backend/prompt_logs.json`.

