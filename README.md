# CryptoMagma - Bot d'Arbitrage Crypto

Bot d'arbitrage automatique pour détecter les opportunités de profit entre différentes plateformes crypto.

## Fonctionnalités

- Surveillance des prix en temps réel sur Binance, Coinbase et Kraken
- Détection automatique des opportunités d'arbitrage
- Interface web pour visualiser les opportunités
- API REST pour intégration externe
- Mise à jour automatique des prix

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

## Commandes

- `python manage.py update_arbitrage` - Met à jour les prix et trouve les opportunités
- `python manage.py runserver` - Lance le serveur web

## API

- `/api/opportunities/` - Liste des opportunités en JSON
- `/update-prices/` - Met à jour les prix (POST)