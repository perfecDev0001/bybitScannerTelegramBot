#!/usr/bin/env python3
"""
Configuration settings for Bybit Scanner Telegram Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # Bybit API Configuration
    BYBIT_API_KEY = os.getenv('BYBIT_API_KEY', '')
    BYBIT_API_SECRET = os.getenv('BYBIT_API_SECRET', '')
    BYBIT_TESTNET = os.getenv('BYBIT_TESTNET', 'False').lower() == 'true'
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')  # Your chat ID for alerts
    
    # Scanner Configuration
    SCAN_INTERVAL_SECONDS = int(os.getenv('SCAN_INTERVAL_SECONDS', '60'))  # 1 minute default
    
    # Alert Thresholds
    VOLUME_SPIKE_THRESHOLD = float(os.getenv('VOLUME_SPIKE_THRESHOLD', '2.0'))  # 200% increase
    PRICE_PUMP_THRESHOLD = float(os.getenv('PRICE_PUMP_THRESHOLD', '5.0'))     # 5% price change
    PRICE_DUMP_THRESHOLD = float(os.getenv('PRICE_DUMP_THRESHOLD', '-5.0'))    # -5% price change
    VOLATILITY_THRESHOLD = float(os.getenv('VOLATILITY_THRESHOLD', '10.0'))    # 10% volatility
    LIQUIDITY_DROP_THRESHOLD = float(os.getenv('LIQUIDITY_DROP_THRESHOLD', '50.0'))  # 50% liquidity drop
    
    # Filters
    MIN_VOLUME_24H = float(os.getenv('MIN_VOLUME_24H', '1000000'))  # $1M minimum 24h volume
    MIN_PRICE = float(os.getenv('MIN_PRICE', '0.001'))              # Minimum price filter
    MAX_PRICE = float(os.getenv('MAX_PRICE', '100000'))             # Maximum price filter
    
    # Technical Analysis
    BREAKOUT_LOOKBACK_PERIODS = int(os.getenv('BREAKOUT_LOOKBACK_PERIODS', '20'))  # 20 periods for S/R
    RSI_PERIOD = int(os.getenv('RSI_PERIOD', '14'))                               # RSI calculation period
    
    # Render/Production Configuration
    PORT = int(os.getenv('PORT', '8080'))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SERVER_URL = os.getenv('SERVER_URL', f'http://localhost:{int(os.getenv("PORT", "8080"))}')
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', '100'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_fields = [
            ('TELEGRAM_BOT_TOKEN', cls.TELEGRAM_BOT_TOKEN),
        ]
        
        missing_fields = []
        for field_name, field_value in required_fields:
            if not field_value:
                missing_fields.append(field_name)
        
        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
        
        return True

# Create global config instance
config = Config()