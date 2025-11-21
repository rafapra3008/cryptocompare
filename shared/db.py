"""
Database utilities for Revenue Portfolio
Shared across all 5 projects
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import logging
from .config import Config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.config = {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'database': Config.DB_NAME,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query and optionally fetch results"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                return cursor.rowcount
    
    def insert_asset(self, symbol, name, asset_type, coingecko_id=None):
        """Insert a new asset (crypto/stock)"""
        query = """
            INSERT INTO assets (symbol, name, type, coingecko_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (symbol) DO NOTHING
            RETURNING id
        """
        result = self.execute_query(
            query, 
            (symbol, name, asset_type, coingecko_id),
            fetch=True
        )
        return result[0]['id'] if result else None
    
    def insert_price(self, asset_id, price, volume=None, market_cap=None, source='coingecko'):
        """Insert price data"""
        query = """
            INSERT INTO prices (asset_id, price, volume, market_cap, source, timestamp)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        self.execute_query(query, (asset_id, price, volume, market_cap, source))
    
    def get_latest_price(self, symbol):
        """Get latest price for an asset"""
        query = """
            SELECT p.price, p.timestamp, a.symbol
            FROM prices p
            JOIN assets a ON p.asset_id = a.id
            WHERE a.symbol = %s
            ORDER BY p.timestamp DESC
            LIMIT 1
        """
        result = self.execute_query(query, (symbol,), fetch=True)
        return result[0] if result else None
    
    def insert_page_seo(self, slug, title, meta_desc, content, keyword, asset_id=None):
        """Insert SEO page (Model A)"""
        query = """
            INSERT INTO pages_seo 
            (slug, title, meta_description, content, keyword, asset_id, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'published')
            ON CONFLICT (slug) DO UPDATE SET
                content = EXCLUDED.content,
                updated_at = NOW()
            RETURNING id
        """
        result = self.execute_query(
            query,
            (slug, title, meta_desc, content, keyword, asset_id),
            fetch=True
        )
        return result[0]['id'] if result else None
    
    def insert_exchange(self, name, logo_url, affiliate_url, affiliate_id, 
                       trading_fee, rating=None):
        """Insert exchange data (Model C)"""
        query = """
            INSERT INTO exchanges 
            (name, logo_url, affiliate_url, affiliate_id, trading_fee, rating)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET
                affiliate_url = EXCLUDED.affiliate_url,
                trading_fee = EXCLUDED.trading_fee,
                last_updated = NOW()
            RETURNING id
        """
        result = self.execute_query(
            query,
            (name, logo_url, affiliate_url, affiliate_id, trading_fee, rating),
            fetch=True
        )
        return result[0]['id'] if result else None
    
    def get_all_exchanges(self):
        """Get all exchanges for comparison tables"""
        query = """
            SELECT * FROM exchanges
            ORDER BY rating DESC NULLS LAST
        """
        return self.execute_query(query, fetch=True)
    
    def track_affiliate_click(self, page_slug, exchange_name):
        """Track affiliate click (Model C)"""
        # First update page clicks
        query_page = """
            UPDATE pages_comparison
            SET affiliate_clicks = affiliate_clicks + 1
            WHERE slug = %s
        """
        self.execute_query(query_page, (page_slug,))
        
        # Log click event (for detailed analytics)
        logger.info(f"Affiliate click: {exchange_name} from {page_slug}")
    
    def log_daily_analytics(self, date, project, pageviews, revenue_adsense=0, 
                           revenue_affiliate=0, revenue_subscription=0):
        """Log daily analytics for a project"""
        total = revenue_adsense + revenue_affiliate + revenue_subscription
        query = """
            INSERT INTO analytics_daily 
            (date, project, pageviews, adsense_revenue, affiliate_revenue, 
             subscription_revenue, total_revenue)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (date, project) DO UPDATE SET
                pageviews = analytics_daily.pageviews + EXCLUDED.pageviews,
                adsense_revenue = analytics_daily.adsense_revenue + EXCLUDED.adsense_revenue,
                affiliate_revenue = analytics_daily.affiliate_revenue + EXCLUDED.affiliate_revenue,
                subscription_revenue = analytics_daily.subscription_revenue + EXCLUDED.subscription_revenue,
                total_revenue = analytics_daily.total_revenue + EXCLUDED.total_revenue
        """
        self.execute_query(
            query,
            (date, project, pageviews, revenue_adsense, revenue_affiliate, 
             revenue_subscription, total)
        )
    
    def get_weekly_stats(self, days=7):
        """Get weekly stats across all projects"""
        query = """
            SELECT 
                project,
                SUM(pageviews) as total_pageviews,
                SUM(total_revenue) as total_revenue,
                AVG(total_revenue / NULLIF(pageviews, 0) * 1000) as rpm
            FROM analytics_daily
            WHERE date >= CURRENT_DATE - INTERVAL '%s days'
            GROUP BY project
            ORDER BY total_revenue DESC
        """
        return self.execute_query(query, (days,), fetch=True)

# Singleton instance
db = Database()
