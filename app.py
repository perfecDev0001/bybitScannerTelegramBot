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

def start_scanner():
    """Start the scanner in a background thread"""
    global scanner_thread
    
    logger.info("Starting scanner thread...")
    scanner_thread = threading.Thread(target=run_scanner, daemon=True)
    scanner_thread.start()

if __name__ == '__main__':
    # Start the scanner
    start_scanner()
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )