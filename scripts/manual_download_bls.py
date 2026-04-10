"""
Manual download helper for BLS Employment Situation data.

Since BLS blocks automated crawling, this script helps you process
manually downloaded data.

INSTRUCTIONS:
1. Go to: https://www.bls.gov/news.release/empsit.htm
2. Copy ALL the text from the page (Ctrl+A, Ctrl+C)
3. Save it to a file: data/bls_employment_raw.txt
4. Run this script: python scripts/manual_download_bls.py
"""

from pathlib import Path
from datetime import datetime
import re


def process_manual_download():
    """Process manually downloaded BLS employment data."""
    
    data_dir = Path("data")
    raw_file = data_dir / "bls_employment_raw.txt"
    
    if not raw_file.exists():
        print("❌ File not found: data/bls_employment_raw.txt")
        print("\nPlease follow these steps:")
        print("1. Go to: https://www.bls.gov/news.release/empsit.htm")
        print("2. Press Ctrl+A to select all text")
        print("3. Press Ctrl+C to copy")
        print("4. Create file: data/bls_employment_raw.txt")
        print("5. Paste the content (Ctrl+V) and save")
        print("6. Run this script again")
        return None
    
    print("Reading raw data...")
    content = raw_file.read_text(encoding='utf-8')
    
    # Extract release date
    release_date = None
    date_patterns = [
        r'For release (?:at )?[\d:]+ [ap]\.m\. \(ET\) (\w+ \d{1,2}, \d{4})',
        r'Release Date: (\w+ \d{1,2}, \d{4})',
        r'(\w+ \d{1,2}, \d{4})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, content)
        if match:
            release_date = match.group(1)
            break
    
    if not release_date:
        release_date = datetime.now().strftime("%B %d, %Y")
    
    # Clean up content
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    # Create formatted document
    document = f"""Bureau of Labor Statistics - Employment Situation Report

Title: The Employment Situation
Source: U.S. Bureau of Labor Statistics
Release Date: {release_date}
URL: https://www.bls.gov/news.release/empsit.htm
Data Type: Official Government Economic Data (Public Domain)

---

{content}

---

This is official data from the U.S. Bureau of Labor Statistics.
All data is public domain and free to use for any purpose.
Data Quality: Official Government Data
"""
    
    # Save to file
    date_str = datetime.now().strftime("%Y_%m_%d")
    filename = f"bls_employment_situation_{date_str}.txt"
    output_file = data_dir / filename
    
    output_file.write_text(document, encoding='utf-8')
    
    print(f"\n✓ Successfully processed and saved to: {output_file}")
    print(f"  File size: {len(document):,} characters")
    print(f"  Release date: {release_date}")
    
    # Optionally delete raw file
    print(f"\n  Raw file kept at: {raw_file}")
    print(f"  You can delete it if you want.")
    
    return output_file


if __name__ == "__main__":
    print("="*80)
    print("BLS EMPLOYMENT DATA - MANUAL DOWNLOAD PROCESSOR")
    print("="*80)
    print()
    
    process_manual_download()
