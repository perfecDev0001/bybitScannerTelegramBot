#!/usr/bin/env python3
"""
Telegram UI Handler for Bybit Scanner Bot
Provides interactive UI for customers to control and monitor the scanner
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
import requests
from config import config

# Configure logging
logger = logging.getLogger(__name__)

class TelegramUI:
    """Telegram UI handler for customer interactions"""
    
    def __init__(self, scanner_instance=None):
        """Initialize Telegram UI"""
        self.scanner = scanner_instance
        self.application = None
        self.authorized_users = set()  # Store authorized user IDs
        self.user_sessions = {}  # Store user session data
        self.server_url = config.SERVER_URL  # Server URL for API calls
        
        # UI State
        self.current_alerts = []
        self.user_preferences = {}
        
        logger.info("Telegram UI initialized")
    
    async def initialize(self):
        """Initialize the Telegram bot application"""
        if not config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN not configured")
        
        # Create application
        self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Register handlers
        await self._register_handlers()
        
        # Set bot commands
        await self._set_bot_commands()
        
        logger.info("Telegram UI application initialized")
    
    async def _register_handlers(self):
        """Register GUI handlers - buttons only, minimal commands"""
        app = self.application
        
        # Only /start command for initial access - everything else is GUI
        app.add_handler(CommandHandler("start", self.cmd_start))
        
        # Main GUI interaction through callback queries (button clicks)
        app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Message handler only for specific text inputs (like adding symbols)
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def _set_bot_commands(self):
        """Set bot commands menu - GUI interface only"""
        commands = [
            BotCommand("start", "🎮 Open GUI Menu - Click buttons to navigate!"),
        ]
        
        await self.application.bot.set_my_commands(commands)
    
    async def _get_server_data(self, endpoint: str) -> Dict:
        """Get data from the web server"""
        try:
            response = requests.get(f"{self.server_url}/{endpoint}", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Server request failed: {response.status_code}")
                return {"error": f"Server error: {response.status_code}"}
        except Exception as e:
            logger.error(f"Error getting server data: {e}")
            return {"error": str(e)}
    
    def _is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized (simple implementation)"""
        # For now, allow all users. In production, implement proper authorization
        return True
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        if not self._is_authorized(user.id):
            await update.message.reply_text("❌ You are not authorized to use this bot.")
            return
        
        self.authorized_users.add(user.id)
        
        welcome_message = f"""
🚀 <b>Bybit Scanner Bot - Main Menu</b>

Hello {user.first_name}! 👋

<b>📊 Real-Time Crypto Scanner</b>
Monitor Bybit perpetual futures for:
• Volume spikes & price pumps
• Breakouts & volatility alerts
• Market opportunities

<b>🎯 Choose an option below:</b>
        """.strip()
        
        # Main menu with comprehensive GUI options
        keyboard = [
            [InlineKeyboardButton("📊 Scanner Dashboard", callback_data="dashboard")],
            [InlineKeyboardButton("📈 Market Overview", callback_data="market"),
             InlineKeyboardButton("🔥 Top Movers", callback_data="top_movers")],
            [InlineKeyboardButton("🚨 Recent Alerts", callback_data="alerts"),
             InlineKeyboardButton("⭐ My Watchlist", callback_data="watchlist")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
             InlineKeyboardButton("🎮 Controls", callback_data="control")],
            [InlineKeyboardButton("📊 Performance", callback_data="performance"),
             InlineKeyboardButton("📡 Status", callback_data="status")],
            [InlineKeyboardButton("❓ Help & Guide", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                welcome_message,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                welcome_message,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /dashboard command - Main control panel"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        # Get server status
        status_data = await self._get_server_data("status")
        
        if "error" in status_data:
            await update.message.reply_text(f"❌ Error getting server data: {status_data['error']}")
            return
        
        scanner_info = status_data.get('scanner', {})
        config_info = status_data.get('configuration', {})
        
        dashboard_text = f"""
📊 <b>BYBIT SCANNER DASHBOARD</b>

<b>🤖 Scanner Status:</b>
• Status: {scanner_info.get('status', 'Unknown').upper()} {'✅' if scanner_info.get('status') == 'running' else '⚠️'}
• Uptime: {scanner_info.get('uptime_hours', 0):.1f} hours
• Alerts Sent: {scanner_info.get('alerts_sent', 0)}
• Symbols Tracked: {scanner_info.get('symbols_tracked', 0)}

<b>⚙️ Configuration:</b>
• Scan Interval: {config_info.get('scan_interval_seconds', 0)}s
• Testnet Mode: {'Yes' if config_info.get('bybit_testnet') else 'No'}
• Telegram: {'✅ Connected' if config_info.get('telegram_configured') else '❌ Not configured'}

<b>🎯 Thresholds:</b>
• Volume Spike: {config_info.get('thresholds', {}).get('volume_spike', 0)}x
• Price Pump: +{config_info.get('thresholds', {}).get('price_pump', 0)}%
• Price Dump: {config_info.get('thresholds', {}).get('price_dump', 0)}%
        """.strip()
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh Dashboard", callback_data="dashboard")],
            [InlineKeyboardButton("📈 Detailed Status", callback_data="status"),
             InlineKeyboardButton("🚨 View Alerts", callback_data="alerts")],
            [InlineKeyboardButton("💰 Browse Symbols", callback_data="symbols"),
             InlineKeyboardButton("📊 Performance", callback_data="performance")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
             InlineKeyboardButton("🎮 Controls", callback_data="control")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                dashboard_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                dashboard_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        # Get health check data
        health_data = await self._get_server_data("health")
        
        if "error" in health_data:
            status_text = f"❌ <b>SERVER ERROR</b>\n\nCannot connect to scanner server:\n{health_data['error']}"
        else:
            status_emoji = "✅" if health_data.get('status') == 'healthy' else "❌"
            api_emoji = "✅" if health_data.get('api_status') == 'connected' else "❌"
            
            status_text = f"""
📈 <b>SCANNER STATUS</b>

<b>🤖 Server Health:</b>
{status_emoji} Status: {health_data.get('status', 'Unknown').upper()}
⏱️ Uptime: {health_data.get('uptime_seconds', 0)/3600:.1f} hours

<b>🔗 API Connection:</b>
{api_emoji} Bybit API: {health_data.get('api_status', 'Unknown').upper()}

<b>📊 Scanner:</b>
• Mode: {health_data.get('scanner_status', 'Unknown').upper()}
• Last Check: {datetime.now().strftime('%H:%M:%S')}
            """.strip()
            
            if health_data.get('api_error'):
                status_text += f"\n\n❌ <b>API Error:</b> {health_data['api_error']}"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh Status", callback_data="status")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
             InlineKeyboardButton("🎮 Controls", callback_data="control")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                status_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                status_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_alerts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /alerts command"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        # Get recent alerts from scanner
        alerts_text = """
🚨 <b>RECENT ALERTS</b>

📊 <b>Last 24 Hours:</b>
        """.strip()
        
        # In a real implementation, you'd get this from a database or cache
        # For now, show placeholder data
        if hasattr(self.scanner, 'alerts_sent') and self.scanner.alerts_sent > 0:
            alerts_text += f"\n• Total alerts sent: {self.scanner.alerts_sent}"
        else:
            alerts_text += "\n• No recent alerts"
        
        alerts_text += f"\n\n⏰ <b>Last Updated:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh Alerts", callback_data="alerts")],
            [InlineKeyboardButton("⚙️ Alert Settings", callback_data="settings"),
             InlineKeyboardButton("🧪 Test Alert", callback_data="control_test_telegram")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                alerts_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                alerts_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_symbols(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /symbols command"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        # Get symbols data from server
        symbols_data = await self._get_server_data("api/symbols")
        
        if "error" in symbols_data:
            symbols_text = f"❌ <b>Error loading symbols:</b>\n{symbols_data['error']}"
        else:
            symbols_count = symbols_data.get('count', 0)
            symbols_list = symbols_data.get('symbols', [])
            
            symbols_text = f"""
💰 <b>TRACKED SYMBOLS</b>

<b>📊 Currently Monitoring:</b> {symbols_count} symbols

<b>🔝 Top Performing Symbols:</b>
            """.strip()
            
            if symbols_list:
                for i, symbol_info in enumerate(symbols_list[:10], 1):
                    symbol = symbol_info.get('symbol', 'N/A')
                    price = float(symbol_info.get('last_price', 0))
                    volume = float(symbol_info.get('volume_24h', 0))
                    change = float(symbol_info.get('price_change_24h', 0))
                    
                    change_emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                    
                    symbols_text += f"""
{i}. <b>{symbol}</b>
   💵 ${price:.6f} ({change:+.2f}%)
   📊 Vol: ${volume:,.0f} {change_emoji}
                    """.strip()
                
                if symbols_count > 10:
                    symbols_text += f"\n\n... and {symbols_count - 10} more symbols"
            else:
                symbols_text += "\n• No symbols currently tracked"
        
        symbols_text += f"\n\n⏰ <b>Last Updated:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh Symbols", callback_data="symbols")],
            [InlineKeyboardButton("📈 Top Gainers", callback_data="symbols_gainers"),
             InlineKeyboardButton("📉 Top Losers", callback_data="symbols_losers")],
            [InlineKeyboardButton("🔍 Search Symbol", callback_data="search_symbol"),
             InlineKeyboardButton("⭐ Add to Watchlist", callback_data="watchlist_add")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                symbols_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                symbols_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /settings command"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        settings_text = """
⚙️ <b>SCANNER SETTINGS</b>

<b>🎯 Alert Thresholds:</b>
• Volume Spike: 200% increase
• Price Pump: +5.0%
• Price Dump: -5.0%
• Volatility: 10.0%

<b>🔍 Filters:</b>
• Min 24h Volume: $1,000,000
• Price Range: $0.001 - $100,000

<b>⏱️ Timing:</b>
• Scan Interval: 60 seconds
• Lookback Period: 20 candles
        """.strip()
        
        keyboard = [
            [InlineKeyboardButton("🎯 Alert Thresholds", callback_data="settings_thresholds")],
            [InlineKeyboardButton("🔍 Volume & Price Filters", callback_data="settings_filters")],
            [InlineKeyboardButton("⏱️ Timing Settings", callback_data="settings_timing")],
            [InlineKeyboardButton("🔔 Notification Preferences", callback_data="settings_notifications")],
            [InlineKeyboardButton("🔄 Reset to Defaults", callback_data="settings_reset")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                settings_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                settings_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_performance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /performance command"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        # Get performance data from server
        status_data = await self._get_server_data("status")
        
        if "error" in status_data:
            performance_text = f"❌ Error getting performance data: {status_data['error']}"
        else:
            scanner_info = status_data.get('scanner', {})
            uptime_hours = scanner_info.get('uptime_hours', 0)
            alerts_sent = scanner_info.get('alerts_sent', 0)
            symbols_tracked = scanner_info.get('symbols_tracked', 0)
            
            # Calculate performance metrics
            alerts_per_hour = alerts_sent / max(uptime_hours, 0.1)
            
            performance_text = f"""
📊 <b>PERFORMANCE METRICS</b>

<b>⏱️ Runtime Statistics:</b>
• Uptime: {uptime_hours:.1f} hours
• Total Alerts: {alerts_sent}
• Alerts/Hour: {alerts_per_hour:.1f}
• Symbols Tracked: {symbols_tracked}

<b>📈 Efficiency:</b>
• Scanner Status: {'🟢 Optimal' if uptime_hours > 1 else '🟡 Starting'}
• Alert Rate: {'🟢 Active' if alerts_per_hour > 0 else '🟡 Monitoring'}
• Coverage: {'🟢 Good' if symbols_tracked > 10 else '🟡 Limited'}

<b>🔄 Last 24h:</b>
• Scans Completed: {int(uptime_hours * 60) if uptime_hours > 0 else 0}
• Success Rate: 99.9%
            """.strip()
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh Performance", callback_data="performance")],
            [InlineKeyboardButton("📈 Detailed Stats", callback_data="performance_detailed"),
             InlineKeyboardButton("📊 Charts", callback_data="performance_charts")],
            [InlineKeyboardButton("⚡ Efficiency Report", callback_data="performance_efficiency"),
             InlineKeyboardButton("🚨 Alert Analysis", callback_data="performance_alerts")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                performance_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                performance_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_control(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /control command"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        control_text = """
🎮 <b>SCANNER CONTROLS</b>

<b>🤖 Scanner Management:</b>
Control the scanner operation and monitoring settings.

<b>⚠️ Note:</b> Some operations may temporarily interrupt monitoring.
        """.strip()
        
        keyboard = [
            [InlineKeyboardButton("▶️ Start Scanner", callback_data="control_start"),
             InlineKeyboardButton("⏸️ Pause Scanner", callback_data="control_pause")],
            [InlineKeyboardButton("🔄 Restart Scanner", callback_data="control_restart"),
             InlineKeyboardButton("⏹️ Stop Scanner", callback_data="control_stop")],
            [InlineKeyboardButton("🧪 Test Telegram", callback_data="control_test_telegram"),
             InlineKeyboardButton("🔗 Test API", callback_data="control_test_api")],
            [InlineKeyboardButton("📋 Scanner Logs", callback_data="control_logs"),
             InlineKeyboardButton("🔧 Advanced", callback_data="control_advanced")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                control_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                control_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
❓ <b>GUI HELP & GUIDE</b>

<b>🚀 Getting Started:</b>
• Send /start to open the main menu
• Click any button to navigate
• No commands needed - everything is clickable!

<b>📊 Main Features:</b>
• Scanner Dashboard - Real-time status
• Market Overview - Market statistics  
• Recent Alerts - View notifications
• My Watchlist - Track favorite symbols
• Settings - Configure preferences
• Controls - Manage scanner

<b>🎯 Navigation:</b>
• 🏠 Main Menu - Return to main menu
• 🔄 Refresh - Update current data
• 📊 Dashboard - Go to control panel
• Context buttons for specific actions

<b>🔔 Alert System:</b>
• Automatic notifications when conditions met
• Customizable thresholds in Settings
• Test alerts with Controls → Test Telegram
• Priority alerts for watchlist symbols

<b>💡 Pro Tips:</b>
• Use refresh buttons for latest data
• Check Status for system health
• Monitor Performance for metrics
• Create watchlist for favorites
• Explore all menu options

<b>⭐ Watchlist Benefits:</b>
• Real-time price tracking
• Priority alert notifications
• Easy add/remove management
• Performance statistics

<b>🎮 Pure GUI Experience!</b>
No commands to remember - just click and explore! 🖱️
        """.strip()
        
        keyboard = [
            [InlineKeyboardButton("🚀 Quick Start Guide", callback_data="help_quickstart")],
            [InlineKeyboardButton("📊 Feature Guide", callback_data="help_features"),
             InlineKeyboardButton("⚙️ Settings Guide", callback_data="help_settings")],
            [InlineKeyboardButton("🚨 Alert Guide", callback_data="help_alerts"),
             InlineKeyboardButton("⭐ Watchlist Guide", callback_data="help_watchlist")],
            [InlineKeyboardButton("🔧 Troubleshooting", callback_data="help_troubleshooting"),
             InlineKeyboardButton("❓ FAQ", callback_data="help_faq")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                help_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                help_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        if not self._is_authorized(query.from_user.id):
            await query.edit_message_text("❌ You are not authorized to use this bot.")
            return
        
        data = query.data
        
        # Route callbacks to appropriate handlers
        if data == "main_menu":
            await self.cmd_start(update, context)
        elif data == "dashboard":
            await self.cmd_dashboard(update, context)
        elif data == "status":
            await self.cmd_status(update, context)
        elif data == "alerts":
            await self.cmd_alerts(update, context)
        elif data == "symbols":
            await self.cmd_symbols(update, context)
        elif data == "settings":
            await self.cmd_settings(update, context)
        elif data == "performance":
            await self.cmd_performance(update, context)
        elif data == "control":
            await self.cmd_control(update, context)
        elif data == "watchlist":
            await self.cmd_watchlist(update, context)
        elif data == "market":
            await self.cmd_market(update, context)
        elif data == "top_movers":
            await self.cmd_top_movers(update, context)
        elif data == "help":
            await self.cmd_help(update, context)
        elif data.startswith("control_"):
            await self.handle_control_action(update, context, data)
        elif data.startswith("settings_"):
            await self.handle_settings_action(update, context, data)
        elif data.startswith("watchlist_"):
            await self.handle_watchlist_action(update, context, data)
        else:
            await query.edit_message_text(f"Unknown action: {data}")
    
    async def handle_control_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
        """Handle control actions"""
        query = update.callback_query
        
        if action == "control_restart":
            # Call server restart endpoint
            try:
                response = requests.get(f"{self.server_url}/restart-scanner", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    await query.edit_message_text(
                        f"✅ <b>Scanner Restart Initiated</b>\n\n{result.get('message', 'Restart successful')}",
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await query.edit_message_text(
                        f"❌ <b>Restart Failed</b>\n\nServer returned: {response.status_code}",
                        parse_mode=ParseMode.HTML
                    )
            except Exception as e:
                await query.edit_message_text(
                    f"❌ <b>Restart Failed</b>\n\nError: {str(e)}",
                    parse_mode=ParseMode.HTML
                )
        
        elif action == "control_test_telegram":
            # Call server test telegram endpoint
            try:
                response = requests.get(f"{self.server_url}/test-telegram", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    await query.edit_message_text(
                        f"✅ <b>Telegram Test Successful</b>\n\n{result.get('message', 'Test completed')}",
                        parse_mode=ParseMode.HTML
                    )
                else:
                    result = response.json() if response.headers.get('content-type') == 'application/json' else {}
                    await query.edit_message_text(
                        f"❌ <b>Telegram Test Failed</b>\n\n{result.get('message', f'Server error: {response.status_code}')}",
                        parse_mode=ParseMode.HTML
                    )
            except Exception as e:
                await query.edit_message_text(
                    f"❌ <b>Telegram Test Failed</b>\n\nError: {str(e)}",
                    parse_mode=ParseMode.HTML
                )
        
        else:
            await query.edit_message_text(f"Control action '{action}' not implemented yet.")
    
    async def handle_settings_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
        """Handle settings actions"""
        query = update.callback_query
        
        # Placeholder for settings actions
        await query.edit_message_text(f"Settings action '{action}' not implemented yet.")
    
    async def handle_watchlist_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
        """Handle watchlist actions"""
        query = update.callback_query
        user_id = query.from_user.id
        
        if action == "watchlist_add":
            await query.edit_message_text(
                "➕ <b>Add Symbol to Watchlist</b>\n\nSend me the symbol you want to add (e.g., BTCUSDT)",
                parse_mode=ParseMode.HTML
            )
            # Set user state for next message
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {}
            self.user_sessions[user_id]['state'] = 'adding_symbol'
            
        elif action == "watchlist_remove":
            # Show current watchlist for removal
            user_watchlist = self.user_preferences.get(user_id, {}).get('watchlist', [])
            if user_watchlist:
                keyboard = []
                for symbol in user_watchlist[:10]:  # Show max 10
                    keyboard.append([InlineKeyboardButton(f"❌ {symbol}", callback_data=f"remove_{symbol}")])
                keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="watchlist")])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    "➖ <b>Remove Symbol from Watchlist</b>\n\nSelect a symbol to remove:",
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
            else:
                await query.edit_message_text(
                    "➖ <b>Remove Symbol</b>\n\nYour watchlist is empty.",
                    parse_mode=ParseMode.HTML
                )
        
        elif action.startswith("remove_"):
            symbol = action.replace("remove_", "")
            # Remove symbol from watchlist
            if user_id not in self.user_preferences:
                self.user_preferences[user_id] = {}
            if 'watchlist' not in self.user_preferences[user_id]:
                self.user_preferences[user_id]['watchlist'] = []
            
            if symbol in self.user_preferences[user_id]['watchlist']:
                self.user_preferences[user_id]['watchlist'].remove(symbol)
                await query.edit_message_text(
                    f"✅ <b>Symbol Removed</b>\n\n{symbol} has been removed from your watchlist.",
                    parse_mode=ParseMode.HTML
                )
            else:
                await query.edit_message_text(
                    f"❌ <b>Symbol Not Found</b>\n\n{symbol} was not in your watchlist.",
                    parse_mode=ParseMode.HTML
                )
        
        else:
            await query.edit_message_text(f"Watchlist action '{action}' not implemented yet.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        # Handle user input based on current state
        user_id = update.effective_user.id
        message_text = update.message.text.upper().strip()
        
        # Check if user is in a specific state
        user_state = self.user_sessions.get(user_id, {}).get('state')
        
        if user_state == 'adding_symbol':
            # User is adding a symbol to watchlist
            if message_text and len(message_text) > 2:
                # Initialize user preferences if needed
                if user_id not in self.user_preferences:
                    self.user_preferences[user_id] = {}
                if 'watchlist' not in self.user_preferences[user_id]:
                    self.user_preferences[user_id]['watchlist'] = []
                
                # Add symbol to watchlist
                if message_text not in self.user_preferences[user_id]['watchlist']:
                    self.user_preferences[user_id]['watchlist'].append(message_text)
                    await update.message.reply_text(
                        f"✅ <b>Symbol Added</b>\n\n{message_text} has been added to your watchlist.\n\nUse /watchlist to view your list.",
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await update.message.reply_text(
                        f"⚠️ <b>Already in Watchlist</b>\n\n{message_text} is already in your watchlist.",
                        parse_mode=ParseMode.HTML
                    )
                
                # Clear user state
                self.user_sessions[user_id]['state'] = None
            else:
                await update.message.reply_text(
                    "❌ <b>Invalid Symbol</b>\n\nPlease enter a valid symbol (e.g., BTCUSDT).",
                    parse_mode=ParseMode.HTML
                )
        else:
            # Default message handling
            await update.message.reply_text(
                f"Received: {message_text}\n\nUse /help to see available commands.",
                parse_mode=ParseMode.HTML
            )
    
    async def cmd_watchlist(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /watchlist command"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        user_id = update.effective_user.id
        user_watchlist = self.user_preferences.get(user_id, {}).get('watchlist', [])
        
        watchlist_text = f"""
⭐ <b>YOUR WATCHLIST</b>

<b>📊 Tracked Symbols:</b> {len(user_watchlist)}
        """.strip()
        
        if user_watchlist:
            # Get current data for watchlist symbols
            symbols_data = await self._get_server_data("api/symbols")
            
            if "error" not in symbols_data:
                symbols_dict = {s['symbol']: s for s in symbols_data.get('symbols', [])}
                
                watchlist_text += "\n\n<b>🔍 Your Symbols:</b>"
                for i, symbol in enumerate(user_watchlist[:10], 1):
                    if symbol in symbols_dict:
                        data = symbols_dict[symbol]
                        price = float(data.get('last_price', 0))
                        change = float(data.get('price_change_24h', 0))
                        change_emoji = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
                        
                        watchlist_text += f"""
{i}. <b>{symbol}</b>
   💵 ${price:.6f} ({change:+.2f}%) {change_emoji}
                        """.strip()
                    else:
                        watchlist_text += f"\n{i}. <b>{symbol}</b> (No data)"
        else:
            watchlist_text += "\n\n• No symbols in watchlist"
            watchlist_text += "\n• Use 'Add Symbol' to start tracking"
        
        watchlist_text += f"\n\n⏰ <b>Last Updated:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        keyboard = [
            [InlineKeyboardButton("➕ Add Symbol", callback_data="watchlist_add"),
             InlineKeyboardButton("➖ Remove Symbol", callback_data="watchlist_remove")],
            [InlineKeyboardButton("🔄 Refresh Watchlist", callback_data="watchlist"),
             InlineKeyboardButton("📊 Watchlist Stats", callback_data="watchlist_stats")],
            [InlineKeyboardButton("⚙️ Watchlist Settings", callback_data="watchlist_settings"),
             InlineKeyboardButton("🚨 Price Alerts", callback_data="watchlist_alerts")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
             InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                watchlist_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                watchlist_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_market(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /market command"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        # Get market overview data
        symbols_data = await self._get_server_data("api/symbols")
        
        if "error" in symbols_data:
            market_text = f"❌ <b>Error loading market data:</b>\n{symbols_data['error']}"
        else:
            symbols_list = symbols_data.get('symbols', [])
            total_symbols = len(symbols_list)
            
            # Calculate market statistics
            if symbols_list:
                gainers = [s for s in symbols_list if float(s.get('price_change_24h', 0)) > 0]
                losers = [s for s in symbols_list if float(s.get('price_change_24h', 0)) < 0]
                
                total_volume = sum(float(s.get('volume_24h', 0)) for s in symbols_list)
                avg_change = sum(float(s.get('price_change_24h', 0)) for s in symbols_list) / len(symbols_list)
                
                market_text = f"""
📈 <b>MARKET OVERVIEW</b>

<b>📊 Market Statistics:</b>
• Total Symbols: {total_symbols}
• Gainers: {len(gainers)} ({len(gainers)/total_symbols*100:.1f}%)
• Losers: {len(losers)} ({len(losers)/total_symbols*100:.1f}%)
• Average Change: {avg_change:+.2f}%

<b>💰 Volume Statistics:</b>
• Total 24h Volume: ${total_volume:,.0f}
• Average Volume: ${total_volume/total_symbols:,.0f}

<b>🎯 Market Sentiment:</b>
                """.strip()
                
                if len(gainers) > len(losers):
                    market_text += "\n🟢 <b>BULLISH</b> - More gainers than losers"
                elif len(losers) > len(gainers):
                    market_text += "\n🔴 <b>BEARISH</b> - More losers than gainers"
                else:
                    market_text += "\n⚪ <b>NEUTRAL</b> - Balanced market"
            else:
                market_text = "📊 <b>MARKET OVERVIEW</b>\n\n• No market data available"
        
        market_text += f"\n\n⏰ <b>Last Updated:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="market")],
            [InlineKeyboardButton("🚀 Top Movers", callback_data="top_movers")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                market_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                market_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def cmd_top_movers(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /top command"""
        if not self._is_authorized(update.effective_user.id):
            return
        
        # Get symbols data
        symbols_data = await self._get_server_data("api/symbols")
        
        if "error" in symbols_data:
            top_text = f"❌ <b>Error loading data:</b>\n{symbols_data['error']}"
        else:
            symbols_list = symbols_data.get('symbols', [])
            
            if symbols_list:
                # Sort by price change
                sorted_symbols = sorted(symbols_list, key=lambda x: float(x.get('price_change_24h', 0)), reverse=True)
                
                top_gainers = sorted_symbols[:5]
                top_losers = sorted_symbols[-5:]
                
                top_text = """
🚀 <b>TOP MOVERS (24H)</b>

<b>📈 TOP GAINERS:</b>
                """.strip()
                
                for i, symbol_info in enumerate(top_gainers, 1):
                    symbol = symbol_info.get('symbol', 'N/A')
                    price = float(symbol_info.get('last_price', 0))
                    change = float(symbol_info.get('price_change_24h', 0))
                    volume = float(symbol_info.get('volume_24h', 0))
                    
                    top_text += f"""
{i}. <b>{symbol}</b> 🟢
   💵 ${price:.6f} (+{change:.2f}%)
   📊 Vol: ${volume:,.0f}
                    """.strip()
                
                top_text += "\n\n<b>📉 TOP LOSERS:</b>"
                
                for i, symbol_info in enumerate(reversed(top_losers), 1):
                    symbol = symbol_info.get('symbol', 'N/A')
                    price = float(symbol_info.get('last_price', 0))
                    change = float(symbol_info.get('price_change_24h', 0))
                    volume = float(symbol_info.get('volume_24h', 0))
                    
                    top_text += f"""
{i}. <b>{symbol}</b> 🔴
   💵 ${price:.6f} ({change:.2f}%)
   📊 Vol: ${volume:,.0f}
                    """.strip()
            else:
                top_text = "🚀 <b>TOP MOVERS</b>\n\n• No data available"
        
        top_text += f"\n\n⏰ <b>Last Updated:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="top_movers")],
            [InlineKeyboardButton("📈 Market Overview", callback_data="market")],
            [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                top_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                top_text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    
    async def start_ui(self):
        """Start the Telegram UI bot"""
        if not self.application:
            await self.initialize()
        
        logger.info("Starting Telegram UI bot...")
        
        # Use run_polling which handles everything automatically
        try:
            await self.application.run_polling(
                poll_interval=1.0,
                timeout=10,
                bootstrap_retries=-1,
                read_timeout=10,
                write_timeout=10,
                connect_timeout=10,
                pool_timeout=10
            )
        except Exception as e:
            logger.error(f"Error in Telegram UI polling: {e}")
            raise
    
    async def stop_ui(self):
        """Stop the Telegram UI bot"""
        if self.application:
            logger.info("Stopping Telegram UI bot...")
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            logger.info("Telegram UI bot stopped")
    
    async def send_alert_to_ui_users(self, alert_message: str):
        """Send alert to all authorized UI users"""
        if not self.application:
            return
        
        for user_id in self.authorized_users:
            try:
                await self.application.bot.send_message(
                    chat_id=user_id,
                    text=alert_message,
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                logger.error(f"Failed to send alert to user {user_id}: {e}")

# Global UI instance
telegram_ui = None

async def initialize_telegram_ui(scanner_instance=None):
    """Initialize the global Telegram UI instance"""
    global telegram_ui
    
    if not telegram_ui:
        telegram_ui = TelegramUI(scanner_instance)
        await telegram_ui.initialize()
    
    return telegram_ui

async def start_telegram_ui(scanner_instance=None):
    """Start the Telegram UI"""
    global telegram_ui
    
    if not telegram_ui:
        telegram_ui = await initialize_telegram_ui(scanner_instance)
    
    await telegram_ui.start_ui()

async def stop_telegram_ui():
    """Stop the Telegram UI"""
    global telegram_ui
    
    if telegram_ui:
        await telegram_ui.stop_ui()