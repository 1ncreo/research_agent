# AI Company Research Agent

An AI-powered research agent that gathers and analyzes comprehensive company data based on a company name. The tool extracts information from multiple sources to provide a detailed company profile.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Features

- Company Overview (Headquarters, industry, founding year, CEO, key executives)
- Financial Information (Revenue, market cap, stock performance)
- Number of Employees (From official sources and estimates)
- Recent News with Sentiment Analysis
- Social Media & Public Sentiment Analysis
- Competitor Analysis
- Company Growth Trends and Forecasting

## Tech Stack

- **Backend**: Python with Flask
- **AI/NLP Processing**: TextBlob, NLTK
- **Web Scraping**: BeautifulSoup, Requests
- **Data Sources**: Yahoo Finance, Yahoo News, Reddit, and more
- **Storage**: MongoDB (can be configured for local storage)

## Installation

1. Clone the repository:
    ```bash
    git clone "https://github.com/1ncreo/research_agent.git"
    cd company-research-agent
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  
    ```

3. Install Requirements:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file in the root directory with the following variables:
    ```plaintext
    NEWS_API_KEY=your_news_api_key  
    ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key  
    MONGO_URI=your_mongo_uri
    MONGO_DB=company_research
    CRUNCHBASE_API=your_crunchbase_api_key
    TWITTER_API_KEY=your_twitter_api_key
    TWITTER_SECRET_KEY=your_twitter_secret_key
    ```

5. Run the application:
    ```bash
    python app.py
    ```

## Usage

1. Open a web browser and navigate to [http://127.0.0.1:5000/templates/research_form.html](http://127.0.0.1:5000/templates/research_form.html)
2. Enter a company name to research.
3. View the comprehensive research results.

## Project Structure

- `app.py`: Main entry point and Flask application
- `config.py`: Configuration settings
- `core.py`: Core research engine
- `data_collectors/`: Modules for collecting data from various sources
- `analysis/`: Modules for sentiment analysis and trends
- `storage/`: Database interaction
- `api/`: API endpoints

## Sample Report

```
{
  "company_name": "microsoft",
  "competitors": [
    {
      "employees": 164,000,
      "industry": IT,
      "market_cap": $3210 billion,
      "name": "Apple"
    },
    {
      "employees": 180,000,
      "industry": Tech,
      "market_cap": $2033 billion,
      "name": "Google"
    },
    {
      "employees": 1,556,000,
      "industry": Tech,
      "market_cap": $2089 billion,
      "name": "Amazon"
    }
  ],
  "financials": {
    "annual_revenue": $245 billion,
    "funding_rounds": 2,
    "market_cap": $2897 billion,
    "stock_price": $388
  },
  "growth_trends": null,
  "overview": {
    "ceo": "Satya Nadella (chairman & CEO)Brad Smith (vice chairman & president)Bill Gates (technical adviser)",
    "company_name": "microsoft",
    "employees": "228,000",
    "founded": 1975,
    "headquarters": "One Microsoft Way, Redmond, Washington, U.S.",
    "industry": "Information technology"
  },
  "recent_news": [
    {
      "date": "2025-03-15",
      "headline": "Intel (NasdaqGS:INTC) Sees 18% Price Move As Lip-Bu Tan Appointed CEO",
      "sentiment": "Positive",
      "sentiment_confidence": "Medium",
      "sentiment_score": 0.48,
      "source": "Yahoo Entertainment",
      "summary": "Intel (NasdaqGS:INTC) experienced a significant stock price increase of 18% over the last quarter amid several key developments. The appointment of Lip-Bu...",
      "url": "https://finance.yahoo.com/news/intel-nasdaqgs-intc-sees-18-171440422.html"
    },
    {
      "date": "2025-03-15",
      "headline": "Week in Review: SXSW week comes to a close | TechCrunch",
      "sentiment": "Positive",
      "sentiment_confidence": "High",
      "sentiment_score": 0.73,
      "source": "TechCrunch",
      "summary": "Welcome back to Week in Review! I'm Karyne Levy, TechCrunch's deputy managing editor, and I'll be writing this newsletter from here on out. Thrilled to be",
      "url": "https://techcrunch.com/2025/03/15/week-in-review-sxsw-week-comes-to-a-close/"
    },
    {
      "date": "2025-03-15",
      "headline": "I love consoles more than anything but Microsoft has me less excited than ever about the Xbox Series X successor",
      "sentiment": "Positive",
      "sentiment_confidence": "High",
      "sentiment_score": 0.76,
      "source": "GamesRadar+",
      "summary": "With there no end in sight to Microsoft games making their way to the PS5 and other consoles, I'm less excited than ever for the Xbox Series X follow-up.",
      "url": "https://www.gamesradar.com/hardware/i-love-consoles-more-than-anything-but-microsoft-has-me-less-excited-than-ever-about-the-xbox-series-x-successor/"
    },
    {
      "date": "2025-03-15",
      "headline": "Huawei's Microsoft Windows license for PCs expires this month, company launching PCs with Harmony OS: Report",
      "sentiment": "Neutral",
      "sentiment_confidence": "Low",
      "sentiment_score": 0.13,
      "source": "Tom's Hardware UK",
      "summary": "Huawei's licenses to install Windows expired this month, so the company will no longer be able to produce and sell PCs with Windows.",
      "url": "https://www.tomshardware.com/tech-industry/huaweis-microsoft-windows-license-for-pcs-expires-this-month-company-launching-pcs-with-harmony-os-report"
    },
    {
      "date": "2025-03-15",
      "headline": "Best vs. First",
      "sentiment": "Positive",
      "sentiment_confidence": "High",
      "sentiment_score": 0.89,
      "source": "CNBC",
      "summary": "The chief executive says there's something more important than being first: being best.",
      "url": "https://www.cnbc.com/2016/10/07/the-one-great-reason-apple-ceo-tim-cook-doesnt-care-about-being-first.html"
    }
  ],
  "social_media_sentiment": {
    "reddit": "Negative",
    "twitter": "Neutral"
  },
  "timestamp": "Sun, 16 Mar 2025 22:47:23 GMT"
}
```