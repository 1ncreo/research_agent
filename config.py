# config.py
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CRUNCHBASE_API_KEY=os.getenv("CRUNCHBASE_API_KEY", "")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")

MONGO_URI = os.getenv("MONGO_URI", "")
MONGO_DB = os.getenv("MONGO_DB", "")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

COMPANY_INFO_SOURCES = ["wikipedia", "crunchbase", "opencorporates"]
FINANCIAL_SOURCES = ["yahoo_finance", "alpha_vantage"]
NEWS_SOURCES = ["newsapi", "yahoo_news"]
SOCIAL_MEDIA_SOURCES = ["twitter", "reddit"]