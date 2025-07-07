#!/usr/bin/env python3
"""
Flask web server for Render deployment
Provides health checks and runs the scanner in background
"""

import asyncio
import threading
import logging
from datetime import datetime
from flask import Flask, jsonify
from scanner import BybitScanner
from telegram_ui import initialize_telegram_ui, start_telegram_ui, stop_telegram_ui
from config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Global scanner instance
scanner = None
scanner_thread = None
telegram_ui_thread = None
scanner_status = {
    'status': 'starting',
    'start_time': datetime.now(),
    'alerts_sent': 0,
    'last_scan': None,
    'error': None
}

def run_scanner():
    """Run the scanner in a separate thread"""
    global scanner, scanner_status
    
    try:
        scanner_status['status'] = 'running'
        scanner = BybitScanner()
        
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the scanner
        loop.run_until_complete(scanner.run())
        
    except Exception as e:
        logger.error(f"Scanner error: {e}")
        scanner_status['status'] = 'error'
        scanner_status['error'] = str(e)

def run_telegram_ui():
    """Run the Telegram UI in a separate thread"""
    global scanner
    
    try:
        logger.info("Starting Telegram UI thread...")
        
        # Set up event loop for this thread
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Create Telegram UI
        from telegram_ui import TelegramUI
        from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
        
        telegram_ui = TelegramUI(scanner)
        
        # Build application
        application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", telegram_ui.cmd_start))
        application.add_handler(CallbackQueryHandler(telegram_ui.handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_ui.handle_message))
        
        # Set the application in telegram_ui
        telegram_ui.application = application
        
        logger.info("Starting Telegram bot with manual polling...")
        
        # Use manual polling approach that works in threads
        async def run_bot():
            await application.initialize()
            await application.start()
            await application.updater.start_polling()
            
            # Keep running
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("Telegram UI stopped")
            finally:
                await application.updater.stop()
                await application.stop()
                await application.shutdown()
        
        # Run the bot
        loop.run_until_complete(run_bot())
        
    except Exception as e:
        logger.error(f"Telegram UI error: {e}")

@app.route('/')
def home():
    """Home page with basic info"""
    return jsonify({
        'name': 'Bybit Scanner Telegram Bot',
        'version': '1.0.0',
        'status': scanner_status['status'],
        'uptime_seconds': (datetime.now() - scanner_status['start_time']).total_seconds(),
        'alerts_sent': scanner_status.get('alerts_sent', 0),
        'configuration': {
            'scan_interval': config.SCAN_INTERVAL_SECONDS,
            'testnet': config.BYBIT_TESTNET,
            'min_volume_24h': config.MIN_VOLUME_24H,
            'price_pump_threshold': config.PRICE_PUMP_THRESHOLD,
            'volume_spike_threshold': config.VOLUME_SPIKE_THRESHOLD
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    global scanner
    
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'scanner_status': scanner_status['status'],
        'uptime_seconds': (datetime.now() - scanner_status['start_time']).total_seconds()
    }
    
    # Check if scanner is running
    if scanner_status['status'] == 'error':
        health_status['status'] = 'unhealthy'
        health_status['error'] = scanner_status.get('error')
        return jsonify(health_status), 500
    
    # Test API connectivity
    try:
        if scanner:
            from pybit.unified_trading import HTTP
            test_session = HTTP(testnet=config.BYBIT_TESTNET)
            result = test_session.get_server_time()
            
            if result.get('retCode') == 0:
                health_status['api_status'] = 'connected'
            else:
                health_status['api_status'] = 'error'
                health_status['api_error'] = result.get('retMsg')
        else:
            health_status['api_status'] = 'not_initialized'
            
    except Exception as e:
        health_status['api_status'] = 'error'
        health_status['api_error'] = str(e)
    
    return jsonify(health_status)

@app.route('/status')
def status():
    """Detailed status information"""
    global scanner
    
    status_info = {
        'scanner': {
            'status': scanner_status['status'],
            'start_time': scanner_status['start_time'].isoformat(),
            'uptime_hours': (datetime.now() - scanner_status['start_time']).total_seconds() / 3600,
            'alerts_sent': scanner.alerts_sent if scanner else 0,
            'symbols_tracked': len(scanner.previous_data) if scanner else 0
        },
        'configuration': {
            'scan_interval_seconds': config.SCAN_INTERVAL_SECONDS,
            'bybit_testnet': config.BYBIT_TESTNET,
            'telegram_configured': bool(config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID != 'YOUR_CHAT_ID_HERE'),
            'thresholds': {
                'volume_spike': config.VOLUME_SPIKE_THRESHOLD,
                'price_pump': config.PRICE_PUMP_THRESHOLD,
                'price_dump': config.PRICE_DUMP_THRESHOLD,
                'volatility': config.VOLATILITY_THRESHOLD,
                'liquidity_drop': config.LIQUIDITY_DROP_THRESHOLD
            },
            'filters': {
                'min_volume_24h': config.MIN_VOLUME_24H,
                'min_price': config.MIN_PRICE,
                'max_price': config.MAX_PRICE
            }
        },
        'system': {
            'timestamp': datetime.now().isoformat(),
            'debug_mode': config.DEBUG
        }
    }
    
    if scanner_status.get('error'):
        status_info['scanner']['error'] = scanner_status['error']
    
    return jsonify(status_info)

@app.route('/test-telegram')
def test_telegram():
    """Test Telegram bot connectivity"""
    try:
        if not config.TELEGRAM_BOT_TOKEN:
            return jsonify({'error': 'Telegram bot token not configured'}), 400
        
        if config.TELEGRAM_CHAT_ID == 'YOUR_CHAT_ID_HERE':
            return jsonify({'error': 'Telegram chat ID not configured'}), 400
        
        # Create a test scanner instance
        test_scanner = BybitScanner()
        
        # Create event loop for async operation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Send test message
        test_message = f"""
🧪 <b>Test Message</b>

✅ Telegram bot is working correctly!
⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        
        success = loop.run_until_complete(test_scanner.send_telegram_message(test_message))
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Test message sent successfully',
                'chat_id': config.TELEGRAM_CHAT_ID
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to send test message'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Telegram test failed: {str(e)}'
        }), 500

@app.route('/restart-scanner')
def restart_scanner():
    """Restart the scanner (for debugging)"""
    global scanner_thread, scanner_status
    
    try:
        # Stop current scanner if running
        if scanner_thread and scanner_thread.is_alive():
            logger.info("Stopping current scanner...")
            # Note: This is a simple restart - in production you'd want more graceful shutdown
        
        # Reset status
        scanner_status = {
            'status': 'restarting',
            'start_time': datetime.now(),
            'alerts_sent': 0,
            'last_scan': None,
            'error': None
        }
        
        # Start new scanner thread
        scanner_thread = threading.Thread(target=run_scanner, daemon=True)
        scanner_thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Scanner restart initiated',
            'restart_time': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to restart scanner: {str(e)}'
        }), 500

@app.route('/api/symbols')
def api_symbols():
    """API endpoint to get tracked symbols"""
    global scanner
    
    try:
        if scanner and hasattr(scanner, 'previous_data'):
            symbols_data = []
            for symbol, data in scanner.previous_data.items():
                symbols_data.append({
                    'symbol': symbol,
                    'last_price': data.get('lastPrice', 0),
                    'volume_24h': data.get('volume24h', 0),
                    'price_change_24h': data.get('price24hPcnt', 0)
                })
            
            return jsonify({
                'status': 'success',
                'count': len(symbols_data),
                'symbols': symbols_data[:50]  # Limit to 50 for performance
            })
        else:
            return jsonify({
                'status': 'success',
                'count': 0,
                'symbols': []
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/alerts')
def api_alerts():
    """API endpoint to get recent alerts"""
    global scanner
    
    try:
        # In a real implementation, you'd store alerts in a database
        # For now, return basic alert statistics
        alerts_data = {
            'total_alerts': scanner.alerts_sent if scanner else 0,
            'last_24h': 0,  # Would be calculated from stored alerts
            'recent_alerts': []  # Would be fetched from database
        }
        
        return jsonify({
            'status': 'success',
            'data': alerts_data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/telegram-status')
def api_telegram_status():
    """API endpoint to check Telegram UI status"""
    global telegram_ui_thread
    
    try:
        telegram_status = {
            'ui_thread_active': telegram_ui_thread.is_alive() if telegram_ui_thread else False,
            'bot_configured': bool(config.TELEGRAM_BOT_TOKEN),
            'chat_configured': bool(config.TELEGRAM_CHAT_ID and config.TELEGRAM_CHAT_ID != 'YOUR_CHAT_ID_HERE')
        }
        
        return jsonify({
            'status': 'success',
            'telegram': telegram_status
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def start_scanner():
    """Start the scanner in a background thread"""
    global scanner_thread
    
    logger.info("Starting scanner thread...")
    scanner_thread = threading.Thread(target=run_scanner, daemon=True)
    scanner_thread.start()

def start_telegram_ui_thread():
    """Start the Telegram UI in a background thread"""
    global telegram_ui_thread
    
    logger.info("Starting Telegram UI thread...")
    telegram_ui_thread = threading.Thread(target=run_telegram_ui, daemon=True)
    telegram_ui_thread.start()

if __name__ == '__main__':
    # Start the scanner
    start_scanner()
    
    # Start the Telegram UI
    start_telegram_ui_thread()
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )