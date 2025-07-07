#!/usr/bin/env python3
"""
Main Bybit Perpetual Futures Scanner
Scans for volume spikes, pumps/dumps, breakouts, and liquidity changes
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional
from pybit.unified_trading import HTTP
import requests
from config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BybitScanner:
    """Main scanner class for Bybit perpetual futures"""
    
    def __init__(self):
        """Initialize the scanner"""
        self.session = HTTP(testnet=config.BYBIT_TESTNET)
        self.telegram_bot_token = config.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = config.TELEGRAM_CHAT_ID
        
        # Data storage for analysis
        self.previous_data = {}
        self.alerts_sent = 0
        self.start_time = datetime.now()
        
        logger.info("Bybit Scanner initialized")
        logger.info(f"Testnet: {config.BYBIT_TESTNET}")
        logger.info(f"Scan interval: {config.SCAN_INTERVAL_SECONDS} seconds")
    
    async def send_telegram_message(self, message: str) -> bool:
        """Send message to Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                logger.info("Telegram message sent successfully")
                return True
            else:
                logger.error(f"Failed to send Telegram message: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def get_perpetual_instruments(self) -> List[Dict]:
        """Get all perpetual futures instruments"""
        try:
            result = self.session.get_instruments_info(category="linear")
            
            if result.get('retCode') == 0:
                instruments = result.get('result', {}).get('list', [])
                # Filter for perpetual contracts only
                perpetuals = [
                    inst for inst in instruments
                    if inst.get('contractType') == 'LinearPerpetual'
                    and inst.get('status') == 'Trading'
                ]
                logger.info(f"Found {len(perpetuals)} perpetual instruments")
                return perpetuals
            else:
                logger.error(f"Failed to get instruments: {result.get('retMsg')}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting instruments: {e}")
            return []
    
    def get_ticker_data(self, symbols: List[str] = None) -> List[Dict]:
        """Get ticker data for symbols"""
        try:
            if symbols:
                all_tickers = []
                for symbol in symbols:
                    result = self.session.get_tickers(category="linear", symbol=symbol)
                    if result.get('retCode') == 0:
                        tickers = result.get('result', {}).get('list', [])
                        all_tickers.extend(tickers)
                    time.sleep(0.1)  # Rate limiting
                return all_tickers
            else:
                result = self.session.get_tickers(category="linear")
                if result.get('retCode') == 0:
                    return result.get('result', {}).get('list', [])
                else:
                    logger.error(f"Failed to get tickers: {result.get('retMsg')}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting ticker data: {e}")
            return []
    
    def get_kline_data(self, symbol: str, interval: str = "1", limit: int = 60) -> List:
        """Get kline data for technical analysis"""
        try:
            result = self.session.get_kline(
                category="linear",
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            if result.get('retCode') == 0:
                return result.get('result', {}).get('list', [])
            else:
                logger.error(f"Failed to get klines for {symbol}: {result.get('retMsg')}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting klines for {symbol}: {e}")
            return []
    
    def get_orderbook(self, symbol: str) -> Dict:
        """Get orderbook for liquidity analysis"""
        try:
            result = self.session.get_orderbook(category="linear", symbol=symbol, limit=25)
            
            if result.get('retCode') == 0:
                return result.get('result', {})
            else:
                logger.error(f"Failed to get orderbook for {symbol}: {result.get('retMsg')}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting orderbook for {symbol}: {e}")
            return {}
    
    def analyze_volume_spike(self, symbol: str, current_data: Dict, previous_data: Dict) -> Optional[Dict]:
        """Analyze for volume spikes"""
        try:
            current_volume = float(current_data.get('volume24h', 0))
            previous_volume = float(previous_data.get('volume24h', 0))
            
            if previous_volume == 0:
                return None
            
            volume_change = (current_volume - previous_volume) / previous_volume * 100
            
            if volume_change >= config.VOLUME_SPIKE_THRESHOLD * 100:
                return {
                    'type': 'volume_spike',
                    'symbol': symbol,
                    'current_volume': current_volume,
                    'previous_volume': previous_volume,
                    'change_percent': volume_change
                }
        except Exception as e:
            logger.error(f"Error analyzing volume spike for {symbol}: {e}")
        
        return None
    
    def analyze_price_movement(self, symbol: str, klines: List) -> Optional[Dict]:
        """Analyze for price pumps/dumps"""
        try:
            if len(klines) < 5:
                return None
            
            # Get recent prices (klines are in reverse chronological order)
            current_price = float(klines[0][4])  # Close price of most recent candle
            price_5min_ago = float(klines[4][4])  # Close price 5 minutes ago
            
            price_change = (current_price - price_5min_ago) / price_5min_ago * 100
            
            if price_change >= config.PRICE_PUMP_THRESHOLD:
                return {
                    'type': 'price_pump',
                    'symbol': symbol,
                    'current_price': current_price,
                    'previous_price': price_5min_ago,
                    'change_percent': price_change,
                    'timeframe': '5min'
                }
            elif price_change <= config.PRICE_DUMP_THRESHOLD:
                return {
                    'type': 'price_dump',
                    'symbol': symbol,
                    'current_price': current_price,
                    'previous_price': price_5min_ago,
                    'change_percent': price_change,
                    'timeframe': '5min'
                }
        except Exception as e:
            logger.error(f"Error analyzing price movement for {symbol}: {e}")
        
        return None
    
    def analyze_volatility(self, symbol: str, klines: List) -> Optional[Dict]:
        """Analyze for volatility spikes"""
        try:
            if len(klines) < 10:
                return None
            
            # Calculate volatility from recent candles
            volatilities = []
            for kline in klines[:10]:
                high = float(kline[2])
                low = float(kline[3])
                close = float(kline[4])
                volatility = (high - low) / close * 100
                volatilities.append(volatility)
            
            current_volatility = volatilities[0]
            avg_volatility = sum(volatilities[1:]) / len(volatilities[1:])
            
            if current_volatility >= config.VOLATILITY_THRESHOLD:
                return {
                    'type': 'volatility_spike',
                    'symbol': symbol,
                    'current_volatility': current_volatility,
                    'avg_volatility': avg_volatility
                }
        except Exception as e:
            logger.error(f"Error analyzing volatility for {symbol}: {e}")
        
        return None
    
    def analyze_breakout(self, symbol: str, klines: List, current_price: float) -> Optional[Dict]:
        """Analyze for breakout patterns"""
        try:
            if len(klines) < config.BREAKOUT_LOOKBACK_PERIODS:
                return None
            
            # Calculate support and resistance from recent candles
            highs = [float(kline[2]) for kline in klines[:config.BREAKOUT_LOOKBACK_PERIODS]]
            lows = [float(kline[3]) for kline in klines[:config.BREAKOUT_LOOKBACK_PERIODS]]
            
            resistance = max(highs)
            support = min(lows)
            
            # Check for breakouts (with 0.1% buffer)
            if current_price > resistance * 1.001:
                return {
                    'type': 'breakout_up',
                    'symbol': symbol,
                    'current_price': current_price,
                    'resistance_level': resistance,
                    'breakout_strength': (current_price - resistance) / resistance * 100
                }
            elif current_price < support * 0.999:
                return {
                    'type': 'breakout_down',
                    'symbol': symbol,
                    'current_price': current_price,
                    'support_level': support,
                    'breakout_strength': (support - current_price) / support * 100
                }
        except Exception as e:
            logger.error(f"Error analyzing breakout for {symbol}: {e}")
        
        return None
    
    def should_scan_symbol(self, ticker: Dict) -> bool:
        """Check if symbol meets scanning criteria"""
        try:
            volume_24h = float(ticker.get('volume24h', 0))
            price = float(ticker.get('lastPrice', 0))
            
            # Apply filters
            if volume_24h < config.MIN_VOLUME_24H:
                return False
            
            if price < config.MIN_PRICE or price > config.MAX_PRICE:
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error checking symbol criteria: {e}")
            return False
    
    async def format_alert_message(self, alert: Dict) -> str:
        """Format alert message for Telegram"""
        symbol = alert['symbol']
        alert_type = alert['type']
        
        if alert_type == 'volume_spike':
            return f"""
🚨 <b>VOLUME SPIKE ALERT</b> 🚨

📊 <b>Symbol:</b> {symbol}
📈 <b>Volume Change:</b> +{alert['change_percent']:.1f}%
💰 <b>Current Volume:</b> ${alert['current_volume']:,.0f}
📊 <b>Previous Volume:</b> ${alert['previous_volume']:,.0f}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            """.strip()
        
        elif alert_type in ['price_pump', 'price_dump']:
            emoji = "🚀" if alert_type == 'price_pump' else "📉"
            action = "PUMP" if alert_type == 'price_pump' else "DUMP"
            
            return f"""
{emoji} <b>{action} ALERT</b> {emoji}

💰 <b>Symbol:</b> {symbol}
💵 <b>Price Change ({alert['timeframe']}):</b> {alert['change_percent']:+.2f}%
📈 <b>Current Price:</b> ${alert['current_price']:.6f}
📊 <b>Previous Price:</b> ${alert['previous_price']:.6f}

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            """.strip()
        
        elif alert_type == 'volatility_spike':
            return f"""
⚡ <b>VOLATILITY SPIKE ALERT</b> ⚡

💰 <b>Symbol:</b> {symbol}
📊 <b>Current Volatility:</b> {alert['current_volatility']:.2f}%
📈 <b>Average Volatility:</b> {alert['avg_volatility']:.2f}%

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            """.strip()
        
        elif alert_type in ['breakout_up', 'breakout_down']:
            emoji = "⬆️" if alert_type == 'breakout_up' else "⬇️"
            direction = "UP" if alert_type == 'breakout_up' else "DOWN"
            level_key = 'resistance_level' if alert_type == 'breakout_up' else 'support_level'
            
            return f"""
{emoji} <b>BREAKOUT ALERT</b> {emoji}

💰 <b>Symbol:</b> {symbol}
📊 <b>Direction:</b> {direction}
💵 <b>Current Price:</b> ${alert['current_price']:.6f}
🎯 <b>Breakout Level:</b> ${alert[level_key]:.6f}
💪 <b>Strength:</b> {alert['breakout_strength']:.2f}%

⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            """.strip()
        
        return f"Alert: {alert_type} for {symbol}"
    
    async def scan_symbols(self):
        """Main scanning function"""
        try:
            logger.info("Starting symbol scan...")
            
            # Get all tickers
            tickers = self.get_ticker_data()
            if not tickers:
                logger.warning("No ticker data received")
                return
            
            # Filter symbols to scan
            symbols_to_scan = [
                ticker for ticker in tickers
                if self.should_scan_symbol(ticker)
            ]
            
            logger.info(f"Scanning {len(symbols_to_scan)} symbols")
            
            alerts = []
            
            for ticker in symbols_to_scan[:50]:  # Limit to top 50 to avoid rate limits
                symbol = ticker['symbol']
                
                try:
                    # Volume spike analysis
                    if symbol in self.previous_data:
                        volume_alert = self.analyze_volume_spike(symbol, ticker, self.previous_data[symbol])
                        if volume_alert:
                            alerts.append(volume_alert)
                    
                    # Get kline data for technical analysis
                    klines = self.get_kline_data(symbol, "1", 60)
                    if klines:
                        # Price movement analysis
                        price_alert = self.analyze_price_movement(symbol, klines)
                        if price_alert:
                            alerts.append(price_alert)
                        
                        # Volatility analysis
                        volatility_alert = self.analyze_volatility(symbol, klines)
                        if volatility_alert:
                            alerts.append(volatility_alert)
                        
                        # Breakout analysis
                        current_price = float(ticker['lastPrice'])
                        breakout_alert = self.analyze_breakout(symbol, klines, current_price)
                        if breakout_alert:
                            alerts.append(breakout_alert)
                    
                    # Store current data for next iteration
                    self.previous_data[symbol] = ticker
                    
                    # Rate limiting
                    time.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Error scanning symbol {symbol}: {e}")
                    continue
            
            # Send alerts
            for alert in alerts:
                try:
                    message = await self.format_alert_message(alert)
                    success = await self.send_telegram_message(message)
                    if success:
                        self.alerts_sent += 1
                        logger.info(f"Alert sent for {alert['symbol']}: {alert['type']}")
                    
                    # Also send to Telegram UI users if available
                    try:
                        from telegram_ui import telegram_ui
                        if telegram_ui:
                            await telegram_ui.send_alert_to_ui_users(message)
                    except ImportError:
                        pass  # Telegram UI not available
                    except Exception as ui_error:
                        logger.error(f"Error sending alert to UI users: {ui_error}")
                    
                    # Rate limit Telegram messages
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error sending alert: {e}")
            
            logger.info(f"Scan completed. Found {len(alerts)} alerts")
            
        except Exception as e:
            logger.error(f"Error in scan_symbols: {e}")
    
    async def send_startup_message(self):
        """Send startup notification"""
        message = f"""
🤖 <b>Bybit Scanner Bot Started</b> 🤖

✅ <b>Status:</b> Online and monitoring
📊 <b>Scanning:</b> Perpetual futures
⏱️ <b>Interval:</b> Every {config.SCAN_INTERVAL_SECONDS} seconds
🎯 <b>Filters:</b> Volume ≥ ${config.MIN_VOLUME_24H:,.0f}

⏰ <b>Started:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        
        await self.send_telegram_message(message)
    
    async def run(self):
        """Main run loop"""
        logger.info("Starting Bybit Scanner...")
        
        # Validate configuration
        try:
            config.validate()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            return
        
        # Send startup message
        if config.TELEGRAM_CHAT_ID and config.TELEGRAM_CHAT_ID != 'YOUR_CHAT_ID_HERE':
            await self.send_startup_message()
        else:
            logger.warning("TELEGRAM_CHAT_ID not configured - alerts will not be sent")
        
        # Main scanning loop
        while True:
            try:
                await self.scan_symbols()
                
                # Log status every hour
                uptime_hours = (datetime.now() - self.start_time).total_seconds() / 3600
                if int(uptime_hours) > 0 and int(uptime_hours) % 1 == 0:
                    logger.info(f"Scanner running for {uptime_hours:.1f} hours. Alerts sent: {self.alerts_sent}")
                
                # Wait for next scan
                await asyncio.sleep(config.SCAN_INTERVAL_SECONDS)
                
            except KeyboardInterrupt:
                logger.info("Scanner stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(30)  # Wait before retrying

async def main():
    """Main entry point"""
    scanner = BybitScanner()
    await scanner.run()

if __name__ == "__main__":
    asyncio.run(main())