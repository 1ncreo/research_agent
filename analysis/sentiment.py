from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
    
    def analyze_news_sentiment(self, news_articles):
        for article in news_articles:
            if article.get('headline'):
                sentiment_score = self.vader.polarity_scores(article['headline'])
                compound_score = sentiment_score['compound']
                if compound_score >= 0.05:
                    article['sentiment'] = "Positive"
                elif compound_score <= -0.05:
                    article['sentiment'] = "Negative"
                else:
                    article['sentiment'] = "Neutral"
        
        return news_articles
    
    def analyze_text_sentiment(self, text):
        if not text:
            return "Neutral"
        
        sentiment_score = self.vader.polarity_scores(text)
        compound_score = sentiment_score['compound']
        if compound_score >= 0.05:
            return "Positive"
        elif compound_score <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    
    def get_overall_sentiment(self, news_articles):
        if not news_articles:
            return "Neutral"
        
        positive_count = sum(1 for article in news_articles if article.get('sentiment') == "Positive")
        negative_count = sum(1 for article in news_articles if article.get('sentiment') == "Negative")
        neutral_count = sum(1 for article in news_articles if article.get('sentiment') == "Neutral")
        
        if positive_count > negative_count and positive_count > neutral_count:
            return "Positive"
        elif negative_count > positive_count and negative_count > neutral_count:
            return "Negative"
        else:
            return "Neutral"