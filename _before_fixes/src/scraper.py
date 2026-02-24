"""
Main web scraper module.
"""
import logging
import time
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, rate_limit

from .config import settings
from .utils import clean_text

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebScraper:
    """A flexible web scraper with retry logic and error handling."""
    
    def __init__(self, timeout: int = None, max_retries: int = None, user_agent: str = None):
        """
        Initialize the web scraper.
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            user_agent: Custom user agent string
        """
        self.timeout = timeout or settings.scraping.timeout
        self.max_retries = max_retries or settings.scraping.max_retries
        self.user_agent = user_agent or settings.scraping.user_agent
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent
        })
        
        # Configure proxies if provided
        if settings.scraping.proxy_url:
            self.session.proxies = {
                'http': settings.scraping.proxy_url,
                'https': settings.scraping.proxy_url
            }
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.session.close()
    
    @retry(stop=stop_after_attempt(3))
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a page with retry logic.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            raise
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content.
        
        Args:
            html: HTML string
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, 'lxml')
    
    def extract_text(self, soup: BeautifulSoup, selector: Optional[str] = None) -> str:
        """
        Extract text from HTML.
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector (optional)
            
        Returns:
            Extracted text
        """
        if selector:
            elements = soup.select(selector)
            text = ' '.join(el.get_text() for el in elements)
        else:
            text = soup.get_text()
        
        return clean_text(text)
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Extract all links from page.
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links
            
        Returns:
            List of absolute URLs
        """
        links = []
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(base_url, link['href'])
            links.append(absolute_url)
        return links
    
    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """
        Extract image information.
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative URLs
            
        Returns:
            List of dictionaries with image data
        """
        images = []
        for img in soup.find_all('img'):
            img_data = {
                'src': urljoin(base_url, img.get('src', '')),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            }
            images.append(img_data)
        return images
    
    def scrape(self, url: str, selectors: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Scrape a single page.
        
        Args:
            url: URL to scrape
            selectors: Dictionary of CSS selectors for specific content
            
        Returns:
            Dictionary with scraped data
        """
        html = self.fetch_page(url)
        if not html:
            return {}
        
        soup = self.parse_html(html)
        
        data = {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'text': self.extract_text(soup),
            'links': self.extract_links(soup, url),
            'images': self.extract_images(soup, url),
            'metadata': {
                'scraped_at': time.time()
            }
        }
        
        # Extract custom selectors if provided
        if selectors:
            data['custom'] = {}
            for name, selector in selectors.items():
                elements = soup.select(selector)
                data['custom'][name] = [el.get_text().strip() for el in elements]
        
        return data
    
    def scrape_multiple(self, urls: List[str], delay: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Scrape multiple URLs with optional delay.
        
        Args:
            urls: List of URLs to scrape
            delay: Delay between requests in seconds
            
        Returns:
            List of scraped data dictionaries
        """
        results = []
        for url in urls:
            try:
                data = self.scrape(url)
                results.append(data)
                
                if delay and url != urls[-1]:  # Don't delay after last URL
                    time.sleep(delay)
            except Exception as e:
                logger.error(f"Failed to scrape {url}: {e}")
                results.append({'url': url, 'error': str(e)})
        
        return results
