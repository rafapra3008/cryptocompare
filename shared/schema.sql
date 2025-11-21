"""
PostgreSQL Database Schema for Revenue Portfolio
Shared across all 5 projects
"""

-- ============================================
-- SHARED TABLES (used by multiple projects)
-- ============================================

-- Assets (cryptocurrencies, stocks)
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,  -- BTC, ETH, TSLA
    name VARCHAR(100),
    type VARCHAR(20),  -- crypto, stock, commodity
    coingecko_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_assets_symbol ON assets(symbol);

-- Prices (time-series data)
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    asset_id INT REFERENCES assets(id),
    price DECIMAL(20,8) NOT NULL,
    volume DECIMAL(20,2),
    market_cap DECIMAL(20,2),
    source VARCHAR(50),  -- coingecko, alphavantage, binance
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_prices_asset_time ON prices(asset_id, timestamp DESC);

-- News articles (for sentiment analysis)
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT UNIQUE,
    summary TEXT,
    published_at TIMESTAMP,
    sentiment_score DECIMAL(3,2),  -- -1.0 to 1.0 (VADER)
    source VARCHAR(100),  -- coindesk, cryptoslate, etc
    asset_ids INT[],  -- Array of related asset IDs
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_news_published ON news(published_at DESC);
CREATE INDEX idx_news_sentiment ON news(sentiment_score);

-- ============================================
-- MODEL A: SEO PROGRAMMATIC (PriceIntel)
-- ============================================

-- Generated pages
CREATE TABLE pages_seo (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(200) UNIQUE NOT NULL,  -- btc-usd-price-live
    title VARCHAR(200),
    meta_description TEXT,
    content TEXT,  -- Full HTML
    template VARCHAR(50),  -- price_page, trend_page, comparison
    asset_id INT REFERENCES assets(id),
    keyword VARCHAR(200),  -- Target SEO keyword
    search_volume INT,  -- Monthly searches
    keyword_difficulty INT,  -- 0-100
    status VARCHAR(20) DEFAULT 'draft',  -- draft, published, archived
    seo_score INT,  -- ML quality prediction 0-100
    indexed_at TIMESTAMP,  -- When Google indexed it
    pageviews_total INT DEFAULT 0,
    revenue_total DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_pages_slug ON pages_seo(slug);
CREATE INDEX idx_pages_status ON pages_seo(status);
CREATE INDEX idx_pages_keyword ON pages_seo(keyword);

-- ============================================
-- MODEL B: API MARKETPLACE (SentimentAPI)
-- ============================================

-- API customers
CREATE TABLE api_customers (
    id SERIAL PRIMARY KEY,
    api_key VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(255),
    plan VARCHAR(20) DEFAULT 'free',  -- free, basic, pro
    calls_limit INT DEFAULT 100,  -- Daily limit
    calls_count INT DEFAULT 0,
    last_call_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',  -- active, suspended
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_api_key ON api_customers(api_key);

-- API usage logs
CREATE TABLE api_logs (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES api_customers(id),
    endpoint VARCHAR(100),
    request_params JSONB,
    response_time_ms INT,
    status_code INT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_api_logs_customer ON api_logs(customer_id, created_at DESC);

-- ============================================
-- MODEL C: COMPARISON TOOL (CryptoCompare)
-- ============================================

-- Exchanges (for comparison tables)
CREATE TABLE exchanges (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,  -- Binance, Coinbase
    logo_url TEXT,
    affiliate_url TEXT,
    affiliate_id VARCHAR(100),
    trading_fee DECIMAL(5,3),  -- 0.1% = 0.001
    withdrawal_fee_btc DECIMAL(10,8),
    supported_countries TEXT[],
    rating DECIMAL(3,2),  -- 4.5/5.0
    pros TEXT[],
    cons TEXT[],
    last_updated TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Comparison pages
CREATE TABLE pages_comparison (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(200) UNIQUE NOT NULL,  -- best-crypto-exchange-italy
    title VARCHAR(200),
    meta_description TEXT,
    content TEXT,  -- HTML with comparison table
    exchange_ids INT[],  -- Which exchanges are compared
    keyword VARCHAR(200),
    pageviews_total INT DEFAULT 0,
    affiliate_clicks INT DEFAULT 0,
    affiliate_revenue DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- MODEL D: SAAS (CryptoTracker)
-- ============================================

-- SaaS users
CREATE TABLE saas_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    plan VARCHAR(20) DEFAULT 'free',  -- free, pro
    stripe_customer_id VARCHAR(100),
    stripe_subscription_id VARCHAR(100),
    subscription_status VARCHAR(20),  -- active, canceled, past_due
    trial_ends_at TIMESTAMP,
    subscription_ends_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User portfolios (exchange connections)
CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES saas_users(id),
    exchange_name VARCHAR(50),  -- binance, coinbase
    api_key_encrypted TEXT,  -- Store encrypted
    api_secret_encrypted TEXT,
    last_sync_at TIMESTAMP,
    total_value_usd DECIMAL(20,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- MODEL E: NEWSLETTER (DailyBrief)
-- ============================================

-- Newsletter subscribers
CREATE TABLE newsletter_subscribers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, active, unsubscribed
    source VARCHAR(50),  -- website, twitter, reddit
    confirmed_at TIMESTAMP,
    unsubscribed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Newsletter issues (sent editions)
CREATE TABLE newsletter_issues (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(200),
    content_html TEXT,
    sent_at TIMESTAMP,
    recipients_count INT,
    open_rate DECIMAL(5,2),
    click_rate DECIMAL(5,2),
    sponsor_revenue DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- ANALYTICS (aggregate daily stats)
-- ============================================

CREATE TABLE analytics_daily (
    date DATE NOT NULL,
    project VARCHAR(20) NOT NULL,  -- model_a, model_b, model_c, model_d, model_e
    pageviews INT DEFAULT 0,
    unique_visitors INT DEFAULT 0,
    adsense_revenue DECIMAL(10,2) DEFAULT 0,
    affiliate_revenue DECIMAL(10,2) DEFAULT 0,
    subscription_revenue DECIMAL(10,2) DEFAULT 0,
    total_revenue DECIMAL(10,2) DEFAULT 0,
    PRIMARY KEY (date, project)
);
CREATE INDEX idx_analytics_date ON analytics_daily(date DESC);
