# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WebScraper AI is a Python 3.9+ web scraping framework with OpenAI-powered content analysis. It combines intelligent scraping (requests + BeautifulSoup4) with AI analysis capabilities (summarization, NER, sentiment, classification, keyword extraction).

## Common Commands

```bash
# Run all tests
pytest tests/ -v

# Run a single test file
pytest tests/test_scraper.py -v

# Run a single test by name
pytest tests/test_scraper.py::TestClassName::test_method_name -v

# Run tests by marker
pytest tests/ -m slow -v
pytest tests/ -m integration -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html

# Format code (line-length=100)
black src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/

# Security scan
bandit -r src/

# Run examples
python examples/basic_scraping.py
python examples/demo_scraping.py
```

## Architecture

The codebase is organized into five modules under `src/`:

- **`scraper.py`** — `WebScraper` class: HTTP fetching with Tenacity retry/exponential backoff, session management, BeautifulSoup HTML parsing, batch scraping with rate limiting, link/image extraction
- **`ai_analyzer.py`** — `AIAnalyzer` class: OpenAI GPT integration for text summarization, entity extraction, sentiment analysis, content classification, keyword extraction, and custom prompts
- **`config.py`** — `Settings` class: Pydantic-based configuration loaded from `.env`. Exports a module-level `settings` singleton used by other modules. Has a `pydantic_settings`/`pydantic` import fallback for compatibility.
- **`logging_config.py`** — `setup_logging()` and `get_logger(name)`: call `get_logger(__name__)` in each module instead of `logging.getLogger` directly
- **`utils.py`** — Data export (JSON/CSV/Excel) with path traversal protection, URL validation, text cleaning, timestamp helpers

Tests mirror this structure in `tests/` with `test_scraper.py`, `test_ai_analyzer.py`, and `test_utils.py`. Test markers: `slow`, `integration`.

## Key Conventions

- Configuration via environment variables (`.env` file, see `.env.example`); `OPENAI_API_KEY` required for AI features
- Black formatting with 100-char line length, targeting Python 3.9–3.11
- Modules import via `from src.module import Class` — run from the project root, not as an installed package
- File export functions validate paths against traversal attacks (strip directory components, resolve canonical paths, check output stays within project root)
- Retry logic uses Tenacity with configurable `max_retries` (default 3), exponential backoff (2s–10s)
- CI runs via GitHub Actions: pytest with coverage → Pylint → Bandit → SonarCloud analysis
