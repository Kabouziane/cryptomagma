# CryptoMagma - Bot d'Arbitrage Crypto

Bot d'arbitrage automatique pour détecter les opportunités de profit entre différentes plateformes crypto avec **données 100% réelles**.

## Fonctionnalités

- **7 plateformes** : Binance, Coinbase Pro, Kraken, KuCoin, Gate.io, Huobi, OKX
- **5 cryptomonnaies** : BTC, ETH, ADA, SOL, MATIC
- **APIs officielles uniquement** - Aucune donnée simulée
- **Détection automatique** des opportunités d'arbitrage (seuil 1%)
- **Interface web** responsive avec mise à jour temps réel
- **API REST** pour intégration externe

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py update_arbitrage
python manage.py runserver
```

## Utilisation

1. Accédez à http://127.0.0.1:8000 pour voir le dashboard
2. Cliquez sur "Mettre à jour les prix" pour rechercher de nouvelles opportunités
3. Les opportunités s'affichent avec le pourcentage de profit potentiel
4. Auto-refresh toutes les 5 minutes

## Exemple d'opportunité

```
💰 Profit potentiel: 2.45%
🛒 Acheter BTC sur Kraken: $43,250.00
💸 Vendre BTC sur Gate.io: $44,310.00
```

## Commandes

- `python manage.py update_arbitrage` - Met à jour les prix et trouve les opportunités
- `python manage.py runserver` - Lance le serveur web

## API Endpoints

- `GET /api/opportunities/` - Liste des opportunités en JSON
- `POST /update-prices/` - Met à jour les prix manuellement

## Plateformes supportées

| Plateforme | API Endpoint | Status |
|------------|--------------|--------|
| Binance | api.binance.com | ✅ |
| Coinbase Pro | api.exchange.coinbase.com | ✅ |
| Kraken | api.kraken.com | ✅ |
| KuCoin | api.kucoin.com | ✅ |
| Gate.io | api.gateio.ws | ✅ |
| Huobi | api.huobi.pro | ✅ |
| OKX | www.okx.com | ✅ |