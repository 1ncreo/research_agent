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
- **AI/NLP Processing**: TextBlob, NLTK, LangChain (free components)
- **Web Scraping**: BeautifulSoup, Requests
- **Data Sources**: Yahoo Finance, Google News, Reddit, and more
- **Storage**: MongoDB (can be configured for local storage)

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
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