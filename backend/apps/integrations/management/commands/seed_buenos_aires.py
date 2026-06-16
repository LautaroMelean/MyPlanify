"""
Seed de lugares de Buenos Aires desde OpenStreetMap via Overpass API.
Actualiza también los city names de places existentes.
"""
import time
from django.core.management.base import BaseCommand
from django.db.models import Q
from apps.integrations.providers.overpass import overpass_provider, CITY_ALIASES
from apps.integrations.services import _upsert_places
from apps.places.models import Place

# (barrio, lat, lon, radio_metros)
NEIGHBORHOODS = [
    ("Palermo",          -34.5883, -58.4322, 2500),
    ("Recoleta",         -34.5928, -58.3954, 2000),
    ("San Telmo",        -34.6218, -58.3731, 1800),
    ("Belgrano",         -34.5599, -58.4488, 2000),
    ("Centro/Microcentro", -34.6037, -58.3816, 2000),
    ("Villa Crespo",     -34.6033, -58.4330, 1800),
    ("Caballito",        -34.6194, -58.4421, 1800),
    ("Flores",           -34.6289, -58.4626, 1800),
    ("La Boca",          -34.6356, -58.3637, 1500),
    ("Almagro",          -34.6098, -58.4206, 1800),
    ("Boedo",            -34.6270, -58.4173, 1500),
    ("Colegiales",       -34.5742, -58.4479, 1500),
]


def _normalize_existing_cities():
    """Fix city names already in DB from previous seeds."""
    aliases = {k: v for k, v in CITY_ALIASES.items()}
    updated = 0
    for place in Place.objects.filter(source="osm").exclude(city="Buenos Aires"):
        raw = place.city.strip().lower()
        canonical = aliases.get(raw)
        if canonical:
            place.city = canonical
            place.save(update_fields=["city"])
            updated += 1
    return updated


class Command(BaseCommand):
    help = "Pre-carga y actualiza lugares de Buenos Aires desde OpenStreetMap via Overpass API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--normalize-only",
            action="store_true",
            help="Solo normaliza los city names existentes, sin hacer nuevas requests a Overpass.",
        )

    def handle(self, *args, **options):
        # Step 0: normalize existing places first
        self.stdout.write("Normalizando nombres de ciudad en la DB...")
        fixed = _normalize_existing_cities()
        self.stdout.write(self.style.SUCCESS(f"  ✓ {fixed} places actualizados a 'Buenos Aires'"))

        if options["normalize_only"]:
            return

        total = 0
        for name, lat, lon, radius in NEIGHBORHOODS:
            self.stdout.write(f"  Buscando en {name} (radio {radius}m)...")
            try:
                raw = overpass_provider.search_nearby(lat, lon, radius)
                # Force city = Buenos Aires for all seeded places
                for item in raw:
                    if not item.get("city"):
                        item["city"] = "Buenos Aires"
                places = _upsert_places(raw)
                self.stdout.write(self.style.SUCCESS(f"  ✓ {name}: {len(places)} lugares"))
                total += len(places)
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"  ✗ {name}: {exc}"))
            time.sleep(8)  # Overpass rate limit

        self.stdout.write(self.style.SUCCESS(f"\nTotal: {total} lugares de Buenos Aires listos."))
