"""
Main web scraper module.
"""
import time
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings
from .utils import clean_text
from .logging_config import get_logger

logger = get_logger(__name__)


class WebScraper:
    """A flexible web scraper with retry logic and error handling."""
    
    # Constants
    RETRY_WAIT_MULTIPLIER = 1
    RETRY_WAIT_MIN = 2
    RETRY_WAIT_MAX = 10
    
    def __init__(self, timeout: Optional[int] = None, max_retries: Optional[int] = None):
        """
        Initialize the web scraper.
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            
        Raises:
            ValueError: If timeout or max_retries are invalid
        """
        # Validate inputs
        if timeout is not None and timeout <= 0:
            raise ValueError("Timeout must be positive")
        if max_retries is not None and max_retries < 0:
            raise ValueError("Max retries cannot be negative")
            
        self.timeout = timeout or settings.scraping_timeout
        self.max_retries = max_retries or settings.max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.user_agent
        })
        
        # Setup proxies if configured
        if settings.http_proxy or settings.https_proxy:
            self.session.proxies.update({
                'http': settings.http_proxy,
                'https': settings.https_proxy
            })
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL with retry logic.
        
        Args:
            url: The URL to fetch
            
        Returns:
            HTML content as string or None if failed
            
        Raises:
            ValueError: If URL is invalid
            requests.exceptions.RequestException: If fetching fails after retries
        """
        # Validate URL
        if not url or not url.strip():
            raise ValueError("URL cannot be empty")
        
        from urllib.parse import urlparse
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL format: {url}")
        
        # Use retry with instance-specific max_retries
        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(
                multiplier=self.RETRY_WAIT_MULTIPLIER,
                min=self.RETRY_WAIT_MIN,
                max=self.RETRY_WAIT_MAX
            )
        )
        def _fetch():
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            return response.text
        
        try:
            return _fetch()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            raise
    
    def parse_html(self, html: str, parser: str = "lxml") -> BeautifulSoup:
        """
        Parse HTML content using BeautifulSoup.
        
        Args:
            html: HTML content as string
            parser: Parser to use (lxml, html.parser, etc.)
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, parser)
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        """
        Extract all links from a BeautifulSoup object.
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links
            
        Returns:
            List of absolute URLs
        """
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if isinstance(href, str) and href:
                absolute_url = urljoin(base_url, href)
                links.append(absolute_url)
        
        return links
    
    def extract_text(self, soup: BeautifulSoup, selector: Optional[str] = None) -> str:
        """
        Extract text content from HTML.
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector to target specific elements
            
        Returns:
            Extracted and cleaned text
        """
        if selector:
            elements = soup.select(selector)
            text = ' '.join([el.get_text() for el in elements])
        else:
            text = soup.get_text()
        
        return clean_text(text)
    
    def extract_images(self, soup: BeautifulSoup, base_url: str) -> list[dict[str, str]]:
        """
        Extract image URLs and alt text.
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative URLs
            
        Returns:
            List of dictionaries with image info
        """
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if isinstance(src, str) and src:
                absolute_url = urljoin(base_url, src)
                alt = img.get('alt', '')
                title = img.get('title', '')
                images.append({
                    'url': absolute_url,
                    'alt': alt if isinstance(alt, str) else '',
                    'title': title if isinstance(title, str) else ''
                })
        
        return images
    
    def scrape(self, url: str, selectors: Optional[dict[str, str]] = None) -> dict[str, Any]:
        """
        Scrape a URL and extract structured data.
        
        Args:
            url: URL to scrape
            selectors: Dictionary of CSS selectors for specific elements
            
        Returns:
            Dictionary containing scraped data
            
        Raises:
            ValueError: If URL is invalid
        """
        # Validate URL
        if not url or not url.strip():
            raise ValueError("URL cannot be empty")
        
        try:
            # Fetch the page
            html = self.fetch_page(url)
            if not html:
                return {}
            
            # Parse HTML
            soup = self.parse_html(html)
            
            # Extract data
            data = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'text': self.extract_text(soup),
                'links': self.extract_links(soup, url),
                'images': self.extract_images(soup, url),
            }
            
            # Extract custom selectors if provided
            if selectors:
                for key, selector in selectors.items():
                    elements = soup.select(selector)
                    data[key] = [clean_text(el.get_text()) for el in elements]
            
            logger.info(f"Successfully scraped: {url}")
            return data
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return {'url': url, 'error': str(e)}
    
    def scrape_multiple(self, urls: list[str], delay: Optional[float] = None) -> list[dict[str, Any]]:
        """
        Scrape multiple URLs with rate limiting.
        
        Args:
            urls: List of URLs to scrape
            delay: Delay between requests in seconds
            
        Returns:
            List of scraped data dictionaries
        """
        delay = delay if delay is not None else settings.delay_between_requests
        results = []
        
        for url in urls:
            result = self.scrape(url)
            results.append(result)
            
            # Rate limiting
            if delay > 0:
                time.sleep(delay)
        
        return results
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
