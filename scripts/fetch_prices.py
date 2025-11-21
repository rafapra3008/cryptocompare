"""
Fetch latest crypto prices and store in database
Runs every hour via cron
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from shared.db import db
from shared.api_coingecko import coingecko
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_store_prices():
    """Fetch prices for all tracked assets"""
    
    # Get all assets from database
    assets = db.execute_query(
        "SELECT id, symbol, coingecko_id FROM assets WHERE coingecko_id IS NOT NULL",
        fetch=True
    )
    
    if not assets:
        logger.warning("No assets found in database")
        return
    
    logger.info(f"Fetching prices for {len(assets)} assets...")
    
    success_count = 0
    error_count = 0
    
    for asset in assets:
        try:
            # Fetch comprehensive data
            data = coingecko.get_coin_data(asset['coingecko_id'])
            
            if not data or 'price_usd' not in data:
                logger.warning(f"No data for {asset['symbol']}")
                error_count += 1
                continue
            
            # Store in database
            db.insert_price(
                asset_id=asset['id'],
                price=data['price_usd'],
                volume=data.get('volume_24h_usd'),
                market_cap=data.get('market_cap_usd'),
                source='coingecko'
            )
            
            logger.info(f"✅ {asset['symbol']}: ${data['price_usd']:,.2f}")
            success_count += 1
            
        except Exception as e:
            logger.error(f"❌ Error fetching {asset['symbol']}: {e}")
            error_count += 1
    
    logger.info(f"\n📊 Summary: {success_count} success, {error_count} errors")
    
    # Log to analytics
    db.execute_query(
        """
        INSERT INTO analytics_daily (date, project, pageviews)
        VALUES (CURRENT_DATE, 'system', 1)
        ON CONFLICT (date, project) DO NOTHING
        """
    )

def main():
    logger.info("🔄 Starting price fetch job...")
    logger.info(f"Time: {datetime.now().isoformat()}")
    
    try:
        fetch_and_store_prices()
        logger.info("✅ Price fetch complete!")
    except Exception as e:
        logger.error(f"❌ Price fetch failed: {e}")
        raise

if __name__ == "__main__":
    main()
