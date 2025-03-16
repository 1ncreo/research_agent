from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self._add_financial_terms()
    
    def _add_financial_terms(self):
        financial_lexicon = {
            "beat expectations": 3.0,
            "exceeded expectations": 3.0,
            "missed expectations": -3.0,
            "fell short": -2.5,
            "earnings beat": 2.5,
            "earnings miss": -2.5,
            "guidance raised": 3.0,
            "guidance lowered": -3.0,
            "downgrade": -2.0,
            "upgrade": 2.0,
            "bullish": 2.0,
            "bearish": -2.0,
            "rally": 2.0,
            "sell-off": -2.0,
            "recession": -2.5,
            "growth": 1.5,
            "profit": 1.5,
            "loss": -1.5,
            "bankruptcy": -4.0,
            "acquisition": 1.5,
            "merger": 1.5,
            "lawsuit": -1.5,
            "investigation": -2.0,
            "fine": -2.0,
            "penalty": -2.0,
            "regulatory approval": 2.0,
            "fda approval": 3.0,
            "clinical trial success": 3.0,
            "clinical trial failure": -3.0,
            "patent": 1.5,
            "innovation": 2.0,
            "layoffs": -2.0,
            "job cuts": -2.0,
            "restructuring": -1.0,
            "debt": -1.0,
            "default": -3.0,
            "dividend increase": 2.0,
            "dividend cut": -2.0,
            "stock buyback": 1.5,
            "overvalued": -1.5,
            "undervalued": 1.5,
        }
        
        self.vader.lexicon.update(financial_lexicon)
    
    def analyze_news_sentiment(self, news_articles):
        for article in news_articles:
            combined_text = ""
            
            if article.get('headline'):
                combined_text += article['headline'] + ". "
            
            if article.get('summary'):
                combined_text += article['summary']
            
            if combined_text:
                sentiment_score = self.vader.polarity_scores(combined_text)
                compound_score = sentiment_score['compound']
                
                if compound_score >= 0.25:
                    sentiment = "Positive"
                    confidence = "High" if compound_score >= 0.5 else "Medium"
                elif compound_score <= -0.25:
                    sentiment = "Negative"
                    confidence = "High" if compound_score <= -0.5 else "Medium"
                else:
                    sentiment = "Neutral"
                    confidence = "Medium" if abs(compound_score) <= 0.1 else "Low"
                
                article['sentiment'] = sentiment
                article['sentiment_score'] = round(compound_score, 2)
                article['sentiment_confidence'] = confidence
            else:
                article['sentiment'] = "Neutral"
                article['sentiment_score'] = 0.0
                article['sentiment_confidence'] = "Low"
        
        return news_articles
    
    def analyze_text_sentiment(self, text):
        if not text:
            return {
                "sentiment": "Neutral", 
                "score": 0.0, 
                "confidence": "Low"
            }
        
        sentiment_score = self.vader.polarity_scores(text)
        compound_score = sentiment_score['compound']
        
        if compound_score >= 0.25:
            sentiment = "Positive"
            confidence = "High" if compound_score >= 0.5 else "Medium"
        elif compound_score <= -0.25:
            sentiment = "Negative"
            confidence = "High" if compound_score <= -0.5 else "Medium"
        else:
            sentiment = "Neutral"
            confidence = "Medium" if abs(compound_score) <= 0.1 else "Low"
        
        return {
            "sentiment": sentiment,
            "score": round(compound_score, 2),
            "confidence": confidence
        }
    
    def get_overall_sentiment(self, news_articles):
        if not news_articles:
            return {
                "sentiment": "Neutral",
                "score": 0.0,
                "confidence": "Low",
                "article_count": 0
            }
        
        # Calculate weighted sentiment based on confidence
        total_score = 0
        weights = {"High": 3, "Medium": 2, "Low": 1}
        total_weight = 0
        
        for article in news_articles:
            if article.get('sentiment_score') is not None:
                confidence = article.get('sentiment_confidence', 'Low')
                weight = weights.get(confidence, 1)
                total_score += article.get('sentiment_score', 0) * weight
                total_weight += weight
        
        avg_score = total_score / total_weight if total_weight > 0 else 0
        
        # Get count of each sentiment type
        positive_count = sum(1 for article in news_articles if article.get('sentiment') == "Positive")
        negative_count = sum(1 for article in news_articles if article.get('sentiment') == "Negative")
        neutral_count = sum(1 for article in news_articles if article.get('sentiment') == "Neutral")
        
        # Determine overall sentiment
        if avg_score >= 0.25:
            sentiment = "Positive"
            confidence = "High" if avg_score >= 0.5 else "Medium"
        elif avg_score <= -0.25:
            sentiment = "Negative"
            confidence = "High" if avg_score <= -0.5 else "Medium"
        else:
            sentiment = "Neutral"
            confidence = "Medium" if abs(avg_score) <= 0.1 else "Low"
        
        return {
            "sentiment": sentiment,
            "score": round(avg_score, 2),
            "confidence": confidence,
            "article_count": len(news_articles),
            "positive_count": positive_count,
            "neutral_count": neutral_count,
            "negative_count": negative_count
        }