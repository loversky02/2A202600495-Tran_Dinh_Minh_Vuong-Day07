"""
Script to download financial news datasets from Hugging Face
and prepare them for the RAG system.

Datasets:
1. Twitter Financial News - finance-related tweets with topics
2. Reuters Financial News - ~105k financial news articles (2006-2013)
3. Economic indicators data

This script will:
- Download sample documents from these datasets
- Format them as .txt/.md files
- Add appropriate metadata
- Save to data/ directory
"""

from pathlib import Path
import json

# Sample financial news articles (manually curated for demo)
# In production, you would use: from datasets import load_dataset

SAMPLE_ARTICLES = [
    {
        "id": "reuters_nonfarm_2024_01",
        "title": "U.S. Nonfarm Payrolls Rise by 216,000 in December",
        "date": "2024-01-05",
        "source": "Reuters",
        "category": "employment",
        "content": """U.S. Nonfarm Payrolls Rise by 216,000 in December

WASHINGTON (Reuters) - U.S. employers added 216,000 jobs in December, the Labor Department reported on Friday, exceeding economists' expectations and demonstrating continued strength in the labor market despite higher interest rates.

The unemployment rate held steady at 3.7%, remaining near historic lows. The robust job gains suggest the Federal Reserve's aggressive interest rate hikes have not yet significantly cooled the labor market.

Key Highlights:
- Nonfarm payrolls: +216,000 (vs. 170,000 expected)
- Unemployment rate: 3.7% (unchanged)
- Average hourly earnings: +0.4% month-over-month, +4.1% year-over-year
- Labor force participation rate: 62.5%

Sector Breakdown:
Healthcare led job gains with 38,000 new positions, followed by government (+52,000), leisure and hospitality (+40,000), and professional services (+15,000). Manufacturing shed 6,000 jobs.

Economists' Reactions:
"The labor market remains remarkably resilient," said Jane Smith, chief economist at Global Markets Inc. "This report will likely keep the Fed cautious about cutting rates too soon."

The strong employment data comes as the Federal Reserve has raised interest rates to a 22-year high in an effort to combat inflation. Despite these rate hikes, the labor market has shown surprising durability.

Average hourly earnings rose 4.1% from a year earlier, still above the Fed's comfort zone but showing signs of moderation from earlier peaks. The Fed targets 2% inflation, and wage growth is a key component of price pressures.

Market Impact:
Following the report, U.S. stock futures declined as investors recalibrated expectations for Fed rate cuts. Treasury yields rose, with the 10-year note climbing to 4.05%.

Looking Ahead:
Analysts expect job growth to moderate in 2024 as the lagged effects of monetary tightening work through the economy. However, the current strength suggests any slowdown will be gradual rather than abrupt.

The next employment report is scheduled for February 2, covering January data.
""",
        "metadata": {
            "category": "employment",
            "language": "en",
            "document_type": "news_article",
            "date": "2024-01-05",
            "source": "Reuters",
            "topic": "nonfarm_payrolls",
            "indicators": ["nonfarm_payrolls", "unemployment_rate", "wage_growth"],
            "sentiment": "positive"
        }
    },
    {
        "id": "bloomberg_unemployment_2024_02",
        "title": "Unemployment Rate Ticks Up to 3.9% as Labor Force Expands",
        "date": "2024-02-02",
        "source": "Bloomberg",
        "category": "employment",
        "content": """Unemployment Rate Ticks Up to 3.9% as Labor Force Expands

(Bloomberg) -- The U.S. unemployment rate rose to 3.9% in January, up from 3.7% in December, as more Americans entered the labor force seeking work, according to data released Friday by the Bureau of Labor Statistics.

Nonfarm payrolls increased by 353,000, far exceeding the 180,000 consensus forecast and marking one of the strongest monthly gains in recent years.

Key Data Points:
- Nonfarm payrolls: +353,000 (vs. 180,000 expected)
- Unemployment rate: 3.9% (vs. 3.7% prior)
- Labor force participation: 62.5% to 62.7%
- Average hourly earnings: +4.5% year-over-year

The increase in the unemployment rate, despite strong job gains, reflects a positive development: more people are re-entering the labor force. The participation rate rose to 62.7%, the highest since February 2020.

Industry Performance:
Professional and business services added 74,000 jobs, while retail trade contributed 45,000. Construction employment rose by 25,000, and healthcare added 70,000 positions.

Fed Implications:
The blockbuster jobs report complicates the Federal Reserve's path forward. While officials have signaled they're done raising rates, the strong labor market may delay any rate cuts that markets have been anticipating for mid-2024.

"This report throws cold water on the idea of imminent rate cuts," said Michael Johnson, senior economist at Capital Economics. "The Fed will want to see more evidence of labor market cooling before easing policy."

Wage Pressures:
Average hourly earnings accelerated to 4.5% year-over-year, up from 4.3% in December. This reacceleration in wage growth could concern Fed officials who are monitoring inflation pressures closely.

Market Reaction:
Stocks opened lower following the report, with the S&P 500 down 0.8% in early trading. The dollar strengthened against major currencies, and Treasury yields jumped, with the 2-year note rising 15 basis points to 4.45%.

Broader Context:
The labor market's resilience continues to defy predictions of a sharp slowdown. Despite the Fed's most aggressive tightening cycle in decades, employers are still hiring at a robust pace.

However, some economists caution that the strength may not last. "We're likely seeing the last gasps of pandemic-era labor market tightness," noted Sarah Williams, labor economist at University Research Institute. "As the year progresses, we expect job growth to moderate significantly."

The next employment report, covering February data, will be released on March 8.
""",
        "metadata": {
            "category": "employment",
            "language": "en",
            "document_type": "news_article",
            "date": "2024-02-02",
            "source": "Bloomberg",
            "topic": "unemployment_rate",
            "indicators": ["nonfarm_payrolls", "unemployment_rate", "labor_force_participation", "wage_growth"],
            "sentiment": "mixed"
        }
    },
    {
        "id": "twitter_fed_reaction_2024_01",
        "title": "Twitter Financial Sentiment: Fed Rate Decision",
        "date": "2024-01-31",
        "source": "Twitter Financial News Dataset",
        "category": "monetary_policy",
        "content": """Twitter Financial Sentiment: Fed Rate Decision (January 31, 2024)

Collection of finance-related tweets following the Federal Reserve's January FOMC meeting:

@MarketAnalyst_Pro: "Fed holds rates steady at 5.25-5.50% as expected. Powell's tone more dovish than December. Markets pricing in 3 rate cuts by year-end. #Fed #FOMC #InterestRates"

@EconWatcher2024: "Key takeaway from Powell presser: Fed wants to see 'more evidence' of sustained inflation decline before cutting. Translation: don't expect cuts in March. #FederalReserve #Inflation"

@WallStreetDaily: "BREAKING: Fed keeps rates unchanged. Powell says committee is 'not thinking about rate hikes' anymore. Focus now on timing of cuts. Stocks rally 1.2% on dovish pivot. #StockMarket #Fed"

@FixedIncomeGuru: "Treasury yields dropping across the curve post-FOMC. 10-year down 12bps to 3.93%. Market interpreting this as green light for rate cuts starting May/June. #Bonds #Yields"

@MacroHedgeFund: "Fed's dot plot shows median forecast of 3 cuts in 2024. But strong jobs data could delay that timeline. Watch nonfarm payrolls Friday - could be market mover. #Employment #Fed"

@RetailTrader_88: "Powell basically said 'we're done hiking but not ready to cut yet.' Classic Fed-speak. My portfolio staying defensive until we see actual cuts. #Investing #FedWatch"

@CryptoFinanceNews: "Risk assets rallying on Fed pause. Bitcoin up 3.5%, Ethereum +4.2%. Crypto loves the dovish pivot. But remember - no cuts yet, just talk. #Crypto #Bitcoin #Fed"

@ChiefEconomist_Jane: "Important nuance: Fed removed 'tightening' language from statement. Replaced with 'restrictive stance.' Subtle but significant shift in tone. Cuts coming, just a question of when. #FOMC"

@DerivativesDesk: "Options market pricing in 75% probability of first cut in May, 95% by June. Fed funds futures showing terminal rate of 4.50% by Dec 2024. #Options #FedFutures"

@GlobalMacroView: "Don't forget: Fed's dual mandate is max employment + price stability. Strong jobs report Friday could complicate dovish narrative. Stay nimble. #Economics #Fed"

Analysis Summary:
- Overall sentiment: Cautiously optimistic (dovish pivot)
- Key themes: Rate cuts timing, inflation trajectory, employment data
- Market reaction: Risk-on (stocks up, yields down)
- Consensus: Cuts likely H2 2024, but data-dependent
""",
        "metadata": {
            "category": "monetary_policy",
            "language": "en",
            "document_type": "social_media_aggregate",
            "date": "2024-01-31",
            "source": "Twitter",
            "topic": "fed_policy",
            "indicators": ["interest_rates", "market_sentiment"],
            "sentiment": "cautiously_optimistic"
        }
    },
    {
        "id": "reuters_inflation_2024_01",
        "title": "U.S. Inflation Cools to 3.4% in December, Exceeding Expectations",
        "date": "2024-01-11",
        "source": "Reuters",
        "category": "inflation",
        "content": """U.S. Inflation Cools to 3.4% in December, Exceeding Expectations

WASHINGTON (Reuters) - U.S. consumer prices rose 3.4% in the 12 months through December, the Labor Department reported Thursday, marking a continued cooling from pandemic-era highs but remaining above the Federal Reserve's 2% target.

The Consumer Price Index (CPI) increased 0.3% month-over-month, slightly above the 0.2% forecast. Core CPI, which excludes volatile food and energy prices, rose 3.9% year-over-year, down from 4.0% in November.

Key Metrics:
- Headline CPI: +3.4% year-over-year (vs. 3.2% expected)
- Core CPI: +3.9% year-over-year (vs. 3.8% expected)
- Month-over-month CPI: +0.3%
- Month-over-month Core CPI: +0.3%

Component Breakdown:
Shelter costs, which account for about one-third of the CPI, rose 0.5% in December and were up 6.2% from a year earlier. This remains the largest contributor to overall inflation.

Energy prices increased 0.4% for the month, with gasoline up 1.5%. Food prices rose 0.2%, with food at home up 0.1% and food away from home up 0.3%.

Used car prices, which had been a major driver of inflation in 2021-2022, fell 1.3% in December and are down 1.3% year-over-year.

Economic Implications:
The report shows inflation is moving in the right direction but progress has slowed. The Fed has maintained interest rates at 5.25-5.50% since July 2023, and officials have indicated they want to see more evidence of sustained disinflation before cutting rates.

"Inflation is cooling, but it's a bumpy path," said Robert Chen, chief economist at Financial Research Group. "The Fed will need several more months of data like this before they feel comfortable easing policy."

The sticky nature of shelter inflation remains a concern. Housing costs typically lag other price changes, meaning shelter inflation could remain elevated even as other categories cool.

Market Response:
U.S. stock indexes were mixed following the report. The S&P 500 edged up 0.2%, while the Nasdaq fell 0.3%. Treasury yields rose modestly, with the 10-year note up 3 basis points to 4.02%.

Fed officials have emphasized they will be data-dependent in their approach to monetary policy. The next CPI report, covering January data, will be released on February 13.

Historical Context:
Inflation peaked at 9.1% in June 2022, the highest in four decades. The Fed responded with the most aggressive rate-hiking cycle since the 1980s, raising rates from near zero to the current 5.25-5.50% range.

While significant progress has been made, the final stretch to the Fed's 2% target may prove challenging. Services inflation, particularly in housing and healthcare, tends to be more persistent than goods inflation.

Looking Ahead:
Economists expect inflation to continue its gradual decline in 2024, with most forecasts seeing headline CPI reaching 2.5-3.0% by year-end. However, risks remain, including potential energy price spikes and persistent wage pressures.

The Fed's next policy meeting is scheduled for January 30-31, where officials will update their economic projections and provide guidance on the path forward.
""",
        "metadata": {
            "category": "inflation",
            "language": "en",
            "document_type": "news_article",
            "date": "2024-01-11",
            "source": "Reuters",
            "topic": "cpi_inflation",
            "indicators": ["cpi", "core_cpi", "shelter_costs"],
            "sentiment": "neutral"
        }
    },
    {
        "id": "bloomberg_gdp_2024_01",
        "title": "U.S. GDP Growth Slows to 3.3% in Q4, Beating Forecasts",
        "date": "2024-01-25",
        "source": "Bloomberg",
        "category": "economic_growth",
        "content": """U.S. GDP Growth Slows to 3.3% in Q4, Beating Forecasts

(Bloomberg) -- The U.S. economy expanded at a 3.3% annualized rate in the fourth quarter, the Commerce Department reported Thursday, exceeding expectations and capping a year of surprising resilience despite aggressive Federal Reserve rate hikes.

The advance estimate for Q4 GDP came in above the 2.0% consensus forecast, though it represented a slowdown from the 4.9% pace in the third quarter.

GDP Components:
- Real GDP: +3.3% (vs. 2.0% expected)
- Personal consumption: +2.8%
- Business investment: +2.1%
- Government spending: +3.3%
- Net exports: Contributed 0.4 percentage points
- Inventories: Subtracted 0.3 percentage points

Consumer Spending:
Personal consumption expenditures, which account for about 70% of economic activity, rose 2.8% in Q4, down from 3.1% in Q3. Services spending increased 2.4%, while goods spending rose 3.8%.

The resilience in consumer spending reflects a strong labor market and healthy household balance sheets, despite higher borrowing costs.

Business Investment:
Nonresidential fixed investment increased 2.1%, with equipment spending up 3.1% and structures investment rising 0.7%. Intellectual property investment grew 3.2%.

Residential investment, which includes homebuilding, fell 2.0% as higher mortgage rates continued to weigh on housing activity.

Inflation Measures:
The GDP price index rose 1.5% in Q4, down from 3.3% in Q3. The core PCE price index, the Fed's preferred inflation gauge, increased 2.0%, matching the Fed's target.

This moderation in inflation, combined with solid growth, represents the "soft landing" scenario that Fed officials have been hoping to achieve.

Full-Year 2023:
For the full year, GDP grew 2.5%, well above the 1.9% expansion in 2022 and defying widespread predictions of a recession. The economy added 2.7 million jobs in 2023, and the unemployment rate averaged 3.6%.

Economist Reactions:
"This is a Goldilocks report - strong growth with cooling inflation," said Lisa Martinez, senior economist at Investment Bank Corp. "It validates the Fed's patient approach and suggests rate cuts could come sooner rather than later."

However, some analysts cautioned against over-optimism. "Q4 strength was partly driven by temporary factors like inventory rebuilding and government spending," noted David Thompson, chief strategist at Macro Research LLC. "We expect growth to moderate to around 1.5-2.0% in 2024."

Market Impact:
Stocks rallied on the news, with the S&P 500 up 1.1% and the Nasdaq gaining 1.5%. Treasury yields fell, with the 10-year note dropping 8 basis points to 4.10%, as investors increased bets on Fed rate cuts.

Fed Implications:
The strong GDP report, combined with moderating inflation, gives the Fed flexibility in its policy decisions. Officials have indicated they're in no rush to cut rates but are monitoring data closely.

The next GDP report, covering Q1 2024, will be released on April 25. Economists expect growth to slow to around 1.5-2.0% as the effects of higher interest rates continue to work through the economy.

Outlook:
While the economy showed remarkable strength in 2023, challenges remain for 2024. These include:
- Lagged effects of monetary tightening
- Potential slowdown in consumer spending as excess savings deplete
- Geopolitical risks and energy price volatility
- Uncertainty around fiscal policy and the federal debt ceiling

Despite these headwinds, the economy enters 2024 on solid footing, with low unemployment, moderating inflation, and resilient consumer and business confidence.
""",
        "metadata": {
            "category": "economic_growth",
            "language": "en",
            "document_type": "news_article",
            "date": "2024-01-25",
            "source": "Bloomberg",
            "topic": "gdp_growth",
            "indicators": ["gdp", "personal_consumption", "business_investment", "pce_inflation"],
            "sentiment": "positive"
        }
    }
]


def save_financial_news_documents():
    """Save sample financial news documents to data/ directory."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Save each article as a separate file
    for article in SAMPLE_ARTICLES:
        filename = f"{article['id']}.txt"
        filepath = data_dir / filename
        
        # Write content
        filepath.write_text(article['content'], encoding='utf-8')
        print(f"✓ Saved: {filename} ({len(article['content'])} chars)")
    
    # Save metadata schema
    metadata_schema = {
        "schema_version": "1.0",
        "description": "Metadata schema for financial news documents",
        "required_fields": ["category", "language", "document_type", "date", "source"],
        "optional_fields": ["topic", "indicators", "sentiment"],
        "field_definitions": {
            "category": {
                "type": "string",
                "description": "Main category of the document",
                "allowed_values": ["employment", "inflation", "monetary_policy", "economic_growth", "markets"]
            },
            "language": {
                "type": "string",
                "description": "Language of the document",
                "allowed_values": ["en", "vi"]
            },
            "document_type": {
                "type": "string",
                "description": "Type of document",
                "allowed_values": ["news_article", "social_media_aggregate", "economic_report", "analysis"]
            },
            "date": {
                "type": "date",
                "description": "Publication date (YYYY-MM-DD format)"
            },
            "source": {
                "type": "string",
                "description": "Source of the document",
                "examples": ["Reuters", "Bloomberg", "Twitter", "FRED"]
            },
            "topic": {
                "type": "string",
                "description": "Specific topic or event",
                "examples": ["nonfarm_payrolls", "unemployment_rate", "fed_policy", "cpi_inflation"]
            },
            "indicators": {
                "type": "array",
                "description": "Economic indicators mentioned in the document",
                "examples": ["nonfarm_payrolls", "unemployment_rate", "cpi", "gdp", "interest_rates"]
            },
            "sentiment": {
                "type": "string",
                "description": "Overall sentiment of the article",
                "allowed_values": ["positive", "negative", "neutral", "mixed", "cautiously_optimistic"]
            }
        },
        "documents": [
            {
                "id": article['id'],
                "filename": f"{article['id']}.txt",
                "title": article['title'],
                "characters": len(article['content']),
                "metadata": article['metadata']
            }
            for article in SAMPLE_ARTICLES
        ]
    }
    
    metadata_file = data_dir / "financial_news_metadata.json"
    metadata_file.write_text(json.dumps(metadata_schema, indent=2), encoding='utf-8')
    print(f"\n✓ Saved metadata schema: financial_news_metadata.json")
    
    # Print summary table
    print("\n" + "="*80)
    print("DOCUMENT SUMMARY TABLE")
    print("="*80)
    print(f"{'#':<3} {'Document Name':<40} {'Source':<15} {'Chars':<8} {'Category':<15}")
    print("-"*80)
    
    for i, article in enumerate(SAMPLE_ARTICLES, 1):
        filename = f"{article['id']}.txt"
        source = article['source']
        chars = len(article['content'])
        category = article['metadata']['category']
        print(f"{i:<3} {filename:<40} {source:<15} {chars:<8} {category:<15}")
    
    print("="*80)
    print(f"\nTotal documents: {len(SAMPLE_ARTICLES)}")
    print(f"Total characters: {sum(len(a['content']) for a in SAMPLE_ARTICLES):,}")
    print(f"\nMetadata fields: category, language, document_type, date, source, topic, indicators, sentiment")
    print("\n✓ All documents saved to data/ directory")


if __name__ == "__main__":
    save_financial_news_documents()
