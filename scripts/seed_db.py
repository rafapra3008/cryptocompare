"""
Seed database with initial data
Run this after creating schema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from shared.db import db
from shared.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_assets():
    """Seed top crypto assets"""
    assets = [
        # Top cryptocurrencies
        ("BTC", "Bitcoin", "crypto", "bitcoin"),
        ("ETH", "Ethereum", "crypto", "ethereum"),
        ("BNB", "Binance Coin", "crypto", "binancecoin"),
        ("XRP", "Ripple", "crypto", "ripple"),
        ("SOL", "Solana", "crypto", "solana"),
        ("ADA", "Cardano", "crypto", "cardano"),
        ("DOGE", "Dogecoin", "crypto", "dogecoin"),
        ("MATIC", "Polygon", "crypto", "matic-network"),
        ("DOT", "Polkadot", "crypto", "polkadot"),
        ("AVAX", "Avalanche", "crypto", "avalanche-2"),
        ("SHIB", "Shiba Inu", "crypto", "shiba-inu"),
        ("UNI", "Uniswap", "crypto", "uniswap"),
        ("LINK", "Chainlink", "crypto", "chainlink"),
        ("ATOM", "Cosmos", "crypto", "cosmos"),
        ("LTC", "Litecoin", "crypto", "litecoin"),
    ]
    
    logger.info("Seeding assets...")
    for symbol, name, asset_type, coingecko_id in assets:
        try:
            asset_id = db.insert_asset(symbol, name, asset_type, coingecko_id)
            if asset_id:
                logger.info(f"✅ Inserted: {symbol} - {name}")
        except Exception as e:
            logger.error(f"❌ Error inserting {symbol}: {e}")

def seed_exchanges():
    """Seed major crypto exchanges for Model C"""
    exchanges = [
        # (name, logo_url, affiliate_url, affiliate_id, trading_fee, rating)
        (
            "Binance",
            "https://example.com/binance-logo.png",
            f"https://accounts.binance.com/register?ref={Config.BINANCE_AFFILIATE_ID}",
            Config.BINANCE_AFFILIATE_ID,
            0.001,  # 0.1%
            4.5
        ),
        (
            "Coinbase",
            "https://example.com/coinbase-logo.png",
            f"https://www.coinbase.com/join/{Config.COINBASE_AFFILIATE_ID}",
            Config.COINBASE_AFFILIATE_ID,
            0.0149,  # 1.49%
            4.3
        ),
        (
            "Kraken",
            "https://example.com/kraken-logo.png",
            f"https://www.kraken.com/?ref={Config.KRAKEN_AFFILIATE_ID}",
            Config.KRAKEN_AFFILIATE_ID,
            0.0016,  # 0.16%
            4.4
        ),
        (
            "Crypto.com",
            "https://example.com/cryptocom-logo.png",
            "https://crypto.com/app/referral",  # Add real affiliate link
            "YOUR_CRYPTOCOM_ID",
            0.004,  # 0.4%
            4.2
        ),
        (
            "KuCoin",
            "https://example.com/kucoin-logo.png",
            "https://www.kucoin.com/r/referral",  # Add real affiliate link
            "YOUR_KUCOIN_ID",
            0.001,  # 0.1%
            4.1
        ),
        (
            "Bitpanda",
            "https://example.com/bitpanda-logo.png",
            "https://www.bitpanda.com/referral",  # Add real affiliate link
            "YOUR_BITPANDA_ID",
            0.0149,  # 1.49%
            4.0
        ),
    ]
    
    logger.info("Seeding exchanges...")
    for exchange_data in exchanges:
        try:
            exchange_id = db.insert_exchange(*exchange_data)
            if exchange_id:
                logger.info(f"✅ Inserted: {exchange_data[0]}")
        except Exception as e:
            logger.error(f"❌ Error inserting {exchange_data[0]}: {e}")

def main():
    logger.info("🌱 Starting database seeding...")
    
    seed_assets()
    seed_exchanges()
    
    logger.info("✅ Database seeding complete!")
    
    # Verify
    logger.info("\n📊 Current database state:")
    
    assets = db.execute_query("SELECT COUNT(*) as count FROM assets", fetch=True)
    logger.info(f"Assets: {assets[0]['count']}")
    
    exchanges = db.execute_query("SELECT COUNT(*) as count FROM exchanges", fetch=True)
    logger.info(f"Exchanges: {exchanges[0]['count']}")

if __name__ == "__main__":
    main()
