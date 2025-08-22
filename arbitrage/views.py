from django.shortcuts import render
from django.http import JsonResponse
from .models import ArbitrageOpportunity, Price
from .services import PriceService, ArbitrageService

def dashboard(request):
    """Page principale avec les opportunités d'arbitrage"""
    opportunities = ArbitrageOpportunity.objects.all()[:20]  # Top 20
    return render(request, 'arbitrage/dashboard.html', {
        'opportunities': opportunities
    })

def update_prices(request):
    """API pour mettre à jour les prix"""
    try:
        PriceService.update_all_prices()
        ArbitrageService.find_opportunities()
        return JsonResponse({'status': 'success', 'message': 'Prix mis à jour'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def api_opportunities(request):
    """API pour récupérer les opportunités en JSON"""
    opportunities = ArbitrageOpportunity.objects.all()[:20]
    data = []
    
    for opp in opportunities:
        data.append({
            'crypto': opp.crypto_pair.symbol,
            'buy_exchange': opp.buy_exchange.name,
            'sell_exchange': opp.sell_exchange.name,
            'buy_price': float(opp.buy_price),
            'sell_price': float(opp.sell_price),
            'profit_percentage': float(opp.profit_percentage),
            'created_at': opp.created_at.isoformat()
        })
    
    return JsonResponse({'opportunities': data})