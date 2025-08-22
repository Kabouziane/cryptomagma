import requests
import random
from decimal import Decimal
from django.utils import timezone
from .models import Exchange, CryptoPair, Price, ArbitrageOpportunity

class PriceService:
    
    @staticmethod
    def fetch_binance_price(symbol):
        """Récupère le prix depuis Binance"""
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
            response = requests.get(url, timeout=10)
            data = response.json()
            return Decimal(data['price'])
        except:
            return None
    
    @staticmethod
    def fetch_coinbase_price(symbol):
        """Récupère le prix depuis Coinbase"""
        try:
            url = f"https://api.coinbase.com/v2/exchange-rates?currency={symbol}"
            response = requests.get(url, timeout=10)
            data = response.json()
            return Decimal(data['data']['rates']['USD'])
        except:
            return None
    
    @staticmethod
    def fetch_kraken_price(symbol):
        """Récupère le prix depuis Kraken"""
        try:
            symbol_map = {'BTC': 'XBTUSD', 'ETH': 'ETHUSD', 'ADA': 'ADAUSD', 'DOT': 'DOTUSD', 'SOL': 'SOLUSD'}
            kraken_symbol = symbol_map.get(symbol, f"{symbol}USD")
            url = f"https://api.kraken.com/0/public/Ticker?pair={kraken_symbol}"
            response = requests.get(url, timeout=10)
            data = response.json()
            pair_data = list(data['result'].values())[0]
            return Decimal(pair_data['c'][0])
        except:
            return None
    
    @staticmethod
    def fetch_kucoin_price(symbol):
        """Récupère le prix depuis KuCoin"""
        try:
            url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT"
            response = requests.get(url, timeout=10)
            data = response.json()
            return Decimal(data['data']['price'])
        except:
            return None
    
    @staticmethod
    def fetch_gate_price(symbol):
        """Récupère le prix depuis Gate.io"""
        try:
            url = f"https://api.gateio.ws/api/v4/spot/tickers?currency_pair={symbol}_USDT"
            response = requests.get(url, timeout=10)
            data = response.json()
            return Decimal(data[0]['last'])
        except:
            return None
    
    @staticmethod
    def generate_mock_price(base_price, exchange_name):
        """Génère des prix simulés avec variations pour créer des opportunités"""
        if not base_price:
            return None
        
        # Variations par exchange pour créer des opportunités
        variations = {
            'Binance': random.uniform(-0.02, 0.02),
            'Coinbase': random.uniform(-0.03, 0.03), 
            'Kraken': random.uniform(-0.04, 0.04),
            'KuCoin': random.uniform(-0.05, 0.05),
            'Gate.io': random.uniform(-0.06, 0.06),
            'Huobi': random.uniform(-0.04, 0.04),
            'OKX': random.uniform(-0.03, 0.03)
        }
        
        variation = variations.get(exchange_name, 0)
        return base_price * (Decimal('1') + Decimal(str(variation)))
    
    @classmethod
    def update_all_prices(cls):
        """Met à jour tous les prix pour toutes les cryptos"""
        exchanges_methods = {
            'Binance': cls.fetch_binance_price,
            'Coinbase': cls.fetch_coinbase_price,
            'Kraken': cls.fetch_kraken_price,
            'KuCoin': cls.fetch_kucoin_price,
            'Gate.io': cls.fetch_gate_price,
            'Huobi': None,  # Mock seulement
            'OKX': None     # Mock seulement
        }
        
        # Créer les exchanges
        for exchange_name in exchanges_methods.keys():
            Exchange.objects.get_or_create(
                name=exchange_name,
                defaults={'api_url': f'https://api.{exchange_name.lower()}.com'}
            )
        
        # Plus de cryptos
        crypto_symbols = ['BTC', 'ETH', 'ADA', 'DOT', 'SOL', 'MATIC', 'AVAX', 'LINK', 'UNI', 'ATOM']
        for symbol in crypto_symbols:
            CryptoPair.objects.get_or_create(symbol=symbol)
        
        # Récupérer les prix
        for crypto_pair in CryptoPair.objects.all():
            base_price = cls.fetch_binance_price(crypto_pair.symbol)  # Prix de référence
            
            for exchange_name, fetch_method in exchanges_methods.items():
                exchange = Exchange.objects.get(name=exchange_name)
                
                if fetch_method:
                    price = fetch_method(crypto_pair.symbol)
                else:
                    # Prix simulé pour créer des opportunités
                    price = cls.generate_mock_price(base_price, exchange_name)
                
                if price:
                    Price.objects.create(
                        exchange=exchange,
                        crypto_pair=crypto_pair,
                        price=price
                    )

class ArbitrageService:
    
    @staticmethod
    def find_opportunities(min_profit_percentage=4.0):
        """Trouve les opportunités d'arbitrage"""
        # Supprimer les anciennes opportunités
        ArbitrageOpportunity.objects.all().delete()
        
        crypto_pairs = CryptoPair.objects.all()
        
        for crypto_pair in crypto_pairs:
            # Récupérer les derniers prix pour cette crypto
            latest_prices = {}
            for exchange in Exchange.objects.filter(is_active=True):
                latest_price = Price.objects.filter(
                    exchange=exchange,
                    crypto_pair=crypto_pair
                ).order_by('-timestamp').first()
                
                if latest_price:
                    latest_prices[exchange] = latest_price.price
            
            # Comparer tous les prix entre eux
            exchanges = list(latest_prices.keys())
            for i, buy_exchange in enumerate(exchanges):
                for sell_exchange in exchanges[i+1:]:
                    buy_price = latest_prices[buy_exchange]
                    sell_price = latest_prices[sell_exchange]
                    
                    # Calculer le profit dans les deux sens
                    if buy_price < sell_price:
                        profit_pct = ((sell_price - buy_price) / buy_price) * 100
                        if profit_pct >= min_profit_percentage:
                            ArbitrageOpportunity.objects.create(
                                crypto_pair=crypto_pair,
                                buy_exchange=buy_exchange,
                                sell_exchange=sell_exchange,
                                buy_price=buy_price,
                                sell_price=sell_price,
                                profit_percentage=profit_pct
                            )
                    
                    elif sell_price < buy_price:
                        profit_pct = ((buy_price - sell_price) / sell_price) * 100
                        if profit_pct >= min_profit_percentage:
                            ArbitrageOpportunity.objects.create(
                                crypto_pair=crypto_pair,
                                buy_exchange=sell_exchange,
                                sell_exchange=buy_exchange,
                                buy_price=sell_price,
                                sell_price=buy_price,
                                profit_percentage=profit_pct
                            )