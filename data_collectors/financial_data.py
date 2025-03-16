# data_collectors/financial_data.py
import yfinance as yf
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
from config import ALPHA_VANTAGE_API_KEY
import requests
import re
import time

class FinancialDataCollector:
    def __init__(self):
        self.alpha_vantage_key = ALPHA_VANTAGE_API_KEY
    
    def get_financial_data(self, company_name):
        result = {
            "market_cap": None,
            "stock_price": None,
            "annual_revenue": None,
            "funding_rounds": None
        }
        
        ticker_symbol = self._get_ticker_symbol(company_name)
        
        if ticker_symbol:
            yahoo_data = self._get_yahoo_finance_data(ticker_symbol)
            if yahoo_data:
                result.update(yahoo_data)
            
            if self.alpha_vantage_key:
                alpha_data = self._get_alpha_vantage_data(ticker_symbol)
                if alpha_data:
                    for key, value in alpha_data.items():
                        if result[key] is None and value is not None:
                            result[key] = value
        
        return result
    
    def _get_ticker_symbol(self, company_name):
        try:
            company_name = company_name.strip().lower()
            
            ticker = yf.Ticker(company_name)
            info = ticker.info
            
            if info and 'symbol' in info:
                return info['symbol']
            
            search_url = f"https://finance.yahoo.com/lookup?s={company_name.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(search_url, headers=headers)
            
            if response.status_code == 200:
                matches = re.findall(r'data-symbol="([^"]+)"', response.text)
                if matches:
                    return matches[0]
            
            manual_mapping = {
                "microsoft": "MSFT",
                "apple": "AAPL",
                "google": "GOOGL",
                "amazon": "AMZN",
                "tesla": "TSLA",
                "facebook": "META",
                "nvidia": "NVDA",
                "netflix": "NFLX",
                "alphabet": "GOOGL",
                "meta": "META",
                "intel": "INTC",
                "ibm": "IBM",
                "oracle": "ORCL",
                "adobe": "ADBE",
                "salesforce": "CRM",
                "walmart": "WMT",
                "disney": "DIS",
                "coca cola": "KO",
                "pepsico": "PEP",
                "mcdonalds": "MCD",
                "starbucks": "SBUX",
                "nike": "NKE",
                "ford": "F",
                "general motors": "GM",
                "boeing": "BA",
                "lockheed martin": "LMT",
                "exxon mobil": "XOM",
                "chevron": "CVX",
                "bp": "BP",
                "shell": "SHEL",
                "walt disney": "DIS",
                "berkshire hathaway": "BRK-B",
                "visa": "V",
                "mastercard": "MA",
                "paypal": "PYPL",
                "square": "SQ",
                "spotify": "SPOT",
                "snap": "SNAP",
                "twitter": "TWTR",
                "uber": "UBER",
                "lyft": "LYFT",
                "airbnb": "ABNB",
                "zoom": "ZM",
                "peloton": "PTON",
                "moderna": "MRNA",
                "pfizer": "PFE",
                "johnson & johnson": "JNJ",
                "merck": "MRK",
                "novartis": "NVS",
                "roche": "RHHBY",
                "astrazeneca": "AZN",
                "biontech": "BNTX",
                "gamestop": "GME",
                "amc entertainment": "AMC",
                "blackberry": "BB",
                "nokia": "NOK",
                "amd": "AMD",
                "qualcomm": "QCOM",
                "broadcom": "AVGO",
                "texas instruments": "TXN",
                "micrsoft": "MSFT",
                "googl": "GOOGL",
                "alphabet inc": "GOOGL",
                "alphabet inc.": "GOOGL",
                "alphabet class a": "GOOGL",
                "alphabet class c": "GOOG",
                "meta platforms": "META",
                "meta platforms inc": "META",
                "meta platforms inc.": "META",
                "meta platforms class a": "META",
            }
            
            if company_name in manual_mapping:
                return manual_mapping[company_name]
            
            return None
        except Exception as e:
            print(f"Error getting ticker symbol: {e}")
            return None
    
    def _get_yahoo_finance_data(self, ticker_symbol):
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            
            result = {}
            
            if 'marketCap' in info and info['marketCap']:
                market_cap = info['marketCap']
                if market_cap >= 1_000_000_000:
                    result['market_cap'] = f"${market_cap / 1_000_000_000:.2f} billion"
                elif market_cap >= 1_000_000:
                    result['market_cap'] = f"${market_cap / 1_000_000:.2f} million"
                else:
                    result['market_cap'] = f"${market_cap:,}"
            
            if 'currentPrice' in info and info['currentPrice']:
                result['stock_price'] = f"${info['currentPrice']:.2f}"
            
            if 'totalRevenue' in info and info['totalRevenue']:
                revenue = info['totalRevenue']
                if revenue >= 1_000_000_000:
                    result['annual_revenue'] = f"${revenue / 1_000_000_000:.2f} billion"
                elif revenue >= 1_000_000:
                    result['annual_revenue'] = f"${revenue / 1_000_000:.2f} million"
                else:
                    result['annual_revenue'] = f"${revenue:,}"
            
            return result
        except Exception as e:
            print(f"Error fetching from Yahoo Finance: {e}")
            return None
    
    def _get_alpha_vantage_data(self, ticker_symbol):
        try:
            fd = FundamentalData(key=self.alpha_vantage_key)
            ts = TimeSeries(key=self.alpha_vantage_key)
            
            result = {}
            
            overview_data, _ = fd.get_company_overview(ticker_symbol)
            
            if 'MarketCapitalization' in overview_data and overview_data['MarketCapitalization']:
                market_cap = int(overview_data['MarketCapitalization'])
                if market_cap >= 1_000_000_000:
                    result['market_cap'] = f"${market_cap / 1_000_000_000:.2f} billion"
                elif market_cap >= 1_000_000:
                    result['market_cap'] = f"${market_cap / 1_000_000:.2f} million"
                else:
                    result['market_cap'] = f"${market_cap:,}"
            
            try:
                price_data, _ = ts.get_quote_endpoint(ticker_symbol)
                if '05. price' in price_data and price_data['05. price']:
                    result['stock_price'] = f"${float(price_data['05. price']):.2f}"
            except Exception as e:
                print(f"Error fetching stock price from Alpha Vantage: {e}")
            
            return result
        except Exception as e:
            print(f"Error fetching from Alpha Vantage: {e}")
            return None