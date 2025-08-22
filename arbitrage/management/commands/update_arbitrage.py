from django.core.management.base import BaseCommand
from arbitrage.services import PriceService, ArbitrageService

class Command(BaseCommand):
    help = 'Met à jour les prix et trouve les opportunités d\'arbitrage'

    def handle(self, *args, **options):
        self.stdout.write('Mise à jour des prix...')
        PriceService.update_all_prices()
        
        self.stdout.write('Recherche d\'opportunités d\'arbitrage...')
        ArbitrageService.find_opportunities()
        
        self.stdout.write(self.style.SUCCESS('Mise à jour terminée!'))