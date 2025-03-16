# core.py
from data_collectors.company_info import CompanyInfoCollector
from data_collectors.financial_data import FinancialDataCollector
from data_collectors.news_collector import NewsCollector
from data_collectors.social_media import SocialMediaCollector
from data_collectors.competitor_info import CompetitorInfoCollector
from analysis.sentiment import SentimentAnalyzer
from analysis.trends import TrendsAnalyzer
from storage.database import DatabaseManager
import time

class ResearchEngine:
    def __init__(self):

        self.company_info = CompanyInfoCollector()
        self.financial_data = FinancialDataCollector()
        self.news_collector = NewsCollector()
        self.social_media = SocialMediaCollector()
        self.competitor_info = CompetitorInfoCollector()
        

        self.sentiment_analyzer = SentimentAnalyzer()
        self.trends_analyzer = TrendsAnalyzer()
        

        self.db = DatabaseManager()

    def research_company(self, company_name):

        print(f"Starting research for: {company_name}")

        print("Getting company overview...")
        try:
            overview = self.company_info.get_company_overview(company_name)
            if not overview:
                print(f"No company overview found for {company_name}")
        except Exception as e:
            print(f"Error getting company overview: {e}")
            overview = {}

        print("Getting financial data...")
        try:
            financials = self.financial_data.get_financial_data(company_name)
            if not financials:
                print(f"No financial data found for {company_name}")
        except Exception as e:
            print(f"Error getting financial data: {e}")
            financials = {}

        print("Getting recent news...")
        try:
            news = self.news_collector.get_recent_news(company_name)
            if not news:
                print(f"No news found for {company_name}")
        except Exception as e:
            print(f"Error getting news: {e}")
            news = []

        print("Analyzing news sentiment...")
        try:
            news_with_sentiment = self.sentiment_analyzer.analyze_news_sentiment(news)
        except Exception as e:
            print(f"Error analyzing news sentiment: {e}")
            news_with_sentiment = []
        print("Getting social media sentiment...")
        try:
            social_sentiment = self.social_media.get_social_media_sentiment(company_name)
        except Exception as e:
            print(f"Error getting social media sentiment: {e}")
            social_sentiment = {}

        print("Getting competitor information...")
        try:
            competitors = self.competitor_info.get_competitors(company_name)
        except Exception as e:
            print(f"Error getting competitor information: {e}")
            competitors = []
        

        growth_trends = None
        ticker_symbol = None
        try:
            if overview.get('company_name'):
                ticker_symbol = self.financial_data._get_ticker_symbol(overview['company_name'])
            if ticker_symbol:
                print("Analyzing growth trends...")
                growth_trends = self.trends_analyzer.get_growth_trend(ticker_symbol)
                if growth_trends:
                    print("Forecasting future trends...")
                    forecast = self.trends_analyzer.forecast_trend(ticker_symbol)
                    if forecast:
                        growth_trends['forecast'] = forecast
        except Exception as e:
            print(f"Error analyzing growth trends: {e}")

        research_results = {
            "company_name": company_name,
            "overview": overview,
            "financials": financials,
            "recent_news": news_with_sentiment,
            "social_media_sentiment": social_sentiment,
            "competitors": competitors,
            "growth_trends": growth_trends
        }
        
        self.db.save_research(research_results)
        print(f"Research results saved for {company_name}")
        
        return research_results
