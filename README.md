# Bybit Perpetual Futures Scanner & Telegram Bot

A comprehensive trading scanner that monitors Bybit perpetual futures for volume spikes, price pumps/dumps, breakouts, and liquidity changes, with a full-featured **Telegram UI** for customer interaction and real-time alerts.

## 🚀 Features

### 📊 Core Scanning Features
- **Real-time Scanning**: Monitors all Bybit perpetual futures every minute
- **Multiple Alert Types**:
  - 📈 Volume spikes (configurable threshold)
  - 🚀 Price pumps and dumps (5min/15min timeframes)
  - ⚡ Volatility spikes
  - 📊 Breakout detection (support/resistance levels)
  - 💧 Liquidity drops
- **Smart Filtering**: Volume, price, and market cap filters

### 🤖 Telegram UI Features
- **Interactive Dashboard**: Full control panel accessible via Telegram
- **Real-time Status**: Live scanner status and performance metrics
- **Alert Management**: View recent alerts and configure preferences
- **Symbol Browser**: Browse and search tracked symbols
- **Settings Control**: Adjust thresholds and filters on-the-fly
- **Scanner Controls**: Start, stop, restart scanner remotely
- **Performance Metrics**: Detailed statistics and uptime monitoring
- **Multi-user Support**: Secure access for authorized users

### 🌐 Web Server Features
- **Health Checks**: API endpoints for monitoring
- **Status Dashboard**: Web-based status information
- **API Endpoints**: RESTful API for data access
- **Render Ready**: Configured for easy cloud deployment

# 🚀 GUI Telegram Bot Implementation Summary

## ✅ What We've Accomplished

Your Bybit Scanner Telegram Bot has been **completely transformed into a GUI-based interface**! No more typing commands - everything is now accessible through clickable buttons and interactive menus.

## 🎯 Key Changes Made

### 1. **Main Menu Transformation**
- **Before**: Simple welcome message with basic buttons
- **After**: Comprehensive main menu with 9 major sections:
  - 📊 Scanner Dashboard
  - 📈 Market Overview  
  - 🔥 Top Movers
  - 🚨 Recent Alerts
  - ⭐ My Watchlist
  - ⚙️ Settings
  - 🎮 Controls
  - 📊 Performance
  - 📡 Status
  - ❓ Help & Guide

### 2. **Enhanced Navigation System**
- **🏠 Main Menu** button on every screen
- **🔄 Refresh** buttons for real-time data updates
- **Context-sensitive buttons** for specific actions
- **Breadcrumb navigation** between sections

### 3. **GUI-Enhanced Menus**

#### 📊 Scanner Dashboard
- Enhanced with more navigation options
- Quick access to all major functions
- Real-time status indicators

#### 🚨 Alerts Menu
- Refresh alerts functionality
- Direct access to alert settings
- Test alert capability
- Alert history and statistics options

#### 📡 Status Menu  
- Detailed system health monitoring
- API status checking
- Enhanced refresh capabilities

#### 💰 Symbols Menu
- Browse symbols with enhanced filtering
- Top gainers/losers quick access
- Add to watchlist functionality
- Search capabilities

#### ⚙️ Settings Menu
- Comprehensive configuration options
- Alert thresholds management
- Volume & price filters
- Timing settings
- Notification preferences
- Reset to defaults option

#### 📊 Performance Menu
- Detailed statistics view
- Performance charts access
- Efficiency reporting
- Alert analysis

#### 🎮 Control Panel
- Start/Stop/Pause/Restart scanner
- Test Telegram and API connectivity
- Scanner logs access
- Advanced options

#### ⭐ Watchlist Management
- Add/remove symbols easily
- Watchlist statistics
- Settings and price alerts
- Real-time price tracking

#### ❓ Help System
- Quick start guide
- Feature guides
- Settings help
- Alert guides
- Troubleshooting
- FAQ section

## 🎮 Pure GUI Experience Features

### ✅ No Commands Required
- Only `/start` command needed to begin
- Everything else is button-based
- Intuitive navigation flow

### ✅ Mobile-Optimized
- Large, touch-friendly buttons
- Clear visual hierarchy
- Emoji-enhanced interface
- Minimal scrolling required

### ✅ Real-Time Updates
- Refresh buttons on every screen
- Live data synchronization
- Instant button responses
- Dynamic content updates

### ✅ Context-Aware Navigation
- Relevant buttons for each section
- Smart back navigation
- Quick access to related features

## 🚀 How to Use the New GUI

### 1. **Start the Bot**
```bash
# Activate virtual environment
source venv/bin/activate

# Start full application
python app.py

# OR start GUI-only for testing
python test_gui.py
```

### 2. **Access the GUI**
1. Open Telegram
2. Find your bot
3. Send `/start`
4. **Click buttons to navigate!**

### 3. **Navigation Flow**
```
/start → Main Menu
├── 📊 Scanner Dashboard → All monitoring functions
├── 📈 Market Overview → Market data & trends
├── 🔥 Top Movers → Gainers/losers lists
├── 🚨 Recent Alerts → Alert management
├── ⭐ My Watchlist → Personal tracking
├── ⚙️ Settings → Configuration
├── 🎮 Controls → Scanner management
├── 📊 Performance → Statistics
├── 📡 Status → System health
└── ❓ Help & Guide → Complete help system
```

## 📱 User Experience Improvements

### Before (Command-Based)
- ❌ Had to remember commands
- ❌ Typing required
- ❌ Limited navigation
- ❌ Text-heavy interface

### After (GUI-Based)
- ✅ Click-only navigation
- ✅ Visual button interface
- ✅ Intuitive menu system
- ✅ Mobile-friendly design
- ✅ Context-aware options
- ✅ Real-time data updates

## 🔧 Technical Implementation

### Enhanced Callback Handling
- Comprehensive callback routing
- Context-aware button responses
- Error handling for unknown actions
- Future-proof expandability

### Improved Menu Structure
- Consistent button layouts
- Logical grouping of functions
- Enhanced visual appeal
- Better information density

### Navigation System
- Main menu accessibility from anywhere
- Refresh capabilities on all screens
- Context-sensitive button placement
- Breadcrumb-style navigation

## 🎉 Result

Your Bybit Scanner Bot now provides a **complete GUI experience** through Telegram! Users can:

1. **Navigate entirely with buttons** - no commands to remember
2. **Access all features visually** - intuitive menu system
3. **Get real-time updates** - refresh buttons everywhere
4. **Enjoy mobile-optimized interface** - perfect for phones
5. **Explore features easily** - guided navigation flow

## 🚀 Next Steps

1. **Test the GUI**: Run `python test_gui.py` to test the interface
2. **Configure your bot**: Set up `.env` with your bot token and chat ID
3. **Start using**: Send `/start` to your bot and enjoy the GUI experience!
4. **Explore features**: Click through all the menus to see the full functionality

**Your Telegram bot is now a fully GUI-driven application! 🎮✨**

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

### Option 1: Full Application (Recommended)
```bash
python app.py
```
This starts:
- 📊 Scanner in background thread
- 🤖 Telegram UI bot
- 🌐 Web server for health checks

### Option 2: Telegram UI Only (Testing)
```bash
python run_telegram_ui.py
```

### Option 3: Direct Scanner (Console Output)
```bash
python scanner.py
```

### Web Endpoints
Visit these URLs when running the full application:
- `http://localhost:8080/` - Main status
- `http://localhost:8080/health` - Health check
- `http://localhost:8080/status` - Detailed status
- `http://localhost:8080/test-telegram` - Test Telegram bot
- `http://localhost:8080/api/symbols` - Get tracked symbols
- `http://localhost:8080/api/alerts` - Get alert statistics
- `http://localhost:8080/api/telegram-status` - Telegram UI status

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

## 🤖 Telegram UI Guide

### Getting Started with Telegram UI

1. **Start the bot**: Send `/start` to your bot
2. **Access Dashboard**: Use `/dashboard` or click the 📊 Dashboard button
3. **Monitor Status**: Use `/status` to check scanner health
4. **View Alerts**: Use `/alerts` to see recent notifications
5. **Browse Symbols**: Use `/symbols` to see tracked markets
6. **Adjust Settings**: Use `/settings` to configure thresholds
7. **Control Scanner**: Use `/control` for start/stop/restart operations

### Dashboard Features

The main dashboard (`/dashboard`) provides:
- **Scanner Status**: Current operational status
- **Uptime**: How long the scanner has been running
- **Alert Count**: Total alerts sent
- **Symbol Count**: Number of symbols being tracked
- **Configuration**: Current threshold settings
- **Quick Actions**: Buttons for common operations

### Interactive Controls

All Telegram UI interactions use inline keyboards for easy navigation:
- 🔄 **Refresh buttons**: Get latest data
- 📊 **Navigation buttons**: Move between sections
- ⚙️ **Settings buttons**: Adjust configurations
- 🎮 **Control buttons**: Manage scanner operations

### Real-time Data

The Telegram UI loads all data from the web server in real-time:
- Scanner status and health
- Performance metrics
- Tracked symbols list
- Alert statistics
- Configuration settings

### Multi-User Support

The Telegram UI supports multiple users:
- Each user gets their own session
- Authorized users can control the scanner
- All users receive alerts when conditions are met
- User preferences can be customized individually

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

### Data Access
- `GET /api/symbols` - Get tracked symbols with current data
- `GET /api/alerts` - Get alert statistics and recent alerts
- `GET /api/telegram-status` - Get Telegram UI bot status

### Testing & Control
- `GET /test-telegram` - Test Telegram bot connectivity
- `GET /restart-scanner` - Restart the scanner (debugging)

### Example API Responses

#### `/api/symbols`
```json
{
  "status": "success",
  "count": 25,
  "symbols": [
    {
      "symbol": "BTCUSDT",
      "last_price": "43250.50",
      "volume_24h": "2500000000",
      "price_change_24h": "2.45"
    }
  ]
}
```

#### `/api/telegram-status`
```json
{
  "status": "success",
  "telegram": {
    "ui_thread_active": true,
    "bot_configured": true,
    "chat_configured": true
  }
}
```

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