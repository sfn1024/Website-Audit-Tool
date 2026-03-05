# Website Audit Tool 🚀

An AI-powered web auditing tool that combines deterministic scraping with generative AI to provide grounded, actionable insights for any URL.

## 🌟 Overview
This tool performs a deep audit of any publicly accessible website. It extracts factual metrics (meta tags, heading hierarchy, link counts, and image accessibility) and passes them to **Google Gemini 2.5 Flash** to generate a qualitative UX and SEO analysis with prioritized recommendations.

## 🏗️ Architecture
The project is built with a clear separation of concerns in a monorepo structure:

- **Frontend (React + Vite)**: A high-fidelity, agency-quality UI built with plain CSS. It follows a 3-column strategic layout:
  1. **Factual Metrics**: Deterministic data extraction.
  2. **AI Performance Analysis**: Qualitative assessment across 5 dimensions.
  3. **Prioritized Recommendations**: Urgent to minor action items.
- **Backend (FastAPI)**: A high-performance Python API that orchestrates the scraping and analysis pipeline.
- **Services (Scraper & Metrics)**: Custom-built services using `httpx` and `BeautifulSoup4` for reliable data extraction.
- **AI Analyzer**: A dedicated service that interacts with the Gemini API to transform raw data into expert-level insights.

## 🤖 AI Design Decisions
- **Structured Prompting**: Prompts are strictly structured to ground the AI in factual numbers. This prevents "hallucinations" and ensures recommendations are always backed by the extracted metrics.
- **JSON Schema Enforcement**: Using Gemini's JSON mode ensure the backend receives 100% parseable data, which is then validated by Pydantic models.
- **Prompt Logging**: Every interaction (system prompt, user data, and raw AI response) is logged to `prompt_logs.json` for auditability and debugging.

## ⚖️ Trade-offs & Decisions
- ✅ **Deployment Ready**: Included `vercel.json` (frontend) and `railway.json` (backend).
- **`httpx` over Puppeteer**: For this assessment, a lightweight HTTP client was chosen for speed and deployment simplicity. While it doesn't execute JavaScript, it covers 90% of SEO/METADATA requirements without the heavy overhead of a headless browser.
- **Single Endpoint (`/audit`)**: All processing (scraping, metrics, and AI) happens in a single request-response cycle. This simplifies the frontend state management for an MVP, though an async task queue (like Celery/RabbitMQ) would be better for high-scale production.
- **Plain CSS**: Opted for Vanilla CSS with variables to demonstrate strong foundational design skills and avoid the bloat of external component libraries.

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- [Gemini API Key](https://aistudio.google.com/app/apikey)

### Backend Setup
1. `cd backend`
2. `pip install -r requirements.txt`
3. Create `.env` from `.env.example` and add your `GEMINI_API_KEY`.
4. `uvicorn app.main:app --reload`
   - *Runs at http://localhost:8000*

### Frontend Setup
1. `cd frontend`
2. `npm install`
3. `npm run dev`
   - *Runs at http://localhost:5173* (connects to local backend automatically)

## 🔮 Future Improvements
1. **Headless Browser**: Integrate Playwright/Puppeteer to audit SPAs (Single Page Applications) that rely on client-side rendering.
2. **Performance Auditing**: Integrate Lighthouse API for Core Web Vitals assessment.
3. **Database Integration**: Store audit history to allow users to compare results over time.
4. **PDF Reports**: Export the 3-column analysis as a professional PDF for clients.
