"""
WebScraper AI package.
"""
from .scraper import WebScraper
from .ai_analyzer import AIAnalyzer
from .config import settings
from .logging_config import get_logger, setup_logging
from .utils import (
    save_to_json,
    save_to_csv,
    save_to_excel,
    clean_text,
    get_timestamp,
    create_directories
)

__version__ = "0.1.0"
__all__ = [
    "WebScraper",
    "AIAnalyzer",
    "settings",
    "get_logger",
    "setup_logging",
    "save_to_json",
    "save_to_csv",
    "save_to_excel",
    "clean_text",
    "get_timestamp",
    "create_directories"
]
