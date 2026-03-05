"""
AI Analyzer module — integrates Gemini 2.5 Flash for page analysis.

Receives extracted metrics + page text, builds a structured prompt,
calls Gemini with JSON response mode, parses the result, and logs
every prompt/response cycle to prompt_logs.json.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from google import genai
from google.genai import types

from app.config import settings
from app.models import PageMetrics

# ── Configure Gemini ─────────────────────────────────────────────────────────

client = genai.Client(api_key=settings.gemini_api_key)

# Path to the prompt log file (in the backend root directory)
LOG_FILE = Path(__file__).resolve().parent.parent.parent / "prompt_logs.json"


# ── Custom Exception ─────────────────────────────────────────────────────────

class AnalysisError(Exception):
    """Raised when Gemini analysis fails."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


# ── Prompts ──────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a senior website auditor and UX strategist. You have been given the factual metrics extracted from a web page along with the visible text content of that page.

Your job is to analyze the page and produce a structured audit report. Follow these rules strictly:

1. GROUND EVERY INSIGHT IN THE DATA. Reference specific numbers from the metrics (e.g., "With only 1 H1 and 0 H2 tags..." or "The 33.3% missing alt text rate means..."). Never give generic advice that could apply to any page.

2. BE SPECIFIC AND ACTIONABLE. Instead of "improve your headings", say "Add 2-3 H2 subheadings to break the 1,245-word body into scannable sections."

3. ANALYZE THESE 5 DIMENSIONS:
   - seo_analysis: Evaluate heading hierarchy (H1/H2/H3 counts), meta title (length, keyword usage), meta description (length, presence), and overall SEO structure. Ideal meta title is 50-60 chars, meta description is 150-160 chars.
   - messaging_clarity: Assess whether the page text communicates a clear value proposition, whether the H1 is compelling, and whether the content flow is logical. Reference the word count and heading structure.
   - cta_usage: Evaluate the number of CTAs found, their density relative to content length, and whether there are too few or too many. A good ratio is roughly 1 CTA per 300-500 words.
   - content_depth: Judge whether the word count is appropriate for the page type, whether headings create logical sections, and whether the content has substance or is thin.
   - ux_concerns: Flag accessibility issues (images missing alt text %), structural problems (missing headings, no meta description), and link balance (internal vs external).

4. PROVIDE 3 TO 5 PRIORITIZED RECOMMENDATIONS. Each must include a priority number (1 = most urgent), a short title, the reasoning grounded in the metrics, and a concrete action step.

5. RESPOND WITH ONLY VALID JSON. No markdown fences, no explanation text outside the JSON. The response must parse directly as JSON.

6. USE EXACTLY THIS JSON STRUCTURE:
{
  "seo_analysis": "string — 2-4 sentences",
  "messaging_clarity": "string — 2-4 sentences",
  "cta_usage": "string — 2-4 sentences",
  "content_depth": "string — 2-4 sentences",
  "ux_concerns": "string — 2-4 sentences",
  "recommendations": [
    {
      "priority": 1,
      "title": "short title",
      "reasoning": "why this matters, referencing specific metrics",
      "action": "concrete step to fix it"
    }
  ]
}"""


def _build_user_prompt(metrics: PageMetrics, page_text: str) -> str:
    """
    Build the user prompt containing the metrics JSON and truncated page text.
    Truncates text to ~8,000 words to stay within Gemini token limits.
    """
    # Truncate page text to ~8,000 words
    words = page_text.split()
    if len(words) > 8000:
        truncated_text = " ".join(words[:8000]) + "\n\n[... content truncated at 8,000 words ...]"
    else:
        truncated_text = page_text

    metrics_json = metrics.model_dump_json(indent=2)

    return f"""Here are the extracted metrics for this web page:

{metrics_json}

Here is the visible text content of the page:

---
{truncated_text}
---

Analyze this page across all 5 dimensions and provide 3-5 prioritized recommendations. Return ONLY valid JSON."""


# ── Prompt Logging ───────────────────────────────────────────────────────────

def _log_prompt_cycle(url: str, system_prompt: str, user_prompt: str, raw_response: str):
    """
    Append a prompt/response log entry to prompt_logs.json.
    Creates the file if it doesn't exist.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "url": url,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "raw_gemini_response": raw_response,
    }

    # Read existing log or start fresh
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []
    else:
        logs = []

    logs.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


# ── Main Analysis Function ──────────────────────────────────────────────────

async def analyze_page(metrics: PageMetrics, page_text: str, url: str) -> dict:
    """
    Send metrics + page text to Gemini 2.5 Flash and return structured insights.

    Args:
        metrics: The PageMetrics Pydantic model with all factual data.
        page_text: The visible text content extracted from the page.
        url: The original URL (used for logging).

    Returns:
        A dict matching the AI analysis JSON structure.

    Raises:
        AnalysisError: If Gemini fails or returns unparseable output.
    """
    user_prompt = _build_user_prompt(metrics, page_text)

    # ── Call Gemini ──────────────────────────────────────────────────────
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                temperature=0.4,
            ),
            contents=user_prompt
        )
        raw_response = response.text

    except Exception as e:
        _log_prompt_cycle(url, SYSTEM_PROMPT, user_prompt, f"ERROR: {str(e)}")
        raise AnalysisError(f"Gemini API call failed: {str(e)}")

    # ── Log the full prompt cycle ────────────────────────────────────────
    _log_prompt_cycle(url, SYSTEM_PROMPT, user_prompt, raw_response)

    # ── Parse the JSON response ──────────────────────────────────────────
    try:
        insights = json.loads(raw_response)
    except json.JSONDecodeError:
        raise AnalysisError("Gemini returned invalid JSON. Check prompt_logs.json for details.")

    # ── Validate required keys exist ─────────────────────────────────────
    required_keys = [
        "seo_analysis", "messaging_clarity", "cta_usage",
        "content_depth", "ux_concerns", "recommendations",
    ]
    missing = [k for k in required_keys if k not in insights]
    if missing:
        raise AnalysisError(f"Gemini response missing keys: {', '.join(missing)}")

    return insights
