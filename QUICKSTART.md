# Quick Start Guide

Get started with WebScraper AI in minutes!

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Installation

### 1. Clone or Navigate to the Project

```bash
cd webscraper_ai
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
copy .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## Basic Usage

### Simple Web Scraping

```python
from src.scraper import WebScraper

scraper = WebScraper()
data = scraper.scrape("https://example.com")

print(f"Title: {data['title']}")
print(f"Links found: {len(data['links'])}")
```

### AI-Powered Analysis

```python
from src.scraper import WebScraper
from src.ai_analyzer import AIAnalyzer

# Scrape content
scraper = WebScraper()
data = scraper.scrape("https://example.com")

# Analyze with AI
analyzer = AIAnalyzer()
analysis = analyzer.analyze(data)

print(analysis['summary'])
```

### Custom Selectors

```python
from src.scraper import WebScraper

scraper = WebScraper()

# Define what to extract
selectors = {
    'headings': 'h1, h2, h3',
    'paragraphs': 'p',
    'prices': '.price'
}

data = scraper.scrape("https://example.com", selectors=selectors)
print(data['headings'])
```

### Save Results

```python
from src.scraper import WebScraper
from src.utils import save_to_json, save_to_csv

scraper = WebScraper()
data = scraper.scrape("https://example.com")

# Save as JSON
save_to_json(data, "results.json")

# Save as CSV (for list data)
save_to_csv([data], "results.csv")
```

## Run Examples

```bash
python examples/basic_scraping.py
```

## Run Tests

```bash
pytest tests/ -v
```

## Project Structure Overview

```
webscraper_ai/
├── src/                    # Source code
│   ├── scraper.py         # Main scraping logic
│   ├── ai_analyzer.py     # AI analysis
│   ├── config.py          # Configuration
│   └── utils.py           # Utilities
├── examples/              # Usage examples
├── tests/                 # Test suite
├── data/                  # Data storage
│   ├── raw/              # Raw scraped data
│   └── processed/        # Processed data
└── requirements.txt       # Dependencies
```

## Common Tasks

### Scrape Multiple URLs

```python
urls = ["https://example.com", "https://example.org"]
results = scraper.scrape_multiple(urls, delay=1.0)
```

### Extract Specific Content

```python
# Get only text from specific elements
soup = scraper.parse_html(html)
text = scraper.extract_text(soup, selector='article p')
```

### Handle Errors

```python
with WebScraper() as scraper:
    try:
        data = scraper.scrape(url)
        if 'error' in data:
            print(f"Error: {data['error']}")
    except Exception as e:
        print(f"Failed: {e}")
```

## Next Steps

- Explore [examples/basic_scraping.py](examples/basic_scraping.py) for more examples
- Read the full [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Troubleshooting

### Import Errors

Make sure you're in the project root and have activated the virtual environment.

### API Key Issues

Ensure your `.env` file exists and contains a valid `OPENAI_API_KEY`.

### Missing Dependencies

Run `pip install -r requirements.txt` again to ensure all packages are installed.

## Support

For issues and questions, please open an issue on GitHub.

Happy scraping! 🚀
