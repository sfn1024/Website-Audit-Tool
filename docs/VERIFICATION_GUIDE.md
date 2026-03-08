# 🧪 Manual Verification Guide

Use these JavaScript snippets in your browser's Developer Tools Console (**F12 -> Console**) to verify the metrics calculated by the system.

---

### 1. Word Count (Cleaned)
This matches our "Clean Soul" extraction logic by removing boilerplate and hidden elements before counting.
```javascript
(function() {
    const clone = document.body.cloneNode(true);
    const selector = 'script, style, nav, footer, header, aside, noscript, [aria-hidden="true"]';
    clone.querySelectorAll(selector).forEach(el => el.remove());
    
    // Remove inline-hidden items
    clone.querySelectorAll('*').forEach(el => {
        const style = el.getAttribute('style') || '';
        if (style.includes('display:none') || style.includes('visibility:hidden')) {
            el.remove();
        }
    });

    const text = clone.innerText || clone.textContent;
    const words = text.trim().split(/\s+/).filter(w => w.length > 0);
    console.log("Total Cleaned Word Count:", words.length);
})();
```

---

### 2. Heading Counts
```javascript
console.log("H1 Count:", document.querySelectorAll('h1').length);
console.log("H2 Count:", document.querySelectorAll('h2').length);
console.log("H3 Count:", document.querySelectorAll('h3').length);
```

---

### 3. CTA (Call to Action) Count
This scans for buttons, links with specific keywords, and role-based actions.
```javascript
(function() {
    let count = 0;
    const ctaPatterns = /\b(get started|sign up|sign in|register|subscribe|buy now|shop now|try free|start free|download|learn more|contact us|book a demo|request demo|join now|apply now|add to cart|enroll|donate|get in touch|let's talk|lets talk|book a call|get a quote|schedule a call|free trial|view demo|see pricing|talk to us|get access|request a quote|watch demo|explore now)\b/i;
    const ctaKeywords = ["btn", "cta", "button", "action", "primary"];

    // Count all buttons
    count += document.querySelectorAll('button').length;

    // Count div/span with role="button"
    document.querySelectorAll('div[role="button"], span[role="button"]').forEach(el => {
        count++;
    });

    // Count <a> tags with CTA logic
    document.querySelectorAll('a[href]').forEach(el => {
        const classes = el.className.toLowerCase();
        const text = el.innerText.trim();
        const href = el.getAttribute('href').toLowerCase();

        if (ctaKeywords.some(kw => classes.includes(kw)) || 
            el.getAttribute('role') === 'button' ||
            href.includes('contact') ||
            ctaPatterns.test(text)) {
            count++;
        }
    });

    console.log("Total CTA Count:", count);
})();
```

---

### 4. Link Counts (Internal vs External)
```javascript
(function() {
    const domain = window.location.hostname;
    let internal = 0, external = 0;

    document.querySelectorAll('a[href]').forEach(a => {
        const href = a.getAttribute('href');
        if (href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) return;
        
        try {
            const url = new URL(a.href);
            if (url.hostname === domain) internal++;
            else external++;
        } catch(e) {}
    });

    console.log("Internal Links:", internal);
    console.log("External Links:", external);
})();
```

---

### 5. Image Count & Missing Alt
This script filters out images in `<template>`/`<noscript>` and excludes tracking pixels or hidden assets.
```javascript
(function() {
    const trackingKeywords = ["pixel", "tracking", "beacon"];
    const allImgs = Array.from(document.querySelectorAll('img'));
    
    const cleanImgs = allImgs.filter(img => {
        // 1. Skip if inside template or noscript
        if (img.closest('template, noscript')) return false;

        const width = img.getAttribute('width');
        const height = img.getAttribute('height');
        const src = (img.getAttribute('src') || "").toLowerCase();
        const style = (img.getAttribute('style') || "").toLowerCase().replace(/\s/g, "");

        // 2. Skip tracking pixels (1x1 or 0x0)
        if (width === "0" || width === "1" || height === "0" || height === "1") return false;

        // 3. Skip keywords in URL
        if (trackingKeywords.some(kw => src.includes(kw))) return false;

        // 4. Skip hidden styles
        if (style.includes("display:none") || style.includes("visibility:hidden")) return false;

        return true;
    });
    
    const total = cleanImgs.length;
    const missingAlt = cleanImgs.filter(img => !img.alt || !img.alt.trim()).length;
    const missingPct = total > 0 ? ((missingAlt / total) * 100).toFixed(1) : 0;

    console.log("Total Images (Filtered):", total);
    console.log("Missing Alt Text:", missingAlt);
    console.log("Missing Alt %:", missingPct + "%");
})();
```

---

### 6. Meta Tags
```javascript
console.log("Meta Title:", document.title);
console.log("Meta Description:", document.querySelector('meta[name="description"]')?.content || "None Found");
```
