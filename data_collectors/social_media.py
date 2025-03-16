# data_collectors/social_media.py
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from config import HEADERS
import time
import json
from config import HEADERS, TWITTER_API_KEY, TWITTER_API_SECRET

class SocialMediaCollector:
    def __init__(self):
        self.headers = HEADERS
        self.twitter_api_key = TWITTER_API_KEY
        self.twitter_api_secret = TWITTER_API_SECRET
        self.twitter_bearer_token = self._get_twitter_bearer_token()
    
    def get_social_media_sentiment(self, company_name):
        result = {
            "twitter": None,
            "reddit": None,
        }
        
        twitter_sentiment = self._get_twitter_sentiment(company_name)
        if twitter_sentiment:
            result["twitter"] = twitter_sentiment
        
        reddit_sentiment = self._get_reddit_sentiment(company_name)
        if reddit_sentiment:
            result["reddit"] = reddit_sentiment
            
        return result
    
    def _get_twitter_bearer_token(self):
        if not self.twitter_api_key or not self.twitter_api_secret:
            return None
            
        try:
            auth_url = "https://api.twitter.com/oauth2/token"
            auth_headers = {
                "Authorization": f"Basic {self._get_base64_encoded_credentials()}",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            }
            auth_data = {
                "grant_type": "client_credentials"
            }
            
            response = requests.post(auth_url, headers=auth_headers, data=auth_data)
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                print(f"Failed to get Twitter bearer token: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting Twitter bearer token: {e}")
            return None
    
    def _get_base64_encoded_credentials(self):
        import base64
        credentials = f"{self.twitter_api_key}:{self.twitter_api_secret}"
        return base64.b64encode(credentials.encode()).decode()
    
    def _get_twitter_sentiment(self, company_name):
        try:
            if (self.twitter_bearer_token):
                return self._get_twitter_api_sentiment(company_name)
            else:
                return self._get_twitter_scrape_sentiment(company_name)
        except Exception as e:
            print(f"Error fetching Twitter sentiment: {e}")
            return None
    
    def _get_twitter_api_sentiment(self, company_name):
        try:
            search_url = "https://api.twitter.com/2/tweets/search/recent"
            search_headers = {
                "Authorization": f"Bearer {self.twitter_bearer_token}"
            }
            search_params = {
                "query": f"{company_name} -is:retweet -is:reply",
                "max_results": 100,
                "tweet.fields": "public_metrics,created_at"
            }
            
            response = requests.get(search_url, headers=search_headers, params=search_params)
            
            if response.status_code == 200:
                data = response.json()
                tweets = data.get("data", [])
                
                if not tweets:
                    return "Neutral"
                
                positive_words = ['good', 'great', 'excellent', 'amazing', 'positive', 'bull', 'bullish', 'up', 'higher', 'rise', 'profit']
                negative_words = ['bad', 'terrible', 'awful', 'negative', 'poor', 'bear', 'bearish', 'down', 'lower', 'fall', 'loss']
                
                positive_count = 0
                negative_count = 0
                
                for tweet in tweets:
                    text = tweet.get("text", "").lower()
                    positive_count += sum(1 for word in positive_words if word in text)
                    negative_count += sum(1 for word in negative_words if word in text)
                
                if positive_count > negative_count * 1.5:
                    return "Positive"
                elif negative_count > positive_count * 1.5:
                    return "Negative"
                else:
                    return "Neutral"
            else:
                print(f"Twitter API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error with Twitter API sentiment: {e}")
            return None
    
    def _get_twitter_scrape_sentiment(self, company_name):
        try:
            url = f"https://nitter.net/search?f=tweets&q={company_name}&since=&until=&near="
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                positive_count = len(re.findall(r'good|great|excellent|amazing|positive|bull|bullish', response.text, re.IGNORECASE))
                negative_count = len(re.findall(r'bad|terrible|awful|negative|poor|bear|bearish', response.text, re.IGNORECASE))
                
                if positive_count > negative_count * 1.5:
                    return "Positive"
                elif negative_count > positive_count * 1.5:
                    return "Negative"
                else:
                    return "Neutral"
            
            return "Neutral"
        except Exception as e:
            print(f"Error with Twitter scrape sentiment: {e}")
            return "Neutral"
    
    def _get_reddit_sentiment(self, company_name):
        try:
            url = f"https://www.reddit.com/search/?q={company_name}&sort=top&t=month"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                positive_count = len(re.findall(r'good|great|excellent|amazing|positive|bull|bullish', response.text, re.IGNORECASE))
                negative_count = len(re.findall(r'bad|terrible|awful|negative|poor|bear|bearish', response.text, re.IGNORECASE))
                
                if positive_count > negative_count * 1.5:
                    return "Positive"
                elif negative_count > positive_count * 1.5:
                    return "Negative"
                else:
                    return "Neutral"
            
            return None
        except Exception as e:
            print(f"Error fetching Reddit sentiment: {e}")
            return None