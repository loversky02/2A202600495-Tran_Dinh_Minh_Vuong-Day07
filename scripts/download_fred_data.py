"""
Download REAL economic data from FRED (Federal Reserve Economic Data).

This downloads actual government data:
- Nonfarm Payrolls (PAYEMS)
- Unemployment Rate (UNRATE)
- CPI (CPIAUCSL)
- GDP (GDP)

Installation: pip install fredapi pandas
Get free API key: https://fred.stlouisfed.org/docs/api/api_key.html
"""

import os
from pathlib import Path

def download_fred_data():
    """Download real economic indicators from FRED."""
    try:
        from fredapi import Fred
        import pandas as pd
    except ImportError:
        print("❌ Please install required libraries:")
        print("   pip install fredapi pandas")
        return False
    
    # Check for API key
    api_key = os.getenv('FRED_API_KEY')
    if not api_key:
        print("❌ FRED API key not found!")
        print("\nTo get real data from FRED:")
        print("1. Get free API key: https://fred.stlouisfed.org/docs/api/api_key.html")
        print("2. Set environment variable: FRED_API_KEY=your_key")
        print("3. Or add to .env file: FRED_API_KEY=your_key")
        return False
    
    fred = Fred(api_key=api_key)
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print("\n" + "="*80)
    print("DOWNLOADING REAL ECONOMIC DATA FROM FRED")
    print("="*80)
    
    # Series to download
    series = {
        'PAYEMS': 'Nonfarm Payrolls (Total Employees)',
        'UNRATE': 'Unemployment Rate',
        'CPIAUCSL': 'Consumer Price Index (CPI)',
        'GDP': 'Gross Domestic Product',
        'FEDFUNDS': 'Federal Funds Rate'
    }
    
    for series_id, description in series.items():
        try:
            print(f"\n[{series_id}] Downloading {description}...")
            data = fred.get_series(series_id, observation_start='2020-01-01')
            
            # Create document
            filename = f"fred_{series_id.lower()}_data.txt"
            filepath = data_dir / filename
            
            # Format as readable document
            content = f"""FRED Economic Data: {description}

Source: Federal Reserve Economic Data (FRED)
Series ID: {series_id}
URL: https://fred.stlouisfed.org/series/{series_id}
Data Range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}
Observations: {len(data)}

Latest 12 Months:
"""
            
            # Add latest 12 data points
            recent_data = data.tail(12)
            for date, value in recent_data.items():
                content += f"{date.strftime('%Y-%m-%d')}: {value:,.2f}\n"
            
            content += f"\nStatistics (Last 12 Months):\n"
            content += f"- Mean: {recent_data.mean():,.2f}\n"
            content += f"- Min: {recent_data.min():,.2f}\n"
            content += f"- Max: {recent_data.max():,.2f}\n"
            content += f"- Latest: {recent_data.iloc[-1]:,.2f}\n"
            
            if len(recent_data) >= 2:
                change = recent_data.iloc[-1] - recent_data.iloc[-2]
                pct_change = (change / recent_data.iloc[-2]) * 100
                content += f"- Month-over-month change: {change:+,.2f} ({pct_change:+.2f}%)\n"
            
            content += f"\n---\nThis is REAL economic data from the Federal Reserve.\n"
            
            filepath.write_text(content, encoding='utf-8')
            print(f"  ✓ Saved: {filename} ({len(content)} chars)")
            
        except Exception as e:
            print(f"  ❌ Error downloading {series_id}: {e}")
    
    print("\n" + "="*80)
    print("DOWNLOAD COMPLETE - ALL DATA IS REAL")
    print("="*80)
    return True


if __name__ == "__main__":
    success = download_fred_data()
    
    if not success:
        print("\n" + "="*80)
        print("ALTERNATIVE: Manual Download")
        print("="*80)
        print("\nYou can manually download real data:")
        print("\n1. Visit: https://fred.stlouisfed.org/")
        print("2. Search for series (e.g., 'PAYEMS', 'UNRATE', 'CPIAUCSL')")
        print("3. Click 'Download' → Select format (CSV/TXT)")
        print("4. Save to data/ directory")
        print("\nOr use these direct links:")
        print("- Nonfarm Payrolls: https://fred.stlouisfed.org/series/PAYEMS")
        print("- Unemployment Rate: https://fred.stlouisfed.org/series/UNRATE")
        print("- CPI: https://fred.stlouisfed.org/series/CPIAUCSL")
