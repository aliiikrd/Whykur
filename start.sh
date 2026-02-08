#!/bin/bash

# =====================================================
# Telegram Stars Bot - Quick Start Script
# =====================================================

echo "⭐️ Starting Telegram Stars Bot..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python is installed"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed!"
    echo "Please install pip3"
    exit 1
fi

echo "✅ pip is installed"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Check for environment variables
if [ -z "$BOT_TOKEN" ]; then
    echo ""
    echo "⚠️  Warning: BOT_TOKEN environment variable is not set!"
    echo "Please set it using: export BOT_TOKEN='your_token'"
    echo ""
fi

if [ -z "$ADMIN_ID" ]; then
    echo "⚠️  Warning: ADMIN_ID environment variable is not set!"
    echo "Please set it using: export ADMIN_ID='your_id'"
    echo ""
fi

# Run the bot
echo ""
echo "🚀 Starting bot..."
echo "Press Ctrl+C to stop"
echo ""

python3 bot.py
