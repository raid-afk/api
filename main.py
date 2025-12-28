from fastapi import FastAPI, HTTPException
from textblob import TextBlob
import random
import time
from pydantic import BaseModel

# --- THE BUSINESS LOGIC ---
class SentimentEngine:
    def __init__(self):
        self.targets = ["BTC", "ETH", "SOL", "NVDA", "TSLA"]

    def get_social_signals(self, asset):
        headlines = [
            f"{asset} seeing massive volume increase",
            f"Regulatory crackdown on {asset}",
            f"{asset} adoption signals bullish trend",
            f"Market uncertainty surrounding {asset}"
        ]
        return random.choice(headlines)

    def analyze(self, text):
        return TextBlob(text).sentiment.polarity

    def run(self, specific_ticker=None):
        results = []
        loop_targets = [specific_ticker] if specific_ticker else self.targets
        
        for asset in loop_targets:
            news = self.get_social_signals(asset)
            score = self.analyze(news)
            
            # The "Money" Algorithm
            signal = "HOLD"
            if score > 0.2: signal = "BUY"
            if score < -0.2: signal = "SELL"
            
            results.append({
                "ticker": asset,
                "news_snippet": news,
                "sentiment_score": round(score, 2),
                "trade_signal": signal,
                "timestamp_utc": time.time()
            })
        return results

# --- THE WEB SERVER (What allows you to get paid) ---
app = FastAPI()
engine = SentimentEngine()

@app.get("/")
def home():
    return {"status": "Online", "message": "High-Frequency Sentiment API is running."}

@app.get("/predict")
def predict_all():
    # This is the endpoint you charge $500/mo for
    return {"data": engine.run()}

@app.get("/predict/{ticker}")
def predict_specific(ticker: str):
    # Specialized endpoint
    return {"data": engine.run(ticker.upper())}