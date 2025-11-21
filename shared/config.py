"""
Shared configuration for all revenue projects
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "revenue_portfolio")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    
    # APIs
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
    ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")  # GPT-4
    
    # Affiliate IDs
    BINANCE_AFFILIATE_ID = os.getenv("BINANCE_AFFILIATE_ID", "")
    COINBASE_AFFILIATE_ID = os.getenv("COINBASE_AFFILIATE_ID", "")
    KRAKEN_AFFILIATE_ID = os.getenv("KRAKEN_AFFILIATE_ID", "")
    
    # Monitoring
    WEBHOOK_ALERT_URL = os.getenv("WEBHOOK_ALERT_URL", "")  # Telegram/Slack
    OWNER_EMAIL = os.getenv("OWNER_EMAIL", "")
    
    # GCP (if using)
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")
    GCP_VM_NAME = os.getenv("GCP_VM_NAME", "cervello-contabilita")
    GCP_ZONE = os.getenv("GCP_ZONE", "us-central1-c")
