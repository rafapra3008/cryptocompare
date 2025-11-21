#!/bin/bash
# Quick setup script for revenue portfolio

set -e  # Exit on error

echo "🚀 Revenue Portfolio - Quick Setup"
echo "===================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install postgresql@15
    else
        echo "❌ Please install PostgreSQL manually"
        exit 1
    fi
fi

echo "✅ PostgreSQL found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Check .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your API keys!"
    echo "   Required: OPENROUTER_API_KEY (for GPT-4)"
    echo "   Optional: COINGECKO_API_KEY, affiliate IDs"
fi

# Database setup
echo ""
echo "🗄️  Database Setup"
echo "=================="
read -p "Database host (default: localhost): " DB_HOST
DB_HOST=${DB_HOST:-localhost}

read -p "Database user (default: postgres): " DB_USER
DB_USER=${DB_USER:-postgres}

read -p "Database name (default: revenue_portfolio): " DB_NAME
DB_NAME=${DB_NAME:-revenue_portfolio}

echo ""
echo "Creating database..."

# Check if database exists
if psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "⚠️  Database '$DB_NAME' already exists."
    read -p "Drop and recreate? (y/N): " confirm
    if [[ $confirm == [yY] ]]; then
        psql -U $DB_USER -c "DROP DATABASE $DB_NAME;"
        psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;"
        echo "✅ Database recreated"
    fi
else
    psql -U $DB_USER -c "CREATE DATABASE $DB_NAME;"
    echo "✅ Database created"
fi

# Load schema
echo "Loading schema..."
psql -U $DB_USER $DB_NAME < shared/schema.sql
echo "✅ Schema loaded"

# Seed data
echo "Seeding initial data..."
python3 scripts/seed_db.py
echo "✅ Data seeded"

# Install Hugo (for static sites)
if ! command -v hugo &> /dev/null; then
    echo "📦 Installing Hugo..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install hugo
        echo "✅ Hugo installed"
    else
        echo "⚠️  Hugo not found. Please install manually: https://gohugo.io/installation/"
    fi
else
    echo "✅ Hugo found: $(hugo version)"
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Sign up for affiliate programs:"
echo "   - Binance: https://www.binance.com/en/activity/affiliate"
echo "   - Coinbase: https://www.coinbase.com/affiliates"
echo "   - Kraken: https://support.kraken.com/hc/en-us/articles/360027545252"
echo "3. Buy domain: cryptoexchange-compare.com"
echo "4. Run: python3 model_c_comparison/generate_content.py"
echo ""
echo "📖 See DAILY_TASKS.md for today's checklist"
echo ""
