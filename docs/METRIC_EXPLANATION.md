# 📊 How Each Metric is Calculated

This document provides a simple, technical explanation of how the system achieves professional-grade accuracy when scraping and counting your website data.

---

## 🏗️ Step 1: The Scraper (scraper.py)
Before any counting happens, the **Scraper** fetches the data using a real Chromium browser (**Playwright**).

1. **JavaScript Support**: Unlike basic scrapers, Playwright allows us to render complex React/Vue sites and triggered lazy-loaded content.
2. **Infinite Scroll**: It "walks" down the page in 800-pixel steps with pauses. This ensures every image and sub-section is fully rendered.
3. **Capture**: Once the page is stable, it extracts the final HTML for processing.

---

## 🛠️ Step 2: The Metrics Engine (metrics.py)
The Metrics engine uses **BeautifulSoup** to parse the HTML with advanced logic for high accuracy:

### 1. Word Count (Rendered Content)
- **Logic**: 
  - It removes non-visual elements like `<script>`, `<style>`, and `<template>`.
  - It filters out elements hidden via accessibility tags (`aria-hidden="true"`) or inline CSS (`display:none`).
  - It counts the remaining text that a human user would actually see.

### 2. Heading Breakdown (H1, H2, H3)
- **Logic**: Captures both the **Count** and the **Actual Text** of headings.
- **Interactive**: You can click the **(i)** icon in the dashboard to see exactly what those headings say.

### 3. CTA (Call to Action) Discovery
- **Logic**: 
  - **Buttons**: Every `<button>` tag and `role="button"` attribute.
  - **Action Heuristics**: Scans for 25+ specific conversion phrases (e.g., "Get Started," "Book Now").

### 4. Link Mapping (Internal vs. External)
- **Logic**: Categorizes links based on their destination. 
- **Interactive**: The **(i)** icon reveals the full list of URLs found, helping you track where your traffic is going.

### 5. Image Count (Visible Media)
- **What it does**: Counts every actual image element while ignoring "noise."
- **Logic**: 
  - **Filters**: It automatically ignores tracking pixels (1x1), hidden assets, and template code.
  - **Breakdown**: It shows you exactly how many images exist and how many have proper **Alt Text**.

### 6. Meta Title & Description
- **Logic**: Extracts the exact title and description as they would appear in Google Search results, providing length counts for SEO optimization.
