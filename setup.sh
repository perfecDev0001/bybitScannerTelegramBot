#!/bin/bash
# Setup script for Bybit Scanner Telegram Bot

echo "🚀 Setting up Bybit Scanner Telegram Bot..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy example env file if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your Telegram bot token and chat ID"
fi

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your Telegram bot token and chat ID"
echo "2. Run: source venv/bin/activate"
echo "3. Test: python test_telegram_ui.py"
echo "4. Start: python app.py"
echo ""
echo "🤖 Telegram Commands:"
echo "- /start - Welcome message"
echo "- /dashboard - Main control panel"
echo "- /status - Scanner status"
echo "- /help - Help and commands"