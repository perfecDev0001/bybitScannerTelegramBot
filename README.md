# Bybit Perpetual Futures Scanner & Telegram Bot

A comprehensive trading scanner that monitors Bybit perpetual futures for volume spikes, price pumps/dumps, breakouts, and liquidity changes, sending real-time alerts via Telegram.

## 🚀 Features

- **Real-time Scanning**: Monitors all Bybit perpetual futures every minute
- **Multiple Alert Types**:
  - 📈 Volume spikes (configurable threshold)
  - 🚀 Price pumps and dumps (5min/15min timeframes)
  - ⚡ Volatility spikes
  - 📊 Breakout detection (support/resistance levels)
  - 💧 Liquidity drops
- **Smart Filtering**: Volume, price, and market cap filters
- **Telegram Integration**: Real-time alerts with formatted messages
- **Web Dashboard**: Health checks and status monitoring
- **Render Ready**: Configured for easy cloud deployment

## 📋 Requirements

- Python 3.12+
- Bybit account (uses public API - no authentication needed for market data)
- Telegram Bot Token
- Telegram Chat ID

## 🛠️ Installation & Setup

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd bybitScannerTelegramBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Update the `.env` file with your settings:

```env
# Telegram Configuration (REQUIRED)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Scanner Configuration
SCAN_INTERVAL_SECONDS=60

# Alert Thresholds (adjust as needed)
VOLUME_SPIKE_THRESHOLD=2.0      # 200% volume increase
PRICE_PUMP_THRESHOLD=5.0        # 5% price change
PRICE_DUMP_THRESHOLD=-5.0       # -5% price change
VOLATILITY_THRESHOLD=10.0       # 10% volatility
LIQUIDITY_DROP_THRESHOLD=50.0   # 50% liquidity drop

# Filters
MIN_VOLUME_24H=1000000          # $1M minimum 24h volume
MIN_PRICE=0.001                 # Minimum price filter
MAX_PRICE=100000                # Maximum price filter
```

### 3. Get Your Telegram Chat ID

1. Create a bot with [@BotFather](https://t.me/botfather)
2. Get your chat ID:
   - Send a message to [@userinfobot](https://t.me/userinfobot)
   - Or send a message to your bot and visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

### 4. Test the Setup

```bash
# Run the test suite
python test_scanner.py
```

This will test:
- ✅ Bybit API connectivity
- ✅ Telegram bot functionality
- ✅ Scanning logic
- ✅ Configuration validation

## 🚀 Running Locally

### Option 1: Direct Scanner (Console Output)
```bash
python scanner.py
```

### Option 2: Web Server + Scanner (Recommended)
```bash
python app.py
```

Then visit:
- `http://localhost:8080/` - Main status
- `http://localhost:8080/health` - Health check
- `http://localhost:8080/status` - Detailed status
- `http://localhost:8080/test-telegram` - Test Telegram bot

## 🌐 Deployment to Render

### 1. Prepare for Deployment

All necessary files are included:
- `Procfile` - Render process configuration
- `runtime.txt` - Python version specification
- `requirements.txt` - Dependencies
- `app.py` - Web server with health checks

### 2. Deploy to Render

1. **Create Render Account**: Sign up at [render.com](https://render.com)

2. **Create Web Service**:
   - Connect your GitHub repository
   - Choose "Web Service"
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`

3. **Set Environment Variables** in Render dashboard:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   SCAN_INTERVAL_SECONDS=60
   VOLUME_SPIKE_THRESHOLD=2.0
   PRICE_PUMP_THRESHOLD=5.0
   MIN_VOLUME_24H=1000000
   ```

4. **Deploy**: Render will automatically build and deploy

### 3. Monitor Deployment

- Health Check: `https://your-app.onrender.com/health`
- Status: `https://your-app.onrender.com/status`
- Test Telegram: `https://your-app.onrender.com/test-telegram`

## 📊 Alert Types & Examples

### Volume Spike Alert
```
🚨 VOLUME SPIKE ALERT 🚨

📊 Symbol: BTCUSDT
📈 Volume Change: +250.5%
💰 Current Volume: $2,500,000
📊 Previous Volume: $1,000,000

⏰ Time: 2024-01-15 14:30:25 UTC
```

### Price Pump Alert
```
🚀 PUMP ALERT 🚀

💰 Symbol: ETHUSDT
💵 Price Change (5min): +7.25%
📈 Current Price: $2,150.50
📊 Previous Price: $2,005.25

⏰ Time: 2024-01-15 14:30:25 UTC
```

### Breakout Alert
```
⬆️ BREAKOUT ALERT ⬆️

💰 Symbol: ADAUSDT
📊 Direction: UP
💵 Current Price: $0.485000
🎯 Breakout Level: $0.480000
💪 Strength: 1.04%

⏰ Time: 2024-01-15 14:30:25 UTC
```

## ⚙️ Configuration Options

### Alert Thresholds
- `VOLUME_SPIKE_THRESHOLD`: Multiplier for volume spike detection (2.0 = 200% increase)
- `PRICE_PUMP_THRESHOLD`: Percentage for pump detection (5.0 = 5% increase)
- `PRICE_DUMP_THRESHOLD`: Percentage for dump detection (-5.0 = 5% decrease)
- `VOLATILITY_THRESHOLD`: Percentage for volatility spike (10.0 = 10% volatility)
- `LIQUIDITY_DROP_THRESHOLD`: Percentage for liquidity drop (50.0 = 50% decrease)

### Filters
- `MIN_VOLUME_24H`: Minimum 24h volume in USD (1000000 = $1M)
- `MIN_PRICE`: Minimum price filter (0.001 = $0.001)
- `MAX_PRICE`: Maximum price filter (100000 = $100,000)

### Technical Analysis
- `BREAKOUT_LOOKBACK_PERIODS`: Periods for support/resistance calculation (20)
- `RSI_PERIOD`: RSI calculation period (14)

## 🔧 API Endpoints

### Health & Status
- `GET /` - Basic service information
- `GET /health` - Health check (for monitoring)
- `GET /status` - Detailed status information

### Testing & Control
- `GET /test-telegram` - Test Telegram bot connectivity
- `GET /restart-scanner` - Restart the scanner (debugging)

## 📝 Logs & Monitoring

### Log Levels
Set `LOG_LEVEL` in `.env`:
- `DEBUG` - Detailed debugging information
- `INFO` - General information (default)
- `WARNING` - Warning messages only
- `ERROR` - Error messages only

### Monitoring
- Scanner status via web endpoints
- Telegram startup/error notifications
- Automatic error recovery
- Uptime and alert statistics

## 🛡️ Security & Best Practices

### API Security
- Uses Bybit public endpoints (no private keys needed)
- Rate limiting implemented
- Error handling and recovery

### Telegram Security
- Bot token stored in environment variables
- Chat ID validation
- Message rate limiting

### Production Considerations
- Automatic restarts on errors
- Health check endpoints for monitoring
- Configurable alert thresholds
- Resource usage optimization

## 🐛 Troubleshooting

### Common Issues

1. **No Telegram Messages**
   - Check `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
   - Test with `/test-telegram` endpoint
   - Verify bot permissions

2. **No Alerts Generated**
   - Lower `MIN_VOLUME_24H` threshold
   - Adjust alert thresholds
   - Check scanner logs

3. **API Errors**
   - Check internet connectivity
   - Verify Bybit API status
   - Review rate limiting settings

4. **Deployment Issues**
   - Check Render logs
   - Verify environment variables
   - Test health endpoints

### Debug Mode
Set `DEBUG=True` in `.env` for detailed logging.

## 📈 Performance

### Resource Usage
- Memory: ~100-200MB
- CPU: Low (mostly I/O bound)
- Network: ~1-2 requests per second

### Scalability
- Handles 1000+ symbols efficiently
- Rate limiting prevents API overload
- Configurable scan intervals

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This software is for educational and informational purposes only. Trading cryptocurrencies involves substantial risk of loss. The authors are not responsible for any financial losses incurred through the use of this software.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Test with the provided test script
4. Create an issue with detailed information

---

**Happy Trading! 🚀📈**