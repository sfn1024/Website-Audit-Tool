# 🤖 How the AI Performance Analysis Works

This document explains in simple English how the "brain" of our system (powered by Gemini 2.5 Flash) analyzes your website and provides prioritized recommendations.

---

## 1. How the AI Analysis Works

### 🧠 What Data is Sent to Gemini?
When you click "Audit," the system sends two main pieces of information to the AI:
1.  **Factual Metrics**: A clean list of numbers AND **detailed outcomes** (Word count, precise heading text, CTA labels, full link URLs, and image breakdown).
2.  **Visible Text**: The actual text content of your page (what a human sees), excluding code like scripts, styles, or technical metadata.

### 📋 The System Prompt (The AI's "Job Description")
We don't just ask the AI to "look at the site." We give it a strict set of instructions (a System Prompt):
- **Role**: "You are a senior website auditor and UX strategist."
- **Rule of Data**: "Ground every insight in the data. Reference specific numbers."
- **Action Goal**: "Be specific and actionable. Don't say 'improve headings,' say 'add 2 H2 subheadings to break up this 1,200-word block.'"

### 📐 The 5 Dimensions Analyzed
The AI breaks every page down into 5 specific categories:
1.  **SEO Structure**: Checks if your titles are the right length and if your H1/H2/H3 tags follow a logical hierarchy.
2.  **Messaging Clarity**: Checks if your H1 and text content clearly explain what your business does immediately.
3.  **CTA Usage**: Calculates your "CTA Density." The AI looks for roughly **1 CTA per 300-500 words**. Too few is a missed opportunity; too many is spammy.
4.  **Content Depth**: Judges if your page is "thin" (too little text) or "meaty" (helpful and substantial).
5.  **UX Concerns**: Flags "red alerts" like images missing descriptions (Alt Text) or broken link balances.

### 🚄 Response & Display
Gemini returns a structured JSON "package." Our frontend then:
- Maps each dimension to a beautiful block with a custom icon (**SEO**, **Messaging**, **Target**, etc.).
- Categorizes all text into the **AI Performance Analysis** section of the dashboard.

---

## 2. How Recommendations Work

### 🎯 How Gemini Decides
Gemini compares your metrics against industry best practices. If your Alt Text is at 0%, it knows that is a major accessibility failure. If your word count is 2000 but you have 0 headings, it knows the page is unreadable.

### ⚖️ Priority (1 to 5)
- **Priority 1 (Critical)**: Fixes for missing Meta titles, 0 images with alt text, or 0 H1 tags. "Must fix now."
- **Priority 2-3 (Important)**: Improvement to heading structure or adding more CTAs. "Major impact."
- **Priority 4-5 (Strategic)**: Subtle tweaks to meta descriptions or content length. "Fine-tuning."

### 📝 What a Recommendation Contains
Every single recommendation includes:
- **Title**: A short, catchy name for the task.
- **Reasoning**: A "Why" that references your data (e.g., "Since you only have 1 CTA for 1,200 words...").
- **Action Item**: A "How-To" instruction (e.g., "Add a 'Get Started' button midway through the page").

---

## 3. What if the Website is Perfect?

If you have optimal meta tags, a perfect heading structure, 100% alt text coverage, and ideal CTA density:

1.  **Positive Reinforcement**: In the 5-dimension analysis, Gemini will say things like "Excellent SEO groundwork..." or "Messaging is exceptionally crisp."
2.  **Strategic Recommendations**: Even for "perfect" sites, our prompt requires 3-5 recommendations. Instead of fixes, Gemini will suggest **strategic next steps** like:
    - "Your messaging is perfect; now try A/B testing a different CTA color."
    - "Your content depth is great; consider adding internal links to deeper blog posts."
3.  **No False Alarms**: It won't lie and say things are bad, but it will always look for the "next 1%" improvement.

---

## 4. Grounded in Metrics (Example)

The AI is strictly "grounded," meaning it cannot guess. It must use your numbers.

**Example of Metric Grounding in a Recommendation:**
> **Title**: Fix Accessibility Gap
> **Reasoning**: Your **Missing Alt Percentage is 85.2%**. This means nearly all your visual assets are invisible to screen readers and search engines.
> **Action**: Add descriptive text to the 42 images currently missing Alt tags.

**What stops it from being generic?**
Our internal instructions (the Prompt) forbid generic advice. If Gemini says "improve your site" without mentioning a metric or a specific content snippet, it would be violating its "Strict Rule #1."
