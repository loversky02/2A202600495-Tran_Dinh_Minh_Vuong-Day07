"""Simple CSV to TXT converter - creates exactly 4 documents."""

import csv
from pathlib import Path

data_dir = Path("data")

# 1. Convert CPI (1 document)
print("Converting CPI...")
with open(data_dir / "CPI (MoM and YoY).csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    row = next(reader)  # Get first row
    
    content = f"""Consumer Price Index (CPI) Report - December 2025

Release Date: {row['Release_Timestamp']}
Reference Period: {row['Reference_Period']}
Source: Bureau of Labor Statistics (BLS)
URL: {row['URL']}

Key Metrics:
- Month-over-Month Change: {row['Actual_Value']}%
- Year-over-Year Change: {row['YoY_Value']}%

Full BLS Press Release:
{row['Sentiment_Text']}

---
Official U.S. Government Data (Public Domain)
Data Quality: Official Government Data
"""
    
    output = data_dir / "bls_cpi_december_2025.txt"
    output.write_text(content, encoding='utf-8')
    print(f"✓ Created: {output.name} ({len(content):,} chars)")

# 2-4. Convert Fed Rates (3 documents)
print("\nConverting Fed Interest Rates...")
with open(data_dir / "fed_interest_rates_2023_2025.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)[:3]  # Get first 3 rows
    
    for i, row in enumerate(rows, 1):
        content = f"""Federal Reserve FOMC Statement

Date: {row['Date']}
Interest Rate: {row['Interest_Rate']}
Source: Federal Reserve Board
URL: {row['URL']}

Full FOMC Statement:
{row['Content']}

---
Official Federal Reserve Data (Public Domain)
Data Quality: Official Government Data
"""
        
        date_clean = row['Date'].replace('-', '_')
        output = data_dir / f"fed_fomc_statement_{date_clean}.txt"
        output.write_text(content, encoding='utf-8')
        print(f"✓ Created: {output.name} ({len(content):,} chars)")

print("\n" + "="*80)
print("✓ Conversion complete: 4 documents created")
print("="*80)
