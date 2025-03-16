import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TrendsAnalyzer:
    def __init__(self):
        pass
    
    def get_growth_trend(self, ticker_symbol, period='1y'):
        try:
            import yfinance as yf
            
            ticker_symbol = ticker_symbol.replace('$', '').strip()
            
            if not ticker_symbol:
                print("Error: Ticker symbol is empty.")
                return None
            
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                print(f"Error: No data found for ticker symbol '{ticker_symbol}'.")
                return None
            
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            
            growth_pct = ((end_price - start_price) / start_price) * 100
            
            high_price = hist['High'].max()
            low_price = hist['Low'].min()
            
            daily_returns = hist['Close'].pct_change().dropna()
            volatility = daily_returns.std() * 100
            
            if growth_pct >= 10:
                trend = "Strong Growth"
            elif growth_pct >= 3:
                trend = "Moderate Growth"
            elif growth_pct >= -3:
                trend = "Stable"
            elif growth_pct >= -10:
                trend = "Moderate Decline"
            else:
                trend = "Strong Decline"
            
            return {
                "ticker": ticker_symbol,
                "start_date": hist.index[0].strftime('%Y-%m-%d'),
                "end_date": hist.index[-1].strftime('%Y-%m-%d'),
                "growth_percentage": round(growth_pct, 2),
                "start_price": round(start_price, 2),
                "end_price": round(end_price, 2),
                "high_price": round(high_price, 2),
                "low_price": round(low_price, 2),
                "volatility": round(volatility, 2),
                "trend": trend
            }
        except Exception as e:
            print(f"Error analyzing growth trend: {e}")
            return None
    
    def forecast_trend(self, ticker_symbol, days_ahead=30):
        try:
            import yfinance as yf
            
            ticker_symbol = ticker_symbol.replace('$', '').strip()
            
            if not ticker_symbol:
                print("Error: Ticker symbol is empty.")
                return None
            
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period='1y')
            
            if hist.empty:
                print(f"Error: No data found for ticker symbol '{ticker_symbol}'.")
                return None
            
            ts_data = hist['Close'].values
            
            window = 30
            if len(ts_data) < window:
                window = len(ts_data) // 2
            
            moving_avg = np.convolve(ts_data, np.ones(window)/window, mode='valid')
            
            last_values = moving_avg[-5:]
            avg_change = np.mean(np.diff(last_values))
            
            forecast = []
            last_value = moving_avg[-1]
            
            for _ in range(days_ahead):
                next_value = last_value + avg_change
                forecast.append(next_value)
                last_value = next_value
            
            return {
                "ticker": ticker_symbol,
                "current_price": round(ts_data[-1], 2),
                "forecast_price": round(forecast[-1], 2),
                "forecast_change_percent": round(((forecast[-1] - ts_data[-1]) / ts_data[-1]) * 100, 2),
                "forecast_period_days": days_ahead,
                "forecast_confidence": "Low"
            }
        except Exception as e:
            print(f"Error forecasting trend: {e}")
            return None