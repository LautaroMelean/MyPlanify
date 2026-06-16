import time
from django.core.management.base import BaseCommand
from apps.integrations.providers.overpass import overpass_provider
from apps.integrations.services import _upsert_places

NEIGHBORHOODS = [
    ("Palermo",          -34.5883, -58.4322, 2000),
    ("Recoleta",         -34.5928, -58.3954, 1500),
    ("San Telmo",        -34.6218, -58.3731, 1500),
    ("Belgrano",         -34.5599, -58.4488, 1500),
    ("Centro",           -34.6118, -58.3736, 1500),
    ("Villa Crespo",     -34.6033, -58.4330, 1500),
]


class Command(BaseCommand):
    help = "Pre-carga lugares de Buenos Aires desde OpenStreetMap via Overpass API"

    def handle(self, *args, **options):
        total = 0
        for name, lat, lon, radius in NEIGHBORHOODS:
            self.stdout.write(f"  Buscando en {name}...")
            try:
                raw = overpass_provider.search_nearby(lat, lon, radius)
                places = _upsert_places(raw)
                self.stdout.write(self.style.SUCCESS(f"  ✓ {name}: {len(places)} lugares"))
                total += len(places)
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"  ✗ {name}: {exc}"))
            time.sleep(6)  # Overpass rate limit: 1 req per ~5s

        self.stdout.write(self.style.SUCCESS(f"\nTotal: {total} lugares de Buenos Aires listos."))
