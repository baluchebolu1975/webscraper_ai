"""
Configuration settings for the web scraper.
"""
from dotenv import load_dotenv
try:
    from pydantic_settings import BaseSettings  # type: ignore[import]
except ImportError:
    from pydantic import BaseSettings  # type: ignore[attr-defined]
from pydantic import Field

load_dotenv()


class Settings(BaseSettings):  # type: ignore[misc]
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", validation_alias="OPENAI_MODEL")
    
    # Scraping Configuration
    scraping_timeout: int = Field(default=30, validation_alias="SCRAPING_TIMEOUT")
    max_retries: int = Field(default=3, validation_alias="MAX_RETRIES")
    delay_between_requests: float = Field(default=1.0, validation_alias="DELAY_BETWEEN_REQUESTS")
    
    # User Agent
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        validation_alias="USER_AGENT"
    )
    
    # Proxy Settings
    http_proxy: str = Field(default="", validation_alias="HTTP_PROXY")
    https_proxy: str = Field(default="", validation_alias="HTTPS_PROXY")
    
    # Output Settings
    output_format: str = Field(default="json", validation_alias="OUTPUT_FORMAT")
    output_dir: str = Field(default="data/processed", validation_alias="OUTPUT_DIR")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        populate_by_name = True


# Global settings instance
settings = Settings()
