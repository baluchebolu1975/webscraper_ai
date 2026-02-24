"""
Configuration management using Pydantic settings.
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class OpenAIConfig(BaseModel):
    """OpenAI API configuration."""
    api_key: str = Field(default="your-api-key-here", description="OpenAI API key")
    model: str = Field(default="gpt-3.5-turbo", description="Model to use")


class Settings(BaseSettings):  # type: ignore[misc]
    """Application settings loaded from environment variables."""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
    
    class ScrapingConfig(BaseModel):
        """Scraping-specific configuration."""
        timeout: int = Field(default=30, description="Request timeout in seconds")
        max_retries: int = Field(default=3, description="Maximum retry attempts")
        user_agent: str = Field(
            default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            description="User agent string"
        )
        proxy_url: Optional[str] = Field(default=None, description="Proxy server URL")
    
    class OutputConfig(BaseModel):
        """Output configuration."""
        format: str = Field(default="json", description="Default output format")
        directory: str = Field(default="data/processed", description="Output directory")
    
    openai: OpenAIConfig = OpenAIConfig()
    scraping: ScrapingConfig = ScrapingConfig()
    output: OutputConfig = OutputConfig()


# Global settings instance
settings = Settings()  # type: ignore[call-arg]
