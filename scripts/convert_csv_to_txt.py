"""
Convert CSV files to .txt format for RAG system.

This script converts real financial CSV data to readable .txt documents.
"""

import csv
from pathlib import Path
from datetime import datetime

def convert_cpi_csv():
    """Convert CPI CSV to readable .txt document."""
    data_dir = Path("data")
    csv_file = data_dir / "CPI (MoM and YoY).csv"
    
    if not csv_file.exists():
        print(f"❌ File not found: {csv_file}")
        return None
    
    # Read CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        print("❌ No data in CPI CSV")
        return None
    
    # Get the first (most recent) entry
    latest = rows[0]
    
    # Create readable document
    content = f"""Consumer Price Index (CPI) Report - Official BLS Data

Release Date: {latest['Release_Timestamp']}
Reference Period: {latest['Reference_Period']}
Event Type: {latest['Event_Type']}
Source: Bureau of Labor Statistics (BLS)
URL: {latest['URL']}

Key Metrics:
- Month-over-Month (MoM) Change: {latest['Actual_Value']}%
- Year-over-Year (YoY) Change: {latest['YoY_Value']}%

Full Report:
{latest['Sentiment_Text']}

---
This is official data from the U.S. Bureau of Labor Statistics.
All data is public domain and free to use for any purpose.
Data Quality: Official Government Data
"""
    
    # Save as .txt
    output_file = data_dir / "bls_cpi_report_latest.txt"
    output_file.write_text(content, encoding='utf-8')
    
    print(f"✓ Converted CPI CSV to: {output_file.name} ({len(content):,} chars)")
    
    return {
        'filename': output_file.name,
        'source': 'Bureau of Labor Statistics (BLS)',
        'chars': len(content),
        'metadata': {
            'category': 'inflation',
            'language': 'en',
            'document_type': 'government_press_release',
            'date': latest['Release_Timestamp'].split()[0],
            'source': 'BLS',
            'indicators': ['cpi', 'mom_change', 'yoy_change'],
            'data_quality': 'official_government_data'
        }
    }


def convert_fed_rates_csv():
    """Convert Fed Interest Rates CSV to readable .txt documents."""
    data_dir = Path("data")
    csv_file = data_dir / "fed_interest_rates_2023_2025.csv"
    
    if not csv_file.exists():
        print(f"❌ File not found: {csv_file}")
        return []
    
    # Read CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        print("❌ No data in Fed Rates CSV")
        return []
    
    documents = []
    
    # Convert first 3 most recent entries
    for i, row in enumerate(rows[:3]):
        date_str = row['Date']
        rate = row['Interest_Rate']
        
        content = f"""Federal Reserve FOMC Statement - Interest Rate Decision

Date: {date_str}
Interest Rate: {rate}
Source: Federal Reserve Board
URL: {row['URL']}

Full FOMC Statement:
{row['Content']}

---
This is an official Federal Reserve FOMC statement.
All data is public domain and free to use for any purpose.
Data Quality: Official Government Data
"""
        
        # Create filename
        date_clean = date_str.replace('-', '_')
        filename = f"fed_fomc_statement_{date_clean}.txt"
        output_file = data_dir / filename
        output_file.write_text(content, encoding='utf-8')
        
        print(f"✓ Converted Fed Rate #{i+1} to: {filename} ({len(content):,} chars)")
        
        documents.append({
            'filename': filename,
            'source': 'Federal Reserve',
            'chars': len(content),
            'metadata': {
                'category': 'monetary_policy',
                'language': 'en',
                'document_type': 'government_press_release',
                'date': date_str,
                'source': 'Federal Reserve',
                'indicators': ['interest_rates', 'federal_funds_rate'],
                'data_quality': 'official_government_data'
            }
        })
    
    return documents


def convert_fomc_communications_csv():
    """Convert FOMC Communications CSV to readable .txt documents."""
    data_dir = Path("data")
    csv_file = data_dir / "fomc_communications_2023_2025.csv"
    
    if not csv_file.exists():
        print(f"❌ File not found: {csv_file}")
        return []
    
    # Read CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        print("❌ No data in FOMC Communications CSV")
        return []
    
    documents = []
    
    # Convert first 2 most recent entries
    for i, row in enumerate(rows[:2]):
        date_str = row['Date']
        comm_type = row['Type']
        
        content = f"""Federal Reserve FOMC {comm_type}

Date: {date_str}
Type: {comm_type}
Source: Federal Reserve Board
URL: {row['URL']}

Full {comm_type}:
{row['Text']}

---
This is an official Federal Reserve FOMC {comm_type.lower()}.
All data is public domain and free to use for any purpose.
Data Quality: Official Government Data
"""
        
        # Create filename
        date_clean = date_str.replace('-', '_')
        type_clean = comm_type.lower()
        filename = f"fed_fomc_{type_clean}_{date_clean}.txt"
        output_file = data_dir / filename
        output_file.write_text(content, encoding='utf-8')
        
        print(f"✓ Converted FOMC {comm_type} #{i+1} to: {filename} ({len(content):,} chars)")
        
        documents.append({
            'filename': filename,
            'source': 'Federal Reserve',
            'chars': len(content),
            'metadata': {
                'category': 'monetary_policy',
                'language': 'en',
                'document_type': f'fomc_{type_clean}',
                'date': date_str,
                'source': 'Federal Reserve',
                'indicators': ['fomc_communications', 'monetary_policy'],
                'data_quality': 'official_government_data'
            }
        })
    
    return documents


def main():
    """Main conversion function."""
    print("\n" + "="*80)
    print("CONVERTING CSV FILES TO .TXT FORMAT")
    print("="*80)
    print("\nConverting real financial data from CSV to readable .txt documents...")
    print("\n" + "="*80)
    
    all_documents = []
    
    # Convert CPI
    print("\n[1/3] Converting CPI data...")
    cpi_doc = convert_cpi_csv()
    if cpi_doc:
        all_documents.append(cpi_doc)
    
    # Convert Fed Rates
    print("\n[2/3] Converting Fed Interest Rates...")
    fed_docs = convert_fed_rates_csv()
    all_documents.extend(fed_docs)
    
    # Convert FOMC Communications
    print("\n[3/3] Converting FOMC Communications...")
    fomc_docs = convert_fomc_communications_csv()
    all_documents.extend(fomc_docs)
    
    # Summary
    print("\n" + "="*80)
    print("CONVERSION COMPLETE")
    print("="*80)
    print(f"\nTotal documents created: {len(all_documents)}")
    print(f"Total characters: {sum(doc['chars'] for doc in all_documents):,}")
    
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(f"\n{'#':<3} {'Document Name':<45} {'Source':<20} {'Chars':<10}")
    print("-"*80)
    
    for i, doc in enumerate(all_documents, 1):
        print(f"{i:<3} {doc['filename']:<45} {doc['source']:<20} {doc['chars']:<10}")
    
    print("-"*80)
    print(f"\n✓ All CSV files converted to .txt format")
    print("✓ Ready to delete CSV files and keep only .txt files")
    
    return all_documents


if __name__ == "__main__":
    main()
