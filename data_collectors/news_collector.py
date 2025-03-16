# data_collectors/news_collector.py
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
from config import NEWS_API_KEY, HEADERS
import time
import random

class NewsCollector:
    def __init__(self):
        self.news_api_key = NEWS_API_KEY
        self.headers = HEADERS if HEADERS else {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml",
            "Referer": "https://www.google.com/"
        }
    
    def get_recent_news(self, company_name, max_articles=5):

        news_articles = []

        if self.news_api_key:
            newsapi_articles = self._get_from_newsapi(company_name, max_articles)
            if newsapi_articles:
                news_articles.extend(newsapi_articles)

        if len(news_articles) < max_articles:
            yahoo_articles = self._scrape_yahoo_finance_news(company_name, max_articles - len(news_articles))
            if yahoo_articles:
                news_articles.extend(yahoo_articles)

        if len(news_articles) < max_articles:
            marketwatch_articles = self._scrape_marketwatch_news(company_name, max_articles - len(news_articles))
            if marketwatch_articles:
                news_articles.extend(marketwatch_articles)
        
        if len(news_articles) == 0:
            print(f"No news found for {company_name}")
        else:
            print(f"Found {len(news_articles)} news articles for {company_name}")
            
        return news_articles[:max_articles]
    
    def _get_from_newsapi(self, company_name, max_articles=5):

        try:

            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            url = f"https://newsapi.org/v2/everything?q={company_name} OR {company_name.lower()}&language=en&from={start_date_str}&to={end_date_str}&sortBy=publishedAt&apiKey={self.news_api_key}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                if 'articles' in data and data['articles']:
                    for article in data['articles'][:max_articles]:
                        articles.append({
                            "headline": article.get('title'),
                            "source": article.get('source', {}).get('name'),
                            "date": article.get('publishedAt', '')[:10],  # Format YYYY-MM-DD
                            "url": article.get('url'),
                            "summary": article.get('description', ''),
                            "sentiment": None  # Will be filled by sentiment analyzer
                        })
                
                return articles
            
            print(f"NewsAPI response: {response.status_code}, {response.text[:100]}...")
            return []
        except Exception as e:
            print(f"Error fetching from NewsAPI: {e}")
            return []
    
    def _scrape_yahoo_finance_news(self, company_name, max_articles=5):
        try:
            
            ticker = company_name
            
            url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
            
            time.sleep(1)  
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = []
                
                # Find news section
                news_section = soup.find('div', {'id': 'quoteNewsStream-0-Stream'})
                if news_section:
                    article_elements = news_section.find_all('li', {'class': 'js-stream-content'})
                    
                    for article in article_elements[:max_articles]:
                        try:
                            title_element = article.find('h3')
                            headline = title_element.text.strip() if title_element else "No title"

                            link_element = article.find('a')
                            relative_url = link_element.get('href') if link_element else None
                            url = f"https://finance.yahoo.com{relative_url}" if relative_url else None

                            footer = article.find('div', {'class': 'C(#959595)'})
                            source = "Yahoo Finance"
                            date = datetime.now().strftime('%Y-%m-%d')
                            
                            if footer and '·' in footer.text:
                                parts = footer.text.split('·')
                                source = parts[0].strip()
                                
                            articles.append({
                                "headline": headline,
                                "source": source,
                                "date": date,
                                "url": url,
                                "sentiment": None
                            })
                        except Exception as e:
                            print(f"Error extracting Yahoo article: {e}")
                            continue
                
                return articles
            
            print(f"Yahoo Finance response status code: {response.status_code}")
            return []
        except Exception as e:
            print(f"Error scraping Yahoo Finance News: {e}")
            return []
    
    def _scrape_marketwatch_news(self, company_name, max_articles=5):

        try:
            url = f"https://www.marketwatch.com/search?q={company_name}&m=Keyword&rpp=15&mp=0&bd=false&rs=true"
            
            time.sleep(1)  # Prevent rate limiting
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = []
                
                # Find article elements in MarketWatch
                article_elements = soup.select('.card__headline a')
                
                for i, article in enumerate(article_elements[:max_articles]):
                    try:
                        # Extract title and URL
                        headline = article.text.strip()
                        url = article.get('href')
            
                        date = datetime.now().strftime('%Y-%m-%d')
                        
                        articles.append({
                            "headline": headline,
                            "source": "MarketWatch",
                            "date": date,
                            "url": url,
                            "sentiment": None
                        })
                    except Exception as article_error:
                        print(f"Error parsing MarketWatch article: {article_error}")
                        continue
                
                return articles
            
            print(f"MarketWatch response status code: {response.status_code}")
            return []
        except Exception as e:
            print(f"Error scraping MarketWatch News: {e}")
            return []