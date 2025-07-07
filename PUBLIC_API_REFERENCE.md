# Bybit Public API Endpoints - No Authentication Required

## 🔓 **Overview**
These endpoints work **WITHOUT** API key or secret. Perfect for:
- Market data analysis
- Price monitoring
- Trading bots (read-only data)
- Portfolio tracking
- Research and development

## 📊 **Complete List of Public Endpoints**

### 🕐 **Server & System Information**
```python
# Get server time
session.get_server_time()
# Direct HTTP: GET /v5/market/time

# Get system announcements
session.get_announcements(locale="en-US")
# Direct HTTP: GET /v5/announcements/index
```

### 📈 **Market Data - Basic**
```python
# Get trading instruments (all trading pairs)
session.get_instruments_info(category="spot")           # Spot pairs
session.get_instruments_info(category="linear")         # Linear futures
session.get_instruments_info(category="inverse")        # Inverse futures
session.get_instruments_info(category="option")         # Options
# Direct HTTP: GET /v5/market/instruments-info

# Get orderbook (bid/ask prices)
session.get_orderbook(category="spot", symbol="BTCUSDT")
# Direct HTTP: GET /v5/market/orderbook

# Get 24hr ticker statistics
session.get_tickers(category="spot", symbol="BTCUSDT")   # Single symbol
session.get_tickers(category="spot")                     # All symbols
# Direct HTTP: GET /v5/market/tickers

# Get recent public trades
session.get_public_trade_history(category="spot", symbol="BTCUSDT", limit=50)
# Direct HTTP: GET /v5/market/trading-records
```

### 📊 **Market Data - Klines/Candlesticks**
```python
# Regular klines (OHLCV data)
session.get_kline(category="spot", symbol="BTCUSDT", interval="60", limit=100)
# Direct HTTP: GET /v5/market/kline

# Mark price klines (futures only)
session.get_mark_price_kline(category="linear", symbol="BTCUSDT", interval="60", limit=100)
# Direct HTTP: GET /v5/market/mark-price-kline

# Index price klines (futures only)
session.get_index_price_kline(category="linear", symbol="BTCUSDT", interval="60", limit=100)
# Direct HTTP: GET /v5/market/index-price-kline

# Premium index klines (futures only)
session.get_premium_index_price_kline(category="linear", symbol="BTCUSDT", interval="60", limit=100)
# Direct HTTP: GET /v5/market/premium-index-price-kline
```

### 🎯 **Futures-Specific Data**
```python
# Funding rate history
session.get_funding_rate_history(category="linear", symbol="BTCUSDT", limit=50)
# Direct HTTP: GET /v5/market/funding/history

# Open interest data
session.get_open_interest(category="linear", symbol="BTCUSDT", intervalTime="5min", limit=50)
# Direct HTTP: GET /v5/market/open-interest

# Long/short ratio
session.get_long_short_ratio(category="linear", symbol="BTCUSDT", period="5min", limit=50)
# Direct HTTP: GET /v5/market/account-ratio

# Risk limit information
session.get_risk_limit(category="linear", symbol="BTCUSDT")
# Direct HTTP: GET /v5/market/risk-limit
```

### 📈 **Options-Specific Data**
```python
# Historical volatility
session.get_historical_volatility(category="option", baseCoin="BTC")
# Direct HTTP: GET /v5/market/historical-volatility

# Delivery price history
session.get_delivery_price(category="option", symbol="BTC", limit=50)
# Direct HTTP: GET /v5/market/delivery-price
```

### 🛡️ **Risk & Insurance Data**
```python
# Insurance fund data
session.get_insurance(coin="BTC")
# Direct HTTP: GET /v5/market/insurance
```

## 🔧 **Usage Examples**

### **Basic Setup (No API Key Needed)**
```python
from pybit.unified_trading import HTTP

# Create public session (no authentication)
session = HTTP(testnet=False)  # Use testnet=True for test data

# Get current BTC price
result = session.get_tickers(category="spot", symbol="BTCUSDT")
price = result['result']['list'][0]['lastPrice']
print(f"BTC Price: ${price}")
```

### **Direct HTTP Requests**
```python
import requests

base_url = "https://api.bybit.com"  # or https://api-testnet.bybit.com

# Get server time
response = requests.get(f"{base_url}/v5/market/time")
data = response.json()
print(data)

# Get BTC price
params = {"category": "spot", "symbol": "BTCUSDT"}
response = requests.get(f"{base_url}/v5/market/tickers", params=params)
data = response.json()
print(data)
```

### **Real-Time Market Monitoring**
```python
import time
from pybit.unified_trading import HTTP

session = HTTP(testnet=False)

def monitor_btc_price():
    while True:
        try:
            # Get current price
            result = session.get_tickers(category="spot", symbol="BTCUSDT")
            price = float(result['result']['list'][0]['lastPrice'])
            change_24h = float(result['result']['list'][0]['price24hPcnt'])
            
            print(f"BTC: ${price:,.2f} ({change_24h:+.2%})")
            
            # Get recent trades
            trades = session.get_public_trade_history(category="spot", symbol="BTCUSDT", limit=1)
            last_trade = trades['result']['list'][0]
            print(f"Last trade: {last_trade['side']} {last_trade['size']} BTC at ${last_trade['price']}")
            
            time.sleep(10)  # Update every 10 seconds
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

# Run monitoring
monitor_btc_price()
```

## 📊 **Available Intervals for Klines**
- `"1"` - 1 minute
- `"3"` - 3 minutes  
- `"5"` - 5 minutes
- `"15"` - 15 minutes
- `"30"` - 30 minutes
- `"60"` - 1 hour
- `"120"` - 2 hours
- `"240"` - 4 hours
- `"360"` - 6 hours
- `"720"` - 12 hours
- `"D"` - 1 day
- `"W"` - 1 week
- `"M"` - 1 month

## 🎯 **Trading Categories**
- `"spot"` - Spot trading (BTCUSDT, ETHUSDT, etc.)
- `"linear"` - Linear futures (USDT-margined)
- `"inverse"` - Inverse futures (coin-margined)
- `"option"` - Options contracts

## 📈 **Real Data Examples**

### **Current BTC Price (Live)**
```json
{
  "symbol": "BTCUSDT",
  "lastPrice": "108261.4",
  "bid1Price": "108261.4",
  "ask1Price": "108261.5",
  "price24hPcnt": "-0.0065",
  "highPrice24h": "109705",
  "lowPrice24h": "107961.8",
  "volume24h": "5644.530757"
}
```

### **Orderbook Data**
```json
{
  "s": "BTCUSDT",
  "a": [["108294.6", "0.940267"]],  // Ask (sell orders)
  "b": [["108294.5", "1.419576"]],  // Bid (buy orders)
  "ts": 1751900476488
}
```

### **Recent Trades**
```json
{
  "execId": "2290000000850766260",
  "symbol": "BTCUSDT",
  "price": "108306",
  "size": "0.000103",
  "side": "Buy",
  "time": "1751900442170"
}
```

## 🚀 **Use Cases**

### **1. Price Alerts Bot**
```python
def check_price_alerts():
    result = session.get_tickers(category="spot", symbol="BTCUSDT")
    price = float(result['result']['list'][0]['lastPrice'])
    
    if price > 110000:
        send_alert(f"BTC above $110k: ${price}")
    elif price < 100000:
        send_alert(f"BTC below $100k: ${price}")
```

### **2. Market Analysis**
```python
def analyze_market():
    # Get klines for technical analysis
    klines = session.get_kline(category="spot", symbol="BTCUSDT", interval="60", limit=100)
    
    # Get funding rates for sentiment
    funding = session.get_funding_rate_history(category="linear", symbol="BTCUSDT", limit=10)
    
    # Get long/short ratio
    ratio = session.get_long_short_ratio(category="linear", symbol="BTCUSDT", period="5min", limit=10)
    
    # Analyze data...
```

### **3. Portfolio Tracker**
```python
def track_portfolio():
    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
    
    for symbol in symbols:
        result = session.get_tickers(category="spot", symbol=symbol)
        price = result['result']['list'][0]['lastPrice']
        change = result['result']['list'][0]['price24hPcnt']
        print(f"{symbol}: ${price} ({change}%)")
```

## ⚡ **Rate Limits**
- Public endpoints have higher rate limits than private endpoints
- Generally 120 requests per minute for most endpoints
- Some endpoints may have different limits
- No authentication required = higher limits

## 🔗 **Base URLs**
- **Mainnet**: `https://api.bybit.com`
- **Testnet**: `https://api-testnet.bybit.com`

## 💡 **Pro Tips**
1. **Use public endpoints for market data** - No API key needed
2. **Cache data when possible** - Reduce API calls
3. **Handle errors gracefully** - Network issues can occur
4. **Respect rate limits** - Don't spam requests
5. **Use WebSocket for real-time data** - More efficient for live updates

## 🎯 **Bottom Line**
You have access to **comprehensive market data** without any API key:
- ✅ Real-time prices and orderbook
- ✅ Historical klines/candlesticks  
- ✅ Trading volume and statistics
- ✅ Futures funding rates and open interest
- ✅ All trading pairs and instruments
- ✅ Perfect for analysis, monitoring, and research

**No authentication barriers - just pure market data access!**