# 📊 Technical Analysis: Metric Calculation & Inaccuracies

This document explains exactly how our Website Audit Tool calculates its core metrics, why they might differ from what you see in a browser, and how we can achieve professional-grade accuracy.

---

## 1. WORD COUNT
### Current Code Logic
```python
visible_text = soup.get_text(separator=" ", strip=True)
word_count = len(visible_text.split())
```
**How it works:** `soup.get_text()` grabs all text nodes from the HTML document, joins them with a space, and counts the resulting "words."

### Why it Overcounts/Differs
- **Boilerplate Inclusion:** It counts navigation menus, footer links, privacy policy text, and sidebars—not just the "article" or "main content."
- **Hidden Text:** It includes text that is hidden from humans via CSS (e.g., `display: none` or mobile-only menus). BeautifulSoup doesn't know what is visible; it only knows what exists in the code.
- **Alt Text/Meta:** Depending on the parser, it can sometimes pull text from non-visible attributes if they aren't properly filtered.

### The Ideal Approach (The Fix)
- **Content Extraction:** Use a "readability" algorithm (similar to Safari Reader Mode) to identify the `main` content block and ignore headers/footers.
- **Visibility Filtering:** Use Playwright's `element.is_visible()` to only count text that a human can actually see on the screen.
- **Realism:** ~90-95% accuracy is realistic once you filter out hidden elements.

---

## 2. CTA COUNT
### Current Code Logic
Checks all `<button>` tags and `<a>` tags for:
- **Classes:** Includes "btn", "cta", "button", "action", "primary".
- **Roles:** `role="button"`.
- **Text Patterns:** Regex check for "Get Started", "Buy Now", etc.

### Why it is Inaccurate
- **Missing Custom Elements:** Modern sites often use `<div>` or `<span>` tags with JavaScript "click" listeners that don't have standard button roles.
- **Icon Buttons:** Buttons that contain only an icon (like a cart icon) without text are often missed by text-based regex.
- **Visual Context:** It can't see the *size* or *color*. A massive red link is a CTA; a tiny footer link is not, even if it says "Contact Us."

### The Ideal Approach (The Fix)
- **Visual Inspection:** Use Playwright to check the "Computed Styles." If an element is large, colorful, and has a "pointer" cursor, it’s likely a CTA.
- **SVG Detection:** Specifically look for SVGs inside links that indicate an action (arrow, cart, envelope).
- **Realism:** ~85% accuracy is realistic because CTA definition is subjective.

---

## 3. IMAGE COUNT
### Current Code Logic
```python
images = soup.find_all("img")
total_images = len(images)
```

### Why it Misses Images
- **CSS Backgrounds:** Many HERO images and decorative banners are loaded via CSS `background-image: url(...)` on a `div` tag. These have no `<img>` tag and are missed entirely.
- **SVGs:** ` <svg>` tags are often used for logos and illustrations. These are technically images but aren't counted.
- **Lazy-Load Limits:** Even with scrolling, some images only load when a specific section is reached *and* the user stops moving.

### The Ideal Approach (The Fix)
- **Unified Discovery:** Loop through EVERY element in the DOM and check for both `img` tags AND `background-image` styles.
- **Network Monitoring:** Use Playwright to count the actual number of image files (`.jpg`, `.png`, `.webp`) requested by the browser during the page load.
- **Realism:** 99% accuracy is achievable by monitoring network traffic.

---

## 4. MISSING ALT PERCENTAGE
### Current Code Logic
`Missing % = (Images with empty/missing alt text) / (Total <img> tags found)`

### Why it Differs
- **The Denominator Problem:** Because we currently miss CSS images and SVGs, our "Total" is too low, making the percentage technically incorrect for the *whole page* (though it might be correct for just the `img` tags).
- **Decorative vs. Informative:** Browsers and accessibility tools often ignore `alt=""` (empty) if the image is marked as decorative. We treat empty alt as a failure, which might be "stricter" than a browser console.

### The Ideal Approach (The Fix)
- **Accurate Base:** Once image count is fixed (including SVGs), the percentage becomes meaningful.
- **Context Awareness:** Only flag images that are *meaningful* (e.g., inside an article) while ignoring tiny icons or spacer pixels.

---

## Final Verdict
- **Root Cause of Inaccuracy:** Relying on **Static HTML Tags** instead of **Computed Styles and Network Activity.**
- **Realistic Goal:** 100% is impossible due to the infinite variety of web design, but **98% accuracy** is achievable by using Playwright to inspect the "Visual Tree" rather than just the "Code Tag."
