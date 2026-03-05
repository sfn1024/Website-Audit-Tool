"""
FastAPI application entry point.

- Mounts the audit router
- Configures CORS for the React frontend
- Provides a health-check root endpoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import audit

# ── Create the app ───────────────────────────────────────────────────────────

app = FastAPI(
    title="Website Audit Tool API",
    description="Scrapes a webpage and returns structured SEO & content metrics.",
    version="1.0.0",
)

# ── CORS Middleware ──────────────────────────────────────────────────────────
# Allow the Vite dev server (localhost:5173) and any other configured origins

origins = [origin.strip() for origin in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routers ────────────────────────────────────────────────────────

app.include_router(audit.router)


# ── Health Check ─────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    """Simple health-check endpoint."""
    return {"status": "ok", "message": "Website Audit Tool API is running."}
