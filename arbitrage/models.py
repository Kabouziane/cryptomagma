from django.db import models
from django.utils import timezone

class Exchange(models.Model):
    name = models.CharField(max_length=50, unique=True)
    api_url = models.URLField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class CryptoPair(models.Model):
    symbol = models.CharField(max_length=20)  # ex: BTC, ETH
    base_currency = models.CharField(max_length=10, default='USDT')
    
    def __str__(self):
        return f"{self.symbol}/{self.base_currency}"

class Price(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    crypto_pair = models.ForeignKey(CryptoPair, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['exchange', 'crypto_pair', 'timestamp']

class ArbitrageOpportunity(models.Model):
    crypto_pair = models.ForeignKey(CryptoPair, on_delete=models.CASCADE)
    buy_exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='buy_opportunities')
    sell_exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='sell_opportunities')
    buy_price = models.DecimalField(max_digits=20, decimal_places=8)
    sell_price = models.DecimalField(max_digits=20, decimal_places=8)
    profit_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-profit_percentage', '-created_at']