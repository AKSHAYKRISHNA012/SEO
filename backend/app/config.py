import os

try:
    from pydantic_settings import BaseSettings
    class Settings(BaseSettings):
        APP_NAME: str = "SEO Intelligence API"
        VERSION: str = "1.0.0"
        ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./seo_intelligence.db")
        LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
        LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
        LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
        CORS_ORIGINS: list = ["*"]

        class Config:
            env_file = ".env"

    settings = Settings()
except Exception:
    class SettingsFallback:
        APP_NAME: str = "SEO Intelligence API"
        VERSION: str = "1.0.0"
        ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./seo_intelligence.db")
        LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
        LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
        LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
        CORS_ORIGINS: list = ["*"]

    settings = SettingsFallback()
