from fastapi import FastAPI
from textblob import TextBlob
import random
import time
import requests # We use this to talk to Discord

# --- CONFIGURATION ---
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1454992677685690580/VK-tX9Q5DYm0k3wYuHXs0cqGYjt0udD8qslXveprmvoQuHPhikOVM-yZ3UUg8aMe_4PK"

# --- THE NOTIFICATION SYSTEM ---
def send_alert(msg):
    try:
        data = {"content": f"💸 **SYSTEM ALERT:** {msg}"}
        requests.post(DISCORD_WEBHOOK, json=data)
    except:
        pass # If discord fails, don't stop the money engine

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

# --- THE WEB SERVER ---
app = FastAPI()
engine = SentimentEngine()

@app.get("/")
def home():
    return {"status": "Online"}

@app.get("/predict")
def predict_all():
    # Trigger the alert
    send_alert("API Accessed! Full Market Scan requested.") 
    return {"data": engine.run()}

@app.get("/predict/{ticker}")
def predict_specific(ticker: str):
    # Trigger the alert
    send_alert(f"API Accessed! Ticker requested: {ticker.upper()}")
    return {"data": engine.run(ticker.upper())}