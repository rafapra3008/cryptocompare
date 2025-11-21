#!/bin/bash
# Daily automation cron jobs for revenue portfolio

set -e

PROJECT_ROOT="/Users/rafapra/.gemini/antigravity/scratch/revenue_portfolio"
cd $PROJECT_ROOT

# Activate venv
source venv/bin/activate

# Timestamp
echo "==================================="
echo "Daily Revenue Jobs - $(date)"
echo "==================================="

# 1. Fetch latest crypto prices (every hour)
echo "📊 Fetching latest prices..."
python3 scripts/fetch_prices.py

# 2. Generate new SEO pages if keyword queue exists (daily at 2am)
if [ -f "model_a_seo/keyword_queue.csv" ]; then
    echo "📝 Generating new SEO pages..."
    python3 model_a_seo/generate_batch.py --batch-size 20
fi

# 3. Build and deploy Model C site (if changes detected)
if [ -d "model_c_comparison/generated" ]; then
    echo "🚀 Building Model C site..."
    python3 model_c_comparison/build_site.py
fi

# 4. Aggregate analytics (daily at 3am)
echo "📊 Aggregating analytics..."
python3 scripts/aggregate_analytics.py

# 5. Send daily report via email
echo "📧 Sending daily report..."
python3 scripts/send_daily_report.py

# 6. Health check - verify all services running
echo "🏥 Health check..."
python3 scripts/health_check.py

echo "✅ Daily automation complete!"
echo "==================================="
