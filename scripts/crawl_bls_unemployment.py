"""
Crawl BLS Unemployment Rate data from official website.

This script fetches the latest Employment Situation report from BLS.
URL: https://www.bls.gov/news.release/empsit.htm
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import re


def crawl_bls_employment_report():
    """Crawl the latest BLS Employment Situation report."""
    
    url = "https://www.bls.gov/news.release/empsit.htm"
    
    print(f"Fetching data from: {url}")
    
    try:
        # Add headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else "Employment Situation Report"
        
        # Extract release date from the page
        release_date = None
        for p in soup.find_all('p'):
            text = p.get_text()
            if 'For release' in text or 'Release Date' in text:
                # Try to extract date
                date_match = re.search(r'(\w+ \d{1,2}, \d{4})', text)
                if date_match:
                    release_date = date_match.group(1)
                    break
        
        if not release_date:
            release_date = datetime.now().strftime("%B %d, %Y")
        
        # Extract main content
        # BLS reports typically have content in <div id="bodytext"> or <pre> tags
        content_div = soup.find('div', {'id': 'bodytext'})
        if not content_div:
            content_div = soup.find('pre')
        
        if not content_div:
            # Fallback: get all text
            content = soup.get_text()
        else:
            content = content_div.get_text()
        
        # Clean up content
        content = re.sub(r'\n{3,}', '\n\n', content)  # Remove excessive newlines
        content = content.strip()
        
        # Create formatted document
        document = f"""Bureau of Labor Statistics - Employment Situation Report

Title: {title}
Source: U.S. Bureau of Labor Statistics
Release Date: {release_date}
URL: {url}
Data Type: Official Government Economic Data (Public Domain)

---

{content}

---

This is official data from the U.S. Bureau of Labor Statistics.
All data is public domain and free to use for any purpose.
Data Quality: Official Government Data
"""
        
        # Save to file
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Create filename with date
        date_str = datetime.now().strftime("%Y_%m_%d")
        filename = f"bls_employment_situation_{date_str}.txt"
        output_file = data_dir / filename
        
        output_file.write_text(document, encoding='utf-8')
        
        print(f"\n✓ Successfully saved to: {output_file}")
        print(f"  File size: {len(document):,} characters")
        print(f"  Release date: {release_date}")
        
        return output_file
        
    except requests.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        print("\nAlternative: Download manually from:")
        print("  https://www.bls.gov/news.release/empsit.htm")
        return None
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        return None


if __name__ == "__main__":
    print("="*80)
    print("BLS EMPLOYMENT SITUATION REPORT CRAWLER")
    print("="*80)
    print("\nThis script fetches the latest unemployment rate data from BLS.")
    print("Source: https://www.bls.gov/news.release/empsit.htm")
    print("\nRequired packages: requests, beautifulsoup4")
    print("Install: pip install requests beautifulsoup4")
    print("\n" + "="*80)
    
    crawl_bls_employment_report()
