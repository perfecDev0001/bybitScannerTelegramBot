#!/usr/bin/env python3
"""
Bybit Public API Endpoints Guide
This script demonstrates ALL public endpoints that work WITHOUT API key/secret.
"""

import json
import requests
from datetime import datetime
from pybit.unified_trading import HTTP

class BybitPublicAPI:
    def __init__(self, testnet=False):
        """Initialize public API client (no authentication needed)."""
        self.testnet = testnet
        self.base_url = "https://api-testnet.bybit.com" if testnet else "https://api.bybit.com"
        
        # Create public session (no API key needed)
        self.session = HTTP(testnet=testnet)
        
        print(f"🌐 Bybit Public API Client")
        print(f"📡 Base URL: {self.base_url}")
        print(f"🔓 Authentication: NOT REQUIRED")
        print("-" * 50)
    
    def print_result(self, title, result):
        """Pretty print results."""
        print(f"\n📋 {title}")
        print("=" * 60)
        if isinstance(result, dict):
            print(json.dumps(result, indent=2, default=str))
        else:
            print(result)
        print("=" * 60)
    
    def safe_api_call(self, title, func, *args, **kwargs):
        """Make API call with error handling."""
        try:
            print(f"\n🔄 {title}")
            result = func(*args, **kwargs)
            self.print_result(title, result)
            return result
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    # ==========================================
    # 1. SERVER & SYSTEM INFORMATION
    # ==========================================
    
    def get_server_time(self):
        """Get Bybit server time."""
        return self.safe_api_call(
            "Server Time",
            self.session.get_server_time
        )
    
    def get_announcements(self):
        """Get system announcements."""
        return self.safe_api_call(
            "System Announcements",
            self.session.get_announcements,
            locale="en-US"
        )

    # ==========================================
    # 2. MARKET DATA - INSTRUMENTS
    # ==========================================
    
    def get_spot_instruments(self):
        """Get all spot trading pairs."""
        return self.safe_api_call(
            "Spot Instruments (All)",
            self.session.get_instruments_info,
            category="spot"
        )
    
    def get_linear_instruments(self):
        """Get linear futures instruments."""
        return self.safe_api_call(
            "Linear Futures Instruments",
            self.session.get_instruments_info,
            category="linear"
        )
    
    def get_inverse_instruments(self):
        """Get inverse futures instruments."""
        return self.safe_api_call(
            "Inverse Futures Instruments",
            self.session.get_instruments_info,
            category="inverse"
        )
    
    def get_option_instruments(self):
        """Get options instruments."""
        return self.safe_api_call(
            "Options Instruments",
            self.session.get_instruments_info,
            category="option"
        )

    # ==========================================
    # 3. MARKET DATA - ORDERBOOK & TRADES
    # ==========================================
    
    def get_orderbook(self, symbol="BTCUSDT", category="spot"):
        """Get orderbook (bid/ask prices)."""
        return self.safe_api_call(
            f"Orderbook ({symbol})",
            self.session.get_orderbook,
            category=category,
            symbol=symbol
        )
    
    def get_recent_trades(self, symbol="BTCUSDT", category="spot", limit=10):
        """Get recent public trades."""
        return self.safe_api_call(
            f"Recent Trades ({symbol})",
            self.session.get_public_trade_history,
            category=category,
            symbol=symbol,
            limit=limit
        )

    # ==========================================
    # 4. MARKET DATA - KLINES/CANDLESTICKS
    # ==========================================
    
    def get_klines(self, symbol="BTCUSDT", category="spot", interval="60", limit=5):
        """Get kline/candlestick data."""
        return self.safe_api_call(
            f"Klines ({symbol} - {interval}min)",
            self.session.get_kline,
            category=category,
            symbol=symbol,
            interval=interval,
            limit=limit
        )
    
    def get_mark_price_klines(self, symbol="BTCUSDT", category="linear", interval="60", limit=5):
        """Get mark price klines (futures only)."""
        return self.safe_api_call(
            f"Mark Price Klines ({symbol})",
            self.session.get_mark_price_kline,
            category=category,
            symbol=symbol,
            interval=interval,
            limit=limit
        )
    
    def get_index_price_klines(self, symbol="BTCUSDT", category="linear", interval="60", limit=5):
        """Get index price klines (futures only)."""
        return self.safe_api_call(
            f"Index Price Klines ({symbol})",
            self.session.get_index_price_kline,
            category=category,
            symbol=symbol,
            interval=interval,
            limit=limit
        )
    
    def get_premium_index_klines(self, symbol="BTCUSDT", category="linear", interval="60", limit=5):
        """Get premium index klines (futures only)."""
        return self.safe_api_call(
            f"Premium Index Klines ({symbol})",
            self.session.get_premium_index_price_kline,
            category=category,
            symbol=symbol,
            interval=interval,
            limit=limit
        )

    # ==========================================
    # 5. MARKET DATA - TICKERS & STATISTICS
    # ==========================================
    
    def get_ticker(self, symbol="BTCUSDT", category="spot"):
        """Get 24hr ticker for specific symbol."""
        return self.safe_api_call(
            f"24hr Ticker ({symbol})",
            self.session.get_tickers,
            category=category,
            symbol=symbol
        )
    
    def get_all_tickers(self, category="spot"):
        """Get all tickers for a category."""
        return self.safe_api_call(
            f"All {category.title()} Tickers",
            self.session.get_tickers,
            category=category
        )

    # ==========================================
    # 6. FUTURES-SPECIFIC DATA
    # ==========================================
    
    def get_funding_rate(self, symbol="BTCUSDT", category="linear", limit=10):
        """Get funding rate history."""
        return self.safe_api_call(
            f"Funding Rate History ({symbol})",
            self.session.get_funding_rate_history,
            category=category,
            symbol=symbol,
            limit=limit
        )
    
    def get_open_interest(self, symbol="BTCUSDT", category="linear", intervalTime="5min", limit=10):
        """Get open interest data."""
        return self.safe_api_call(
            f"Open Interest ({symbol})",
            self.session.get_open_interest,
            category=category,
            symbol=symbol,
            intervalTime=intervalTime,
            limit=limit
        )
    
    def get_long_short_ratio(self, symbol="BTCUSDT", category="linear", period="5min", limit=10):
        """Get long/short ratio."""
        return self.safe_api_call(
            f"Long/Short Ratio ({symbol})",
            self.session.get_long_short_ratio,
            category=category,
            symbol=symbol,
            period=period,
            limit=limit
        )

    # ==========================================
    # 7. OPTIONS-SPECIFIC DATA
    # ==========================================
    
    def get_historical_volatility(self, baseCoin="BTC", category="option"):
        """Get historical volatility for options."""
        return self.safe_api_call(
            f"Historical Volatility ({baseCoin})",
            self.session.get_historical_volatility,
            category=category,
            baseCoin=baseCoin
        )

    # ==========================================
    # 8. INSURANCE & RISK DATA
    # ==========================================
    
    def get_insurance_fund(self, coin="BTC"):
        """Get insurance fund data."""
        return self.safe_api_call(
            f"Insurance Fund ({coin})",
            self.session.get_insurance,
            coin=coin
        )
    
    def get_risk_limit(self, symbol="BTCUSDT", category="linear"):
        """Get risk limit information."""
        return self.safe_api_call(
            f"Risk Limit ({symbol})",
            self.session.get_risk_limit,
            category=category,
            symbol=symbol
        )

    # ==========================================
    # 9. DELIVERY & SETTLEMENT DATA
    # ==========================================
    
    def get_delivery_price(self, symbol="BTC", category="option", limit=10):
        """Get delivery price history."""
        return self.safe_api_call(
            f"Delivery Price ({symbol})",
            self.session.get_delivery_price,
            category=category,
            symbol=symbol,
            limit=limit
        )

    # ==========================================
    # 10. DIRECT HTTP REQUESTS (Alternative Method)
    # ==========================================
    
    def direct_http_request(self, endpoint, params=None):
        """Make direct HTTP request to public endpoint."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            self.print_result(f"Direct HTTP: {endpoint}", result)
            return result
        except Exception as e:
            print(f"❌ Direct HTTP Error: {e}")
            return None

    # ==========================================
    # DEMONSTRATION FUNCTIONS
    # ==========================================
    
    def demo_basic_market_data(self):
        """Demonstrate basic market data endpoints."""
        print("\n" + "="*80)
        print("📊 BASIC MARKET DATA (No Auth Required)")
        print("="*80)
        
        # Server time
        self.get_server_time()
        
        # BTC price
        self.get_ticker("BTCUSDT", "spot")
        
        # Orderbook
        self.get_orderbook("BTCUSDT", "spot")
        
        # Recent trades
        self.get_recent_trades("BTCUSDT", "spot", 5)
        
        # Klines
        self.get_klines("BTCUSDT", "spot", "60", 5)
    
    def demo_all_categories(self):
        """Demonstrate different trading categories."""
        print("\n" + "="*80)
        print("🎯 ALL TRADING CATEGORIES")
        print("="*80)
        
        categories = ["spot", "linear", "inverse"]
        
        for category in categories:
            print(f"\n--- {category.upper()} CATEGORY ---")
            
            # Get instruments
            if category == "spot":
                self.get_spot_instruments()
            elif category == "linear":
                self.get_linear_instruments()
            elif category == "inverse":
                self.get_inverse_instruments()
            
            # Get tickers (limited to avoid spam)
            result = self.get_ticker("BTCUSDT" if category != "inverse" else "BTCUSD", category)
    
    def demo_advanced_data(self):
        """Demonstrate advanced market data."""
        print("\n" + "="*80)
        print("📈 ADVANCED MARKET DATA")
        print("="*80)
        
        # Funding rates
        self.get_funding_rate("BTCUSDT", "linear", 5)
        
        # Open interest
        self.get_open_interest("BTCUSDT", "linear", "5min", 5)
        
        # Long/short ratio
        self.get_long_short_ratio("BTCUSDT", "linear", "5min", 5)
        
        # Historical volatility
        self.get_historical_volatility("BTC", "option")
        
        # Insurance fund
        self.get_insurance_fund("BTC")
    
    def demo_direct_http(self):
        """Demonstrate direct HTTP requests."""
        print("\n" + "="*80)
        print("🌐 DIRECT HTTP REQUESTS")
        print("="*80)
        
        # Direct server time request
        self.direct_http_request("/v5/market/time")
        
        # Direct ticker request
        self.direct_http_request("/v5/market/tickers", {"category": "spot", "symbol": "BTCUSDT"})
        
        # Direct orderbook request
        self.direct_http_request("/v5/market/orderbook", {"category": "spot", "symbol": "BTCUSDT"})
    
    def show_all_public_endpoints(self):
        """Show comprehensive list of all public endpoints."""
        print("\n" + "="*80)
        print("📋 ALL PUBLIC ENDPOINTS AVAILABLE")
        print("="*80)
        
        endpoints = {
            "🕐 Server & System": [
                "/v5/market/time - Server time",
                "/v5/announcements/index - System announcements"
            ],
            "📊 Market Data": [
                "/v5/market/instruments-info - Trading instruments",
                "/v5/market/orderbook - Order book",
                "/v5/market/tickers - 24hr ticker statistics",
                "/v5/market/trading-records - Recent trades",
                "/v5/market/kline - Kline/candlestick data",
                "/v5/market/mark-price-kline - Mark price klines",
                "/v5/market/index-price-kline - Index price klines",
                "/v5/market/premium-index-price-kline - Premium index klines"
            ],
            "🎯 Futures Data": [
                "/v5/market/funding/history - Funding rate history",
                "/v5/market/open-interest - Open interest",
                "/v5/market/account-ratio - Long/short ratio",
                "/v5/market/risk-limit - Risk limit info"
            ],
            "📈 Options Data": [
                "/v5/market/historical-volatility - Historical volatility",
                "/v5/market/delivery-price - Delivery price"
            ],
            "🛡️ Risk & Insurance": [
                "/v5/market/insurance - Insurance fund",
                "/v5/market/risk-limit - Risk limits"
            ]
        }
        
        for category, endpoint_list in endpoints.items():
            print(f"\n{category}:")
            for endpoint in endpoint_list:
                print(f"  • {endpoint}")
    
    def run_comprehensive_demo(self):
        """Run comprehensive demonstration of all public endpoints."""
        print("🚀 Bybit Public API Comprehensive Demo")
        print("🔓 No API Key Required - All Public Endpoints")
        print("=" * 80)
        
        # Show all available endpoints
        self.show_all_public_endpoints()
        
        # Demo basic market data
        self.demo_basic_market_data()
        
        # Demo different categories
        self.demo_all_categories()
        
        # Demo advanced data
        self.demo_advanced_data()
        
        # Demo direct HTTP
        self.demo_direct_http()
        
        print("\n" + "="*80)
        print("✅ PUBLIC API DEMO COMPLETED")
        print("🔓 All functions work WITHOUT API key/secret")
        print("📊 Perfect for market data, analysis, and monitoring")
        print("💡 Use these for building trading bots, price alerts, etc.")
        print("="*80)

def main():
    """Main function."""
    print("Choose environment:")
    print("1. Mainnet (real data)")
    print("2. Testnet (test data)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    testnet = choice == "2"
    
    try:
        api = BybitPublicAPI(testnet=testnet)
        api.run_comprehensive_demo()
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())