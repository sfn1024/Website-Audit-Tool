# Website Audit Tool 🚀

An AI-powered web auditing tool that combines deterministic scraping with generative AI to provide grounded, actionable insights for any URL.

## Overview
This tool performs a deep audit on any publicly accessible website. It extracts factual metrics (meta tags, heading hierarchy, link counts, and image accessibility) and passes them to **Google Gemini 2.5 Flash** to generate a qualitative UX and SEO analysis with prioritized recommendations.

## Architecture
The project is built with a clear separation of concerns in a monorepo structure:

- **Frontend (React + Vite)**: A high-fidelity, agency-quality UI built with plain CSS. It follows a 3-column strategic layout:
  1. **Factual Metrics**: Deterministic data extraction.
  2. **AI Performance Analysis**: Qualitative assessment across 5 dimensions.
  3. **Prioritized Recommendations**: Urgent to minor action items.
- **Backend (FastAPI)**: A high-performance Python API that orchestrates the scraping and analysis pipeline.
- **Services (Scraper & Metrics)**: Custom-built services using `httpx` and `BeautifulSoup4` for reliable data extraction.
- **AI Analyzer**: A dedicated service that interacts with the Gemini API to transform raw data into expert-level insights.

## AI Design Decisions
- **Structured Prompting**: Prompts are strictly structured to ground the AI in factual numbers. This prevents "hallucinations" and ensures recommendations are always backed by the extracted metrics.
- **JSON Schema Enforcement**: Using Gemini's JSON mode ensure the backend receives 100% parseable data, which is then validated by Pydantic models.
- **Prompt Logging**: Every interaction (system prompt, user data, and raw AI response) is logged to `prompt_logs.json` for auditability and debugging.
- **Model Choice**: Gemini 2.5 Flash was chosen for its speed and 
  cost efficiency on a per-request basis, making it practical for 
  an internal agency tool with frequent audits.

## Trade-offs & Decisions
- **Deployment Ready**: Included `vercel.json` (frontend) and `railway.json` (backend).
- **`httpx` over Puppeteer**: For this assessment, a lightweight HTTP client was chosen for speed and deployment simplicity. While it doesn't execute JavaScript, it covers 90% of SEO/METADATA requirements without the heavy overhead of a headless browser.
- **JS-Rendered Pages (SPAs)**: Sites built with React, Vue, or 
  Angular return minimal HTML via httpx since content is rendered 
  client-side. This is a known limitation. Playwright would solve 
  this in a future iteration.
- **Single Endpoint (`/audit`)**: All processing (scraping, metrics, and AI) happens in a single request-response cycle. This simplifies the frontend state management for an MVP, though an async task queue (like Celery/RabbitMQ) would be better for high-scale production.
- **Plain CSS**: Opted for Vanilla CSS with variables to avoid the bloat of external component libraries.

## Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- [Gemini API Key](https://aistudio.google.com/app/apikey)

### Backend Setup
1. `cd backend`
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend/` directory:
   ```bash
   cp .env.example .env
   ```
5. Add your `GEMINI_API_KEY` to the `.env` file.
6. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   - *Runs at http://localhost:8000*

**Note**: Backend .env file Structure
### ── Website Audit Tool — Backend Environment Variables ─────────────

   # Gemini API Key
   GEMINI_API_KEY=Gemini API KEY Here

   # CORS: comma-separated list of allowed origins
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000

### Frontend Setup
1. `cd frontend`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file in the `frontend/` directory:
   ```bash
   cp .env.example .env
   ```
   *(This ensures `VITE_API_URL` points to your local backend at http://localhost:8000)*
4. Start the development server:
   ```bash
   npm run dev
   ```
   - *Runs at http://localhost:5173* (connects to local backend automatically)   

## What I'd Improve With More Time
1. **Headless Browser**: Integrate Playwright/Puppeteer to audit SPAs (Single Page Applications) that rely on client-side rendering.
2. **Performance Auditing**: Integrate Lighthouse API for Core Web Vitals assessment.
3. **Database Integration**: Store audit history to allow users to compare results over time.
4. **PDF Reports**: Export the 3-column analysis as a professional PDF for clients.
5. **Detailed Outcomes**: Provide detailed outcomes for each metric as much as possible. (example: instead of H1: 2, H2: 4. Will provide what are those H1s and H2s)
6. **Better SEO Recommendations**: Provide better SEO recommendations in keyword research integrating DataForSEO, Ahref, SEMrush. (budget + time)