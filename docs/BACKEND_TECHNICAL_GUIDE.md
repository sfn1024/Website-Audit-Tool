# 🐍 Backend Technical Guide

This document provides a deep dive into the Python backend, explaining exactly how each part of the system works, which files are responsible for specific tasks, and where the AI logic lives.

---

## 🏗️ 1. Project Orchestration (`audit.py`)
**Path:** `backend/app/routers/audit.py`

This is the "Brain" that coordinates the three main steps:
1.  **Scraping**: Calls `scraper.py` to get the page HTML.
2.  **Metrics**: Calls `metrics.py` to get the factual numbers.
3.  **AI Analysis**: Calls `ai_analyzer.py` to get qualitative insights.

### 🧩 Logic Breakdown:
- **`audit_url()`**: The primary POST endpoint. It handles error catching for each stage and combines the results into the final `AuditResponse`.
- **`_extract_visible_text()`**: A helper function that prepares the "clean" text for the Google Gemini AI by removing non-visual tags like `<script>` and `<style>`.

---

## 🕵️ 2. The Scraper (`scraper.py`)
**Path:** `backend/app/services/scraper.py`

This module is responsible for loading the website exactly like a human user would.

### 🧩 Key Functions:
- **`scrape_url()`**: 
  - Launches a **Playwright** (Chromium) browser.
  - Switches the User-Agent to mimic a real desktop browser.
  - **Scroll Logic**: It "walks" down the page in 800px steps to trigger lazy-loaded images.
  - **Fallback Logic**: If the page is too slow (`networkidle` timeout), it falls back to `domcontentloaded` to ensure the audit doesn't crash.
  - **Size Cap**: It enforces a 15MB limit on the HTML to prevent server crashes.

---

## 📊 3. The Metrics Engine (`metrics.py`)
**Path:** `backend/app/services/metrics.py`

This is where the factual, deterministic data is extracted using **BeautifulSoup**.

### 🧩 Who Scrapes What?
- **Word Count**: `extract_metrics` removes boilerplate (footer, nav, scripts) then splits and counts the remaining text.
- **Headings (H1-H3)**: Uses `soup.find_all("h1")` etc. It captures both the **Count** and the **Text** of each heading for our detailed popups.
- **CTAs (Call to Action)**: Matches `<button>` tags and `<a>` tags against 25+ action keywords. It also captures the **Button Text**.
- **Links**: Compares the URL domain against the site domain to categorize **Internal** vs **External**. It captures the full list of unique URLs.
- **Images**: 
  - Filters out tracking pixels (0px or 1px wide).
  - Skips "tracking" or "beacon" URLs.
  - Ignores images hidden by CSS (`display:none`).
  - Calculates the **Missing Alt Percentage**.

---

## 🤖 4. AI Analysis & Gemini (`ai_analyzer.py`)
**Path:** `backend/app/services/ai_analyzer.py`

This module manages the interaction with **Google Gemini 2.5 Flash**.

### 🧩 The Gemini Integration:
- **`analyze_page()`**: The primary function that sends data to Gemini.
- **`SYSTEM_PROMPT`**: This is exactly where the instructions for Gemini are defined. It tells the AI:
  - "Ground every insight in the data."
  - "Analyze 5 dimensions: SEO, Messaging, CTA, Content, and UX."
  - "Provide 3 to 5 prioritized recommendations."
- **`_build_user_prompt()`**: Combines the extracted metrics (JSON format) and the page text into a single prompt for the AI.
- **`_log_prompt_cycle()`**: Every single prompt and AI response is logged here to `prompt_logs.json` for debugging.

### 📐 The 5 dimensions analyzed:
1. **SEO Structure** (Based on headings and meta tags).
2. **Messaging Clarity** (Based on page text and H1).
3. **CTA Usage** (Based on CTA density vs word count).
4. **Content Depth** (Based on word count and logical flow).
5. **UX Concerns** (Based on accessibility and link balance).

---

## 🛠️ 5. Data Models (`models.py`)
**Path:** `backend/app/models.py`

This file defines the **"Contract"** between the backend and the frontend. It uses **Pydantic** to ensure that every metric (like `h1_list` or `cta_list`) follows a strict structure so the frontend never crashes.
