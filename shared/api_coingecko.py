"""
CoinGecko API Client
Free tier: 50 calls/minute
"""
import requests
import time
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class CoinGeckoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'x-cg-pro-api-key': api_key})
        self.last_call = 0
        self.min_interval = 1.2  # 50 calls/min = 1.2s between calls
    
    def _rate_limit(self):
        """Enforce rate limiting"""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()
    
    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make GET request with rate limiting"""
        self._rate_limit()
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"CoinGecko API error: {e}")
            return {}
    
    def get_price(self, coin_id: str, vs_currency: str = 'usd') -> Optional[float]:
        """
        Get current price for a coin
        
        Args:
            coin_id: CoinGecko ID (e.g., 'bitcoin', 'ethereum')
            vs_currency: Currency to price in (default: 'usd')
        
        Returns:
            Price as float, or None if error
        """
        data = self._get(
            'simple/price',
            params={
                'ids': coin_id,
                'vs_currencies': vs_currency,
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
        )
        
        if coin_id in data:
            return data[coin_id].get(vs_currency)
        return None
    
    def get_coin_data(self, coin_id: str) -> Dict:
        """
        Get comprehensive coin data
        
        Returns:
            Dict with price, market_cap, volume, etc.
        """
        data = self._get(
            'simple/price',
            params={
                'ids': coin_id,
                'vs_currencies': 'usd,eur',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true',
                'include_24hr_change': 'true'
            }
        )
        
        if coin_id not in data:
            return {}
        
        coin_data = data[coin_id]
        return {
            'price_usd': coin_data.get('usd'),
            'price_eur': coin_data.get('eur'),
            'market_cap_usd': coin_data.get('usd_market_cap'),
            'volume_24h_usd': coin_data.get('usd_24h_vol'),
            'change_24h': coin_data.get('usd_24h_change')
        }
    
    def get_top_coins(self, limit: int = 100) -> List[Dict]:
        """
        Get top coins by market cap
        
        Args:
            limit: Number of coins to fetch (max 250)
        
        Returns:
            List of coin data dicts
        """
        data = self._get(
            'coins/markets',
            params={
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': min(limit, 250),
                'page': 1,
                'sparkline': 'false'
            }
        )
        
        if not isinstance(data, list):
            return []
        
        return [{
            'id': coin['id'],
            'symbol': coin['symbol'].upper(),
            'name': coin['name'],
            'price': coin['current_price'],
            'market_cap': coin['market_cap'],
            'volume_24h': coin['total_volume'],
            'change_24h': coin.get('price_change_percentage_24h', 0)
        } for coin in data]
    
    def get_historical_price(self, coin_id: str, days: int = 30) -> List[Dict]:
        """
        Get historical prices
        
        Args:
            coin_id: CoinGecko ID
            days: Number of days of history (max 365 for free tier)
        
        Returns:
            List of {timestamp, price} dicts
        """
        data = self._get(
            f'coins/{coin_id}/market_chart',
            params={
                'vs_currency': 'usd',
                'days': days
            }
        )
        
        if 'prices' not in data:
            return []
        
        return [
            {
                'timestamp': point[0] / 1000,  # Convert ms to seconds
                'price': point[1]
            }
            for point in data['prices']
        ]
    
    def search_coin(self, query: str) -> List[Dict]:
        """
        Search for coins by name/symbol
        
        Returns:
            List of matching coins
        """
        data = self._get('search', params={'query': query})
        
        if 'coins' not in data:
            return []
        
        return [{
            'id': coin['id'],
            'symbol': coin['symbol'].upper(),
            'name': coin['name']
        } for coin in data['coins'][:10]]  # Top 10 results

# Global instance
coingecko = CoinGeckoAPI()
