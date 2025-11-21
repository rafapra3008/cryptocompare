"""
Daily health check and monitoring
Sends alerts if something is wrong
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from shared.db import db
from shared.config import Config
import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    """Check if database is responsive"""
    try:
        result = db.execute_query("SELECT NOW()", fetch=True)
        logger.info("✅ Database: OK")
        return True
    except Exception as e:
        logger.error(f"❌ Database: FAILED - {e}")
        return False

def check_recent_prices():
    """Check if prices were updated recently"""
    try:
        result = db.execute_query(
            """
            SELECT MAX(created_at) as last_update
            FROM prices
            """,
            fetch=True
        )
        
        if not result or not result[0]['last_update']:
            logger.warning("⚠️  No prices in database")
            return False
        
        last_update = result[0]['last_update']
        age = datetime.now() - last_update
        
        if age > timedelta(hours=2):
            logger.warning(f"⚠️  Prices stale (last update: {age} ago)")
            return False
        
        logger.info(f"✅ Prices: OK (updated {age} ago)")
        return True
        
    except Exception as e:
        logger.error(f"❌ Price check failed: {e}")
        return False

def check_pages_indexed():
    """Check Google indexing status"""
    try:
        result = db.execute_query(
            """
            SELECT COUNT(*) as total,
                   COUNT(indexed_at) as indexed
            FROM pages_seo
            WHERE status = 'published'
            """,
            fetch=True
        )
        
        total = result[0]['total']
        indexed = result[0]['indexed']
        
        if total == 0:
            logger.warning("⚠️  No published pages")
            return False
        
        percentage = (indexed / total * 100) if total > 0 else 0
        
        logger.info(f"📊 Pages: {indexed}/{total} indexed ({percentage:.1f}%)")
        
        if percentage < 5 and total > 20:
            logger.warning("⚠️  Low indexing rate")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Pages check failed: {e}")
        return False

def check_revenue():
    """Check if revenue is being tracked"""
    try:
        result = db.execute_query(
            """
            SELECT SUM(total_revenue) as total
            FROM analytics_daily
            WHERE date >= CURRENT_DATE - INTERVAL '7 days'
            """,
            fetch=True
        )
        
        total = result[0]['total'] or 0
        
        logger.info(f"💰 Revenue (7d): €{total:.2f}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Revenue check failed: {e}")
        return False

def send_alert(message):
    """Send alert via webhook (Telegram/Slack)"""
    if not Config.WEBHOOK_ALERT_URL:
        logger.info("No webhook configured, skipping alert")
        return
    
    try:
        requests.post(
            Config.WEBHOOK_ALERT_URL,
            json={"text": f"🚨 Revenue Portfolio Alert:\n{message}"},
            timeout=10
        )
        logger.info("✅ Alert sent")
    except Exception as e:
        logger.error(f"❌ Failed to send alert: {e}")

def main():
    logger.info("🏥 Running health checks...")
    logger.info(f"Time: {datetime.now().isoformat()}")
    logger.info("=" * 60)
    
    checks = {
        "Database": check_database(),
        "Recent Prices": check_recent_prices(),
        "Pages Indexed": check_pages_indexed(),
        "Revenue Tracking": check_revenue()
    }
    
    logger.info("=" * 60)
    
    failed = [name for name, passed in checks.items() if not passed]
    
    if failed:
        logger.warning(f"⚠️  {len(failed)} checks failed: {', '.join(failed)}")
        send_alert(f"Health check failures: {', '.join(failed)}")
    else:
        logger.info("✅ All health checks passed!")
    
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
