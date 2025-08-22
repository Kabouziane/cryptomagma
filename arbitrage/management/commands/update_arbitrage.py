from django.core.management.base import BaseCommand
from arbitrage.services import PriceService, ArbitrageService
from arbitrage.models import Price, ArbitrageOpportunity

class Command(BaseCommand):
    help = 'Met à jour les prix et trouve les opportunités d\'arbitrage'

    def handle(self, *args, **options):
        self.stdout.write('Mise à jour des prix...')
        PriceService.update_all_prices()
        
        # Debug: afficher les prix récupérés
        prices_count = Price.objects.count()
        self.stdout.write(f'Prix récupérés: {prices_count}')
        
        self.stdout.write('Recherche d\'opportunités d\'arbitrage...')
        ArbitrageService.find_opportunities()
        
        # Debug: afficher les opportunités trouvées
        opportunities_count = ArbitrageOpportunity.objects.count()
        self.stdout.write(f'Opportunités trouvées: {opportunities_count}')
        
        self.stdout.write(self.style.SUCCESS('Mise à jour terminée!'))