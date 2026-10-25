
import os
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("TWELVE_DATA_API_KEY")
SYMBOLS = ["AAPL", "MSFT", "NVDA", "GOOGL"]

if not API_KEY:
    raise SystemExit("Missing TWELVE_DATA_API_KEY")

results = []

for symbol in SYMBOLS:
    params = urllib.parse.urlencode({
        "symbol": symbol,
        "apikey": API_KEY
    })

    request = urllib.request.Request(
        "https://api.twelvedata.com/quote?" + params,
        headers={"User-Agent": "StockVisionAI/1.0"}
    )

    try:
        with urllib.request.urlopen(
            request, timeout=20
        ) as response:
            data = json.load(response)

        if data.get("status") == "error":
            print(symbol, "ERROR:", data.get("message"))
            continue

        if not data.get("close"):
            print(symbol, "No price returned")
            continue

        results.append({
            "symbol": data.get("symbol", symbol),
            "name": data.get("name"),
            "price": data.get("close"),
            "change": data.get("change"),
            "percent_change": data.get("percent_change"),
            "currency": data.get("currency"),
            "market_time": data.get("datetime")
        })

        print(symbol, "SUCCESS")

    except Exception as error:
        print(symbol, "Request failed:", type(error).__name__)

print("Successful quotes:", len(results))
print("Checked at:", datetime.now(timezone.utc).isoformat())
print("Data retained only within this workflow run")
