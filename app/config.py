from pydantic import BaseSettings
import logging
from logging.config import dictConfig

class Settings(BaseSettings):
    # 🧠 Project metadata
    PROJECT_NAME: str = "SmartPromptBox Pro"
    PROJECT_VERSION: str = "1.0.0"

    # 🔐 API keys & tokens
    TELEGRAM_BOT_TOKEN: str = "dummy-placeholder"
    OPENAI_API_KEY: str = "dummy-placeholder"

    # 🌐 Base URL for external services (optional for now)
    BASE_API_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"   # tells pydantic to load from .env

# Create settings object
settings = Settings()

# 📝 Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    },
}

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("SmartPromptBox")
