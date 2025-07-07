#!/usr/bin/env python3
"""
Test script for the Bybit Scanner
Run this locally to test functionality before deployment
"""

import asyncio
import logging
from scanner import BybitScanner
from config import config

# Configure logging for testing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_api_connectivity():
    """Test Bybit API connectivity"""
    print("\n" + "="*50)
    print("🔍 TESTING BYBIT API CONNECTIVITY")
    print("="*50)
    
    scanner = BybitScanner()
    
    try:
        # Test server time
        result = scanner.session.get_server_time()
        if result.get('retCode') == 0:
            print("✅ Bybit API connection successful")
            print(f"   Server time: {result.get('result', {}).get('timeSecond')}")
        else:
            print(f"❌ API connection failed: {result.get('retMsg')}")
            return False
        
        # Test getting instruments
        instruments = scanner.get_perpetual_instruments()
        print(f"✅ Found {len(instruments)} perpetual instruments")
        
        if instruments:
            print("   Sample instruments:")
            for i, inst in enumerate(instruments[:3]):
                print(f"   {i+1}. {inst['symbol']} - {inst['contractType']}")
        
        # Test getting ticker data
        tickers = scanner.get_ticker_data()
        print(f"✅ Retrieved {len(tickers)} ticker data points")
        
        if tickers:
            print("   Sample tickers:")
            for i, ticker in enumerate(tickers[:3]):
                symbol = ticker['symbol']
                price = ticker['lastPrice']
                volume = ticker['volume24h']
                print(f"   {i+1}. {symbol}: ${price} (Vol: ${float(volume):,.0f})")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

async def test_telegram_bot():
    """Test Telegram bot functionality"""
    print("\n" + "="*50)
    print("📱 TESTING TELEGRAM BOT")
    print("="*50)
    
    if not config.TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not configured")
        return False
    
    if config.TELEGRAM_CHAT_ID == 'YOUR_CHAT_ID_HERE':
        print("❌ TELEGRAM_CHAT_ID not configured")
        print("   Please update your .env file with your actual chat ID")
        return False
    
    scanner = BybitScanner()
    
    try:
        test_message = """
🧪 <b>Scanner Test Message</b>

✅ Telegram bot is working correctly!
📊 This is a test from your Bybit Scanner
⏰ If you receive this, the bot is ready to send alerts

<i>Test completed successfully!</i>
        """.strip()
        
        success = await scanner.send_telegram_message(test_message)
        
        if success:
            print("✅ Telegram test message sent successfully")
            print(f"   Bot token: {config.TELEGRAM_BOT_TOKEN[:10]}...")
            print(f"   Chat ID: {config.TELEGRAM_CHAT_ID}")
            return True
        else:
            print("❌ Failed to send Telegram message")
            return False
            
    except Exception as e:
        print(f"❌ Telegram test failed: {e}")
        return False

async def test_scanning_logic():
    """Test the scanning and analysis logic"""
    print("\n" + "="*50)
    print("🔍 TESTING SCANNING LOGIC")
    print("="*50)
    
    scanner = BybitScanner()
    
    try:
        # Get some sample data
        tickers = scanner.get_ticker_data()
        if not tickers:
            print("❌ No ticker data available for testing")
            return False
        
        # Filter symbols that meet criteria
        valid_symbols = [ticker for ticker in tickers if scanner.should_scan_symbol(ticker)]
        print(f"✅ Found {len(valid_symbols)} symbols meeting scan criteria")
        
        if not valid_symbols:
            print("❌ No symbols meet the scanning criteria")
            print("   Consider lowering MIN_VOLUME_24H in your .env file")
            return False
        
        # Test analysis on a few symbols
        test_symbols = valid_symbols[:3]
        print(f"   Testing analysis on {len(test_symbols)} symbols:")
        
        for ticker in test_symbols:
            symbol = ticker['symbol']
            print(f"\n   📊 Analyzing {symbol}:")
            print(f"      Price: ${ticker['lastPrice']}")
            print(f"      24h Volume: ${float(ticker['volume24h']):,.0f}")
            print(f"      24h Change: {ticker['price24hPcnt']}%")
            
            # Test kline data retrieval
            klines = scanner.get_kline_data(symbol, "1", 20)
            if klines:
                print(f"      ✅ Retrieved {len(klines)} klines")
                
                # Test volatility analysis
                volatility_alert = scanner.analyze_volatility(symbol, klines)
                if volatility_alert:
                    print(f"      🚨 Volatility alert detected!")
                
                # Test breakout analysis
                current_price = float(ticker['lastPrice'])
                breakout_alert = scanner.analyze_breakout(symbol, klines, current_price)
                if breakout_alert:
                    print(f"      🚨 Breakout alert detected!")
            else:
                print(f"      ❌ No kline data available")
        
        print("\n✅ Scanning logic test completed")
        return True
        
    except Exception as e:
        print(f"❌ Scanning logic test failed: {e}")
        return False

async def test_configuration():
    """Test configuration settings"""
    print("\n" + "="*50)
    print("⚙️  TESTING CONFIGURATION")
    print("="*50)
    
    try:
        print(f"✅ Scan interval: {config.SCAN_INTERVAL_SECONDS} seconds")
        print(f"✅ Testnet mode: {config.BYBIT_TESTNET}")
        print(f"✅ Min 24h volume: ${config.MIN_VOLUME_24H:,.0f}")
        print(f"✅ Price range: ${config.MIN_PRICE} - ${config.MAX_PRICE}")
        print(f"✅ Volume spike threshold: {config.VOLUME_SPIKE_THRESHOLD}x")
        print(f"✅ Price pump threshold: {config.PRICE_PUMP_THRESHOLD}%")
        print(f"✅ Volatility threshold: {config.VOLATILITY_THRESHOLD}%")
        
        # Validate configuration
        config.validate()
        print("✅ Configuration validation passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def run_single_scan():
    """Run a single scan cycle to test everything together"""
    print("\n" + "="*50)
    print("🚀 RUNNING SINGLE SCAN TEST")
    print("="*50)
    
    scanner = BybitScanner()
    
    try:
        print("Starting scan...")
        await scanner.scan_symbols()
        print(f"✅ Scan completed successfully")
        print(f"   Alerts sent: {scanner.alerts_sent}")
        print(f"   Symbols tracked: {len(scanner.previous_data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Single scan test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 BYBIT SCANNER TEST SUITE")
    print("="*60)
    
    tests = [
        ("Configuration", test_configuration),
        ("API Connectivity", test_api_connectivity),
        ("Telegram Bot", test_telegram_bot),
        ("Scanning Logic", test_scanning_logic),
        ("Single Scan", run_single_scan)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔄 Running {test_name} test...")
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your scanner is ready for deployment.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues before deployment.")
    
    print("\n📝 Next steps:")
    print("1. Fix any failed tests")
    print("2. Update TELEGRAM_CHAT_ID in .env with your actual chat ID")
    print("3. Deploy to Render using the provided files")
    print("4. Monitor the /health endpoint after deployment")

if __name__ == "__main__":
    asyncio.run(main())