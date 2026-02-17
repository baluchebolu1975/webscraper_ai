"""
Simple demo to show actual web scraping with real results.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper import WebScraper
from src.utils import save_to_json, get_timestamp
import json


def demo_real_scraping():
    """Demonstrate actual web scraping with a working URL."""
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "WEB SCRAPING DEMONSTRATION" + " " * 16 + "║")
    print("╚" + "═" * 58 + "╝\n")
    
    # Initialize scraper with custom config
    scraper = WebScraper(timeout=10, max_retries=2)
    
    # Use a simple, reliable test URL
    url = "http://info.cern.ch/"  # First website ever created, still online!
    
    print(f"🌐 Target URL: {url}")
    print(f"⚙️  Configuration:")
    print(f"   • Timeout: {scraper.timeout}s")
    print(f"   • Max Retries: {scraper.max_retries}")
    print(f"\n{'─' * 60}")
    print("📡 Starting scrape operation...\n")
    
    try:
        # Perform the scrape
        data = scraper.scrape(url)
        
        if data and 'error' not in data:
            print("✅ SCRAPING SUCCESSFUL!\n")
            print("📊 Results Summary:")
            print(f"   • Page Title: {data.get('title', 'N/A')}")
            print(f"   • Text Length: {len(data.get('text', ''))} characters")
            print(f"   • Links Found: {len(data.get('links', []))} links")
            print(f"   • Images Found: {len(data.get('images', []))} images")
            
            # Show first few links
            links = data.get('links', [])
            if links:
                print(f"\n🔗 Sample Links (first 5):")
                for i, link in enumerate(links[:5], 1):
                    print(f"   {i}. {link}")
            
            # Show extracted text preview
            text = data.get('text', '')
            if text:
                print(f"\n📄 Text Preview (first 200 chars):")
                print(f"   \"{text[:200].strip()}...\"")
            
            # Save to file
            filename = f"demo_scrape_{get_timestamp()}.json"
            filepath = save_to_json(data, filename)
            print(f"\n💾 Full results saved to:")
            print(f"   {filepath}")
            
            # Display JSON structure
            print(f"\n📋 JSON Structure:")
            print(json.dumps({
                'url': data['url'],
                'title': data.get('title', 'N/A'),
                'text_length': len(data.get('text', '')),
                'links_count': len(data.get('links', [])),
                'images_count': len(data.get('images', []))
            }, indent=2))
            
        else:
            error = data.get('error', 'Unknown error')
            print(f"❌ SCRAPING FAILED: {error}")
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        scraper.close()
        print(f"\n{'─' * 60}")
        print("✓ Scraper session closed")


if __name__ == "__main__":
    demo_real_scraping()
    print("\n🎉 Demo completed!\n")
