# WebScraper AI

An intelligent web scraping tool powered by AI for extracting and analyzing web content.

## Features

- 🌐 Robust web scraping capabilities with retry logic
- 🤖 AI-powered content extraction and analysis (OpenAI integration)
- 📊 Data export in multiple formats (JSON, CSV, Excel)
- 🔄 Intelligent error handling and input validation
- 🔒 Security-focused with path traversal protection
- 📝 Customizable scraping rules with CSS selectors
- 🎯 Configurable retry attempts and timeouts
- 📋 Centralized logging configuration

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from src.scraper import WebScraper
from src.ai_analyzer import AIAnalyzer

# Initialize scraper
scraper = WebScraper()

# Scrape a website
data = scraper.scrape("https://example.com")

# Analyze with AI
analyzer = AIAnalyzer()
insights = analyzer.analyze(data)

print(insights)
```

## Project Structure

```
webscraper_ai/
├── src/
│   ├── scraper.py          # Main scraping logic
│   ├── ai_analyzer.py      # AI analysis module
│   ├── config.py           # Configuration settings
│   ├── logging_config.py   # Centralized logging
│   └── utils.py            # Utility functions
├── tests/
│   ├── test_scraper.py
│   └── test_ai_analyzer.py
├── data/
│   ├── raw/                # Raw scraped data
│   └── processed/          # Processed data
├── examples/
│   └── basic_scraping.py   # Example usage
├── requirements.txt
├── .env.example
└── README.md
```

## Configuration

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Add your API keys and configuration:
- `OPENAI_API_KEY`: Your OpenAI API key for AI analysis
- `SCRAPING_TIMEOUT`: Request timeout in seconds
- `MAX_RETRIES`: Maximum retry attempts

## Usage Examples

See the `examples/` directory for detailed usage examples.

## Testing

```bash
pytest tests/
```

## License

MIT License
