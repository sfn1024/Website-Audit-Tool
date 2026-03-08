# 📊 How Each Metric is Calculated

This document provides a simple, technical explanation of how the system achieves professional-grade accuracy when scraping and counting your website data.

---

## 🏗️ Step 1: The Scraper (scraper.py)
Before any counting happens, the **Scraper** fetches the data using a real Chromium browser (Playwright).

1. **Network Monitoring**: As the page loads, the scraper listens to every network request. It identifies and counts every unique image asset (including CSS background images and SVGs) loaded by the browser.
2. **Infinite Scroll**: It "walks" down the page in 800-pixel steps with pauses. This ensures every lazy-loaded image and dynamic section is fully triggered and rendered.
3. **Capture**: Once the network is idle and scrolling is complete, it extracts the fully-rendered source code (HTML) and the total "Network Image Count."

---

## 🛠️ Step 2: The Metrics Engine (metrics.py)
The Metrics engine uses **BeautifulSoup** to parse the HTML with advanced logic for high accuracy:

### 1. Word Count (High Accuracy)
- **What it does**: Extracts only the meaningful text that a human actually reads.
- **Logic**: 
  - It creates a "Clean Soul" of the page by **removing** boilerplate like navigation (`<nav>`), headers, footers, sidebars (`<aside>`), and non-visible tags like `<script>` or `<style>`.
  - It also deletes elements hidden via accessibility tags (`aria-hidden="true"`) or inline CSS (`display:none`, `visibility:hidden`).
  - Finally, it counts the words in the remaining "pure" content.

### 2. Heading Counts (H1, H2, H3)
- **What it does**: Counts the structural headings used for content hierarchy.
- **Logic**: It searches the document for `<h1>`, `<h2>`, and `<h3>` tags and returns the exact count for each level.

### 3. CTA (Call to Action) Count
- **What it does**: Detects elements designed to drive user conversions.
- **Logic**: 
  - **Buttons**: Every `<button>` tag and any element (`div`, `span`, `a`) with a `role="button"` attribute is counted.
  - **Text Heuristics**: It scans links for 25+ specific "action" phrases (e.g., "Get Started," "Book a Call," "See Pricing").
  - **Contact Logic**: Any link containing "contact" in its address is automatically identified as a CTA.

### 4. Internal vs. External Links
- **What it does**: Categorizes links based on their destination.
- **Logic**: It compares every link's domain to your site's domain. If they match, it's categorized as Internal; otherwise, it's External. Helper links like `mailto:` are ignored.

### 5. Image Count (Tag-Based)
- **What it does**: Counts every rendered image element on the page.
- **Logic**: 
  - It searches the HTML for all `<img>` tags.
  - **Exclusion**: It automatically ignores images hidden inside `<template>` or `<noscript>` tags, as these are not visible to the user.
- **Limitations**: It currently focuses on actual `<img>` elements and intentionally ignores CSS background images and SVGs for maximum accuracy across different site types.

### 6. Missing Alt Text Percentage
- **What it does**: Measures how many images are missing descriptions for accessibility.
- **Logic**: 
  - It checks all rendered images found in Step 5 for the `alt` attribute.
  - **Calculation**: (Images Missing Alt / Total Rendered Images) × 100.

### 7. Meta Title & Description
- **What it does**: Extracts the snippets shown in Search Engine results.
- **Logic**: It looks for the `<title>` tag and the specific `<meta name="description">` tag inside the page's head section.
