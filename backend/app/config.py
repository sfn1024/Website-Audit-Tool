"""
Configuration module.
Loads environment variables from .env and exposes them as a Settings object.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Gemini API key — not used yet, but ready for Phase 2
    gemini_api_key: str = ""

    # CORS: comma-separated list of allowed origins
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # Scraper settings
    scrape_timeout: int = 15  # seconds
    max_redirects: int = 5
    max_html_size: int = 5 * 1024 * 1024  # 5 MB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance — import this wherever settings are needed
settings = Settings()
