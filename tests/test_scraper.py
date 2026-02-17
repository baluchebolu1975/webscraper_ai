"""
Tests for the web scraper module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.scraper import WebScraper
from bs4 import BeautifulSoup


@pytest.fixture
def scraper():
    """Create a WebScraper instance for testing."""
    return WebScraper(timeout=10, max_retries=2)


@pytest.fixture
def sample_html():
    """Sample HTML for testing."""
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Main Heading</h1>
            <p>This is a test paragraph.</p>
            <a href="/relative">Relative Link</a>
            <a href="https://example.com/absolute">Absolute Link</a>
            <img src="/image.jpg" alt="Test Image" />
        </body>
    </html>
    """


def test_scraper_initialization(scraper):
    """Test scraper initialization."""
    assert scraper.timeout == 10
    assert scraper.max_retries == 2
    assert scraper.session is not None


def test_parse_html(scraper, sample_html):
    """Test HTML parsing."""
    soup = scraper.parse_html(sample_html)
    assert isinstance(soup, BeautifulSoup)
    assert soup.title.string == "Test Page"


def test_extract_text(scraper, sample_html):
    """Test text extraction."""
    soup = scraper.parse_html(sample_html)
    text = scraper.extract_text(soup)
    assert "Main Heading" in text
    assert "test paragraph" in text


def test_extract_links(scraper, sample_html):
    """Test link extraction."""
    soup = scraper.parse_html(sample_html)
    base_url = "https://example.com"
    links = scraper.extract_links(soup, base_url)
    
    assert len(links) == 2
    assert "https://example.com/relative" in links
    assert "https://example.com/absolute" in links


def test_extract_images(scraper, sample_html):
    """Test image extraction."""
    soup = scraper.parse_html(sample_html)
    base_url = "https://example.com"
    images = scraper.extract_images(soup, base_url)
    
    assert len(images) == 1
    assert images[0]['url'] == "https://example.com/image.jpg"
    assert images[0]['alt'] == "Test Image"


@patch('src.scraper.requests.Session')
def test_fetch_page_success(mock_session_class, scraper):
    """Test successful page fetching."""
    mock_response = Mock()
    mock_response.text = "<html><body>Test</body></html>"
    mock_response.status_code = 200
    
    mock_session = Mock()
    mock_session.get.return_value = mock_response
    scraper.session = mock_session
    
    html = scraper.fetch_page("https://example.com")
    assert html == "<html><body>Test</body></html>"
    mock_session.get.assert_called_once()


@patch('src.scraper.requests.Session')
def test_fetch_page_failure(mock_session_class, scraper):
    """Test page fetching failure."""
    mock_session = Mock()
    mock_session.get.side_effect = Exception("Connection error")
    scraper.session = mock_session
    
    with pytest.raises(Exception):
        scraper.fetch_page("https://example.com")


def test_scrape_with_selectors(scraper, sample_html):
    """Test scraping with custom selectors."""
    with patch.object(scraper, 'fetch_page', return_value=sample_html):
        selectors = {
            'headings': 'h1',
            'paragraphs': 'p'
        }
        data = scraper.scrape("https://example.com", selectors=selectors)
        
        assert 'headings' in data
        assert 'paragraphs' in data
        assert len(data['headings']) == 1
        assert "Main Heading" in data['headings'][0]


def test_context_manager(scraper):
    """Test context manager functionality."""
    with scraper as s:
        assert s is not None
    # Session should be closed after context exit
    # We can't directly test if session is closed, but we ensure no errors occur


def test_scrape_multiple():
    """Test scraping multiple URLs."""
    scraper = WebScraper()
    sample_html = "<html><body>Test</body></html>"
    
    with patch.object(scraper, 'fetch_page', return_value=sample_html):
        urls = ["https://example1.com", "https://example2.com"]
        results = scraper.scrape_multiple(urls, delay=0)
        
        assert len(results) == 2
        assert all('url' in r for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
