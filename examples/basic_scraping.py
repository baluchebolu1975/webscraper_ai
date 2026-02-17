"""
Basic web scraping example.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper import WebScraper
from src.ai_analyzer import AIAnalyzer
from src.utils import save_to_json, get_timestamp

# Constants
EXAMPLE_URL = "https://example.com"
EXAMPLE_ORG_URL = "https://example.org"


def basic_scraping_example():
    """Example of basic web scraping."""
    print("=" * 60)
    print("Basic Web Scraping Example")
    print("=" * 60)
    
    # Initialize scraper
    scraper = WebScraper()
    
    # Example URL (you can change this to any website)
    url = EXAMPLE_URL
    
    print(f"\n1. Scraping: {url}")
    data = scraper.scrape(url)
    
    if data and 'error' not in data:
        print(f"   ✓ Title: {data.get('title', 'N/A')}")
        print(f"   ✓ Found {len(data.get('links', []))} links")
        print(f"   ✓ Found {len(data.get('images', []))} images")
        print(f"   ✓ Text length: {len(data.get('text', ''))} characters")
    else:
        print(f"   ✗ Error: {data.get('error', 'Unknown error')}")
    
    # Save results
    filename = f"scrape_results_{get_timestamp()}.json"
    filepath = save_to_json(data, filename)
    print(f"\n2. Results saved to: {filepath}")
    
    scraper.close()
    print("\n✓ Scraping completed!")


def scraping_with_selectors_example():
    """Example of scraping with custom CSS selectors."""
    print("\n" + "=" * 60)
    print("Scraping with Custom Selectors")
    print("=" * 60)
    
    scraper = WebScraper()
    
    # Define custom selectors to extract specific content
    selectors = {
        'headings': 'h1, h2, h3',
        'paragraphs': 'p',
        'links_text': 'a'
    }
    
    url = EXAMPLE_URL
    print(f"\nScraping {url} with custom selectors...")
    
    data = scraper.scrape(url, selectors=selectors)
    
    if data and 'error' not in data:
        print(f"✓ Extracted headings: {len(data.get('headings', []))}")
        print(f"✓ Extracted paragraphs: {len(data.get('paragraphs', []))}")
        print(f"✓ Extracted link texts: {len(data.get('links_text', []))}")
        
        # Show first heading if available
        if data.get('headings'):
            print(f"\nFirst heading: {data['headings'][0][:100]}...")
    
    scraper.close()
    print("\n✓ Custom selector scraping completed!")


def ai_analysis_example():
    """Example of AI-powered content analysis."""
    print("\n" + "=" * 60)
    print("AI-Powered Content Analysis")
    print("=" * 60)
    
    # Initialize scraper and analyzer
    scraper = WebScraper()
    analyzer = AIAnalyzer()
    
    url = EXAMPLE_URL
    
    print(f"\n1. Scraping {url}...")
    data = scraper.scrape(url)
    
    if data and 'error' not in data:
        print("   ✓ Scraping successful")
        
        print("\n2. Analyzing content with AI...")
        try:
            # Perform AI analysis
            analysis = analyzer.analyze(data, analysis_type='summary')
            
            print("\n   Analysis Results:")
            print(f"   - Title: {analysis.get('title', 'N/A')}")
            print(f"   - Summary: {analysis.get('summary', 'N/A')[:200]}...")
            
            # Save analysis results
            filename = f"analysis_results_{get_timestamp()}.json"
            filepath = save_to_json(analysis, filename)
            print(f"\n3. Analysis saved to: {filepath}")
            
        except ValueError as e:
            print(f"\n   ⚠ AI analysis not available: {str(e)}")
            print("   Please set your OPENAI_API_KEY in .env file")
    
    scraper.close()
    print("\n✓ AI analysis completed!")


def multiple_urls_example():
    """Example of scraping multiple URLs."""
    print("\n" + "=" * 60)
    print("Scraping Multiple URLs")
    print("=" * 60)
    
    scraper = WebScraper()
    
    # List of URLs to scrape
    urls = [
        EXAMPLE_URL,
        EXAMPLE_ORG_URL,
    ]
    
    print(f"\nScraping {len(urls)} URLs with rate limiting...")
    results = scraper.scrape_multiple(urls, delay=1.0)
    
    print(f"\n✓ Scraped {len(results)} pages")
    for i, result in enumerate(results, 1):
        url = result.get('url', 'N/A')
        title = result.get('title', 'N/A')
        print(f"   {i}. {url}")
        print(f"      Title: {title}")
    
    # Save all results
    filename = f"multi_scrape_{get_timestamp()}.json"
    filepath = save_to_json(results, filename)
    print(f"\nResults saved to: {filepath}")
    
    scraper.close()
    print("\n✓ Multiple URL scraping completed!")


if __name__ == "__main__":
    print("\n🚀 WebScraper AI - Examples\n")
    
    try:
        # Run examples
        basic_scraping_example()
        scraping_with_selectors_example()
        multiple_urls_example()
        ai_analysis_example()
        
        print("\n" + "=" * 60)
        print("✨ All examples completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Examples interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()
