# 🕸️ WebScraper AI

<div align="center">

**An intelligent, production-ready web scraping framework powered by AI**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code Quality](https://img.shields.io/badge/code%20quality-A--grade-brightgreen.svg)](https://github.com/baluchebolu1975/webscraper_ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-webscraper__ai-181717?logo=github)](https://github.com/baluchebolu1975/webscraper_ai)

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Examples](#-usage-examples) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

**WebScraper AI** is a robust, enterprise-grade Python framework that combines intelligent web scraping with OpenAI-powered content analysis. Built with reliability, security, and extensibility in mind, it enables developers to extract, analyze, and structure data from websites with minimal effort.

### 🎯 Key Highlights

- **Production-Ready**: Implements retry logic, error handling, and comprehensive logging
- **AI-Powered**: Integrated OpenAI capabilities for text summarization, entity extraction, and sentiment analysis
- **Secure**: Built-in protection against path traversal attacks and input validation
- **Flexible**: Multiple export formats (JSON, CSV, Excel) and customizable scraping rules
- **Well-Tested**: 26+ unit tests with comprehensive coverage
- **Type-Safe**: Modern Python type hints using Python 3.9+ syntax

---

## ✨ Features

### 🌐 Web Scraping
- **Automatic Retry Logic**: Exponential backoff with configurable retry attempts
- **Session Management**: Persistent HTTP sessions for improved performance
- **HTML Parsing**: BeautifulSoup4 + lxml for fast, reliable parsing
- **Multi-URL Support**: Batch scrape multiple URLs concurrently
- **Custom Selectors**: Target specific elements with CSS selectors
- **Link & Image Extraction**: Automatic discovery and normalization of URLs

### 🤖 AI-Powered Analysis
- **Text Summarization**: Generate concise summaries of scraped content
- **Entity Extraction**: Identify people, organizations, locations, and more
- **Sentiment Analysis**: Determine emotional tone of content
- **Content Classification**: Categorize content by topic or type
- **Keyword Extraction**: Discover key themes and terms
- **Custom Analysis**: Support for user-defined analysis types

### 🔐 Security & Reliability
- **Path Traversal Protection**: Secure file operations with validation
- **URL Validation**: Verify URLs before making requests
- **Input Sanitization**: Clean and validate all user inputs
- **Rate Limiting Ready**: Built-in support for request throttling
- **Error Recovery**: Graceful handling of network failures and timeouts

### 📊 Data Management
- **Multiple Export Formats**: JSON, CSV, Excel (XLSX)
- **Structured Output**: Clean, consistent data schemas
- **Automatic Directory Creation**: No manual setup required
- **Timestamped Files**: Organized output with automatic naming
- **Data Validation**: Pydantic-based configuration and validation

### 📝 Developer Experience
- **Centralized Logging**: Unified logging configuration across all modules
- **Type Hints**: Full type annotations for IDE support
- **Comprehensive Tests**: pytest-based test suite with 26+ tests
- **Example Scripts**: Ready-to-run examples for common use cases
- **Detailed Documentation**: In-code documentation and external guides

---

## 📋 Prerequisites

- **Python 3.9 or higher**
- **pip** (Python package installer)
- **OpenAI API Key** (for AI analysis features)
- **Internet connection** (for web scraping)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/baluchebolu1975/webscraper_ai.git
cd webscraper_ai
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
SCRAPING_TIMEOUT=30
MAX_RETRIES=3
```

---

## 🎬 Quick Start

### Basic Web Scraping

```python
from src.scraper import WebScraper

# Initialize the scraper
scraper = WebScraper(timeout=10, max_retries=3)

# Scrape a website
result = scraper.scrape("http://info.cern.ch/")

# Access the extracted data
print(f"Title: {result['title']}")
print(f"Text Length: {len(result['text'])} characters")
print(f"Links Found: {len(result['links'])}")
print(f"Images Found: {len(result['images'])}")
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
analysis = analyzer.analyze(
    content=data,
    analysis_type='summarize',
    custom_prompt="Provide a concise summary"
)

print(analysis['summary'])
print(analysis['key_points'])
```

### Export Data to Multiple Formats

```python
from src.scraper import WebScraper
from src.utils import save_to_json, save_to_csv, save_to_excel

scraper = WebScraper()
data = scraper.scrape("https://example.com")

# Save to different formats
save_to_json(data, "output.json")
save_to_csv([data], "output.csv")
save_to_excel([data], "output.xlsx")
```

### Batch Scraping Multiple URLs

```python
from src.scraper import WebScraper
from src.utils import save_to_json

scraper = WebScraper()
urls = [
    "http://info.cern.ch/",
    "https://example.com",
    "https://python.org"
]

# Scrape multiple URLs
results = scraper.scrape_multiple(urls)

# Save results
for result in results:
    if result.get('error'):
        print(f"Failed: {result['url']} - {result['error']}")
    else:
        print(f"Success: {result['url']} - {len(result['text'])} chars")
        save_to_json(result, f"scrape_{result['url'].replace('/', '_')}.json")
```

---

## 📁 Project Structure

```
webscraper_ai/
├── 📂 src/                          # Source code
│   ├── __init__.py                  # Package initialization
│   ├── scraper.py                   # Main scraping engine (263 lines)
│   ├── ai_analyzer.py               # AI analysis module (260 lines)
│   ├── config.py                    # Configuration management (48 lines)
│   ├── logging_config.py            # Centralized logging (34 lines)
│   └── utils.py                     # Utility functions (168 lines)
│
├── 📂 tests/                        # Test suite
│   ├── __init__.py
│   ├── test_scraper.py              # Scraper tests
│   ├── test_ai_analyzer.py          # AI analyzer tests
│   └── test_utils.py                # Utility tests
│
├── 📂 examples/                     # Usage examples
│   ├── basic_scraping.py            # Simple scraping example
│   └── demo_scraping.py             # Advanced demo with real data
│
├── 📂 data/                         # Data storage
│   ├── raw/                         # Raw scraped data
│   ├── processed/                   # Processed/analyzed data
│   └── README.md                    # Data directory documentation
│
├── 📂 docs/                         # Documentation (optional)
│
├── 📄 .env.example                  # Environment variables template
├── 📄 .gitignore                    # Git ignore rules
├── 📄 requirements.txt              # Python dependencies
├── 📄 pyproject.toml                # Project metadata
├── 📄 LICENSE                       # MIT License
├── 📄 CONTRIBUTING.md               # Contribution guidelines
├── 📄 QUICKSTART.md                 # Quick start guide
├── 📄 CODE_QUALITY_REPORT.md        # Code quality analysis
├── 📄 SCRAPING_EXPLAINED.md         # Technical scraping guide
└── 📄 README.md                     # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | Yes (for AI) |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` | No |
| `SCRAPING_TIMEOUT` | Request timeout (seconds) | `30` | No |
| `MAX_RETRIES` | Maximum retry attempts | `3` | No |
| `DELAY_BETWEEN_REQUESTS` | Delay between requests (seconds) | `1` | No |
| `USER_AGENT` | Custom user agent string | Mozilla/5.0... | No |
| `OUTPUT_FORMAT` | Default output format | `json` | No |
| `OUTPUT_DIR` | Output directory path | `data/processed` | No |

### Programmatic Configuration

```python
from src.scraper import WebScraper

# Configure scraper instance
scraper = WebScraper(
    timeout=20,           # Request timeout in seconds
    max_retries=5,        # Number of retry attempts
    verify_ssl=True       # SSL certificate verification
)

# Configure with custom headers
scraper = WebScraper()
scraper.session.headers.update({
    'User-Agent': 'CustomBot/1.0',
    'Accept': 'text/html,application/xhtml+xml'
})
```

---

## 📚 Documentation

### Core Classes

#### `WebScraper`

Main scraping engine with retry logic and HTML parsing.

**Methods:**
- `scrape(url: str, selectors: dict = None) -> dict`: Scrape a single URL
- `scrape_multiple(urls: list[str]) -> list[dict]`: Scrape multiple URLs
- `fetch_page(url: str) -> str`: Fetch raw HTML content
- `parse_html(html: str) -> BeautifulSoup`: Parse HTML into BeautifulSoup object
- `extract_text(soup: BeautifulSoup) -> str`: Extract visible text
- `extract_links(soup: BeautifulSoup, base_url: str) -> list[str]`: Extract all links
- `extract_images(soup: BeautifulSoup, base_url: str) -> list[str]`: Extract all images

**Example:**
```python
scraper = WebScraper(timeout=15, max_retries=3)
result = scraper.scrape("https://example.com")
```

#### `AIAnalyzer`

AI-powered content analysis using OpenAI.

**Methods:**
- `analyze(content: dict, analysis_type: str, custom_prompt: str = None) -> dict`: Analyze content
- `summarize(text: str) -> str`: Generate summary
- `extract_entities(text: str) -> list`: Extract named entities
- `sentiment_analysis(text: str) -> dict`: Analyze sentiment
- `classify_content(text: str) -> str`: Classify content type

**Analysis Types:**
- `summarize`: Generate concise summary
- `entities`: Extract people, places, organizations
- `sentiment`: Determine emotional tone
- `classify`: Categorize content
- `keywords`: Extract key terms
- `full`: Comprehensive analysis

**Example:**
```python
analyzer = AIAnalyzer(api_key="your-key")
analysis = analyzer.analyze(data, analysis_type='summarize')
```

#### Utility Functions

**`save_to_json(data: dict, filename: str) -> str`**
- Saves data to JSON file with security validation

**`save_to_csv(data: list[dict], filename: str) -> str`**
- Exports data to CSV format

**`save_to_excel(data: list[dict], filename: str) -> str`**
- Exports data to Excel (XLSX) format

**`clean_text(text: str) -> str`**
- Removes extra whitespace and normalizes text

**`validate_url(url: str) -> bool`**
- Validates URL format

---

## 💻 Usage Examples

### Example 1: Simple Web Scraping

```python
from src.scraper import WebScraper
from src.utils import save_to_json

# Initialize scraper
scraper = WebScraper()

# Scrape a website
result = scraper.scrape("http://info.cern.ch/")

# Display results
print(f"✅ Scraped: {result['url']}")
print(f"📄 Title: {result['title']}")
print(f"📝 Text: {result['text'][:200]}...")
print(f"🔗 Links: {len(result['links'])} found")

# Save to file
save_to_json(result, "cern_scrape.json")
```

### Example 2: Custom CSS Selectors

```python
from src.scraper import WebScraper

scraper = WebScraper()

# Define custom selectors
selectors = {
    'headings': 'h1, h2, h3',
    'articles': 'article',
    'prices': '.price, .cost'
}

result = scraper.scrape("https://example.com", selectors=selectors)
```

### Example 3: Error Handling

```python
from src.scraper import WebScraper
from tenacity import RetryError

scraper = WebScraper(timeout=10, max_retries=3)

try:
    result = scraper.scrape("https://example.com")
    print(f"Success: {result['title']}")
except RetryError:
    print("Failed after all retry attempts")
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Example 4: Batch Processing with Progress

```python
from src.scraper import WebScraper
from src.utils import save_to_json

scraper = WebScraper()
urls = [
    "http://info.cern.ch/",
    "https://www.python.org/",
    "https://github.com/"
]

print(f"Scraping {len(urls)} URLs...")
results = scraper.scrape_multiple(urls)

successful = [r for r in results if not r.get('error')]
failed = [r for r in results if r.get('error')]

print(f"✅ Successful: {len(successful)}")
print(f"❌ Failed: {len(failed)}")

# Save successful results
for result in successful:
    filename = f"scrape_{result['url'].split('//')[1].replace('/', '_')}.json"
    save_to_json(result, filename)
```

### Example 5: AI Analysis Pipeline

```python
from src.scraper import WebScraper
from src.ai_analyzer import AIAnalyzer
from src.utils import save_to_json

# Scrape content
scraper = WebScraper()
data = scraper.scrape("https://example.com/article")

# Analyze with AI
analyzer = AIAnalyzer()

# Get summary
summary = analyzer.analyze(data, analysis_type='summarize')
print("Summary:", summary['summary'])

# Extract entities
entities = analyzer.analyze(data, analysis_type='entities')
print("Entities:", entities['entities'])

# Sentiment analysis
sentiment = analyzer.analyze(data, analysis_type='sentiment')
print("Sentiment:", sentiment['sentiment'])

# Save comprehensive analysis
save_to_json({
    'original': data,
    'summary': summary,
    'entities': entities,
    'sentiment': sentiment
}, "complete_analysis.json")
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_scraper.py -v
```

### Run with Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html
```

### Test Structure

- **test_scraper.py**: Tests for WebScraper class (26 tests)
- **test_ai_analyzer.py**: Tests for AIAnalyzer class
- **test_utils.py**: Tests for utility functions

---

## 🔍 Code Quality

This project maintains high code quality standards:

- **Grade**: A- (92/100)
- **Test Coverage**: 26+ unit tests
- **Type Hints**: Full type annotations
- **Security**: Path traversal protection, input validation
- **Logging**: Centralized configuration
- **Error Handling**: Comprehensive exception handling

### Recent Improvements

- ✅ Fixed hardcoded retry attempts (now configurable)
- ✅ Implemented centralized logging configuration
- ✅ Added security validations for file operations
- ✅ Removed unused imports and dead code
- ✅ Standardized type hints to Python 3.9+ syntax
- ✅ Added comprehensive input validation

See [CODE_QUALITY_REPORT.md](CODE_QUALITY_REPORT.md) for detailed analysis.

---

## 🚧 Roadmap

### Planned Features

- [ ] **Async Support**: Add `asyncio` for concurrent scraping
- [ ] **JavaScript Rendering**: Integrate Playwright/Selenium for dynamic content
- [ ] **Advanced Rate Limiting**: Implement sophisticated throttling strategies
- [ ] **Proxy Support**: Rotate proxies for large-scale scraping
- [ ] **Database Integration**: Direct export to PostgreSQL, MySQL, MongoDB
- [ ] **Scheduling**: Built-in cron-like scheduling for periodic scraping
- [ ] **Web UI**: Dashboard for monitoring and managing scraping jobs
- [ ] **Docker Support**: Containerized deployment
- [ ] **Plugin System**: Extensible architecture for custom scrapers

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/webscraper_ai.git
cd webscraper_ai

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 mypy pytest-cov

# Run tests
pytest tests/

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'src'`**
```bash
# Solution: Ensure you're in the project root directory
cd webscraper_ai
python -m pytest tests/
```

**Issue: `OpenAI API Error: Invalid API Key`**
```bash
# Solution: Check your .env file
cat .env | grep OPENAI_API_KEY
# Make sure the key is valid and has proper permissions
```

**Issue: `RetryError` when scraping**
```python
# Solution: Increase timeout and retries
scraper = WebScraper(timeout=30, max_retries=5)
```

**Issue: `PermissionError` when saving files**
```bash
# Solution: Check directory permissions
chmod 755 data/processed/
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **BeautifulSoup4**: HTML parsing library
- **Requests**: HTTP library for Python
- **OpenAI**: AI-powered analysis capabilities
- **Tenacity**: Retry logic implementation
- **Pydantic**: Data validation and settings management

---

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/baluchebolu1975/webscraper_ai/issues)
- **Documentation**: Check [QUICKSTART.md](QUICKSTART.md) and [SCRAPING_EXPLAINED.md](SCRAPING_EXPLAINED.md)
- **Examples**: See the `examples/` directory for working code

---

## 📊 Live Demo Results

**Successfully scraped http://info.cern.ch/ (World's First Website)**

```
✅ Status: Success (100% success rate)
⏱️  Execution Time: ~1 second
🔄 Retries: 0 (succeeded on first attempt)
📝 Text Extracted: 271 characters
🔗 Links Found: 4 URLs
🖼️  Images Found: 0
```

**Extracted Links:**
1. http://info.cern.ch/hypertext/WWW/TheProject.html
2. http://line-mode.cern.ch/www/hypertext/WWW/TheProject.html
3. http://home.web.cern.ch/topics/birth-web
4. http://home.web.cern.ch/about

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by [Balu Chebolu](https://github.com/baluchebolu1975)

[⬆ Back to Top](#-webscraper-ai)

</div>
