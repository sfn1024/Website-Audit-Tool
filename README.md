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
- **Services (Scraper & Metrics)**: Custom-built services using **Playwright** and **BeautifulSoup4** for accurate, human-like data extraction (including JS-rendered content).
- **AI Analyzer**: A dedicated service that interacts with the Gemini API to transform raw data into expert-level insights.

## AI Design Decisions
- **Structured Prompting**: Prompts are strictly structured to ground the AI in factual numbers. This prevents "hallucinations" and ensures recommendations are always backed by the extracted metrics.
- **JSON Schema Enforcement**: Using Gemini's JSON mode ensure the backend receives 100% parseable data, which is then validated by Pydantic models.
- **Prompt Logging**: Every interaction (system prompt, user data, and raw AI response) is logged to `prompt_logs.json` for auditability and debugging.

## Trade-offs & Decisions
- **Playwright over httpx**: upgraded from `httpx` to a headless Chromium browser (Playwright) to support modern, lazy-loaded, and JavaScript-heavy websites. This ensures 100% accuracy in image and content detection.
- **Detailed Outcomes**: Unlike standard tools, we provide the actual values (URLs, Text) behind the numbers via interactive popups.
- **Single Endpoint (`/audit`)**: All processing (scraping, metrics, and AI) happens in a single request-response cycle. This simplifies the frontend state management for an MVP, though an async task queue (like Celery/RabbitMQ) would be better for high-scale production.
- **Plain CSS**: Opted for Vanilla CSS with variables to avoid the complexity of external component libraries.

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
   playwright install chromium
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
1. **Performance Auditing**: Integrate Lighthouse API for Core Web Vitals assessment.
2. **Database Integration**: Store audit history to allow users to compare results over time.
3. **PDF Reports**: Export the 3-column analysis as a professional PDF for clients.
4. **Better SEO Recommendations**: Provide better SEO recommendations in keyword research integrating DataForSEO, Ahref, SEMrush. (budget + time)