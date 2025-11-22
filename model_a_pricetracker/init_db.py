import os
import psycopg2
from urllib.parse import urlparse

# Database URL provided by user
DB_URL = "postgresql://postgres:YMdwlThHJTlWwnagTpEgtXWMrAHNDBqp@shortline.proxy.rlwy.net:54760/railway"

SCHEMA_SQL = """
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS exchanges;

CREATE TABLE exchanges (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(255) NOT NULL,
    affiliate_link VARCHAR(255)
);

CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    coin_symbol VARCHAR(10) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    exchange_id VARCHAR(50) REFERENCES exchanges(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SEED_SQL = """
INSERT INTO exchanges (id, name, url, affiliate_link) VALUES 
('binance', 'Binance', 'https://binance.com', 'https://accounts.binance.com/register?ref=CPA_004NMYS76M'),
('kraken', 'Kraken', 'https://kraken.com', 'https://r.kraken.com/dd549f99'),
('coinbase', 'Coinbase', 'https://coinbase.com', 'https://coinbase.com/join/PENDING'),
('crypto_com', 'Crypto.com', 'https://crypto.com', NULL);
"""

def init_db():
    print("🔌 Connecting to Railway Database...")
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("📝 Running Schema...")
        cur.execute(SCHEMA_SQL)
        
        print("🌱 Seeding Data...")
        cur.execute(SEED_SQL)
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database Initialized Successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    init_db()
