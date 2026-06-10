"""
Run with: python manage.py shell < seed_data.py
Populates the database with sample data for Sprint 1 demo.
"""
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

from apps.places.models import Place
from apps.activities.models import Activity, ActivityType
from apps.events.models import Event, EventStatus
from apps.users.models import User
from django.utils import timezone
from datetime import timedelta
import uuid

print("Seeding places...")
places_data = [
    {"name": "Parque Centenario", "description": "Gran parque urbano con lago y feria de artesanos los fines de semana.", "category": "parque", "address": "Av. Díaz Vélez 4699", "city": "Buenos Aires", "latitude": -34.6057, "longitude": -58.4341, "price_level": 0},
    {"name": "Teatro Colón", "description": "Uno de los mejores teatros de ópera del mundo, joya arquitectónica de Buenos Aires.", "category": "teatro", "address": "Cerrito 628", "city": "Buenos Aires", "latitude": -34.6010, "longitude": -58.3833, "price_level": 3},
    {"name": "La Biela", "description": "Clásico café de Recoleta, punto de encuentro de artistas e intelectuales.", "category": "café", "address": "Av. Quintana 600", "city": "Buenos Aires", "latitude": -34.5874, "longitude": -58.3929, "price_level": 2},
    {"name": "MALBA", "description": "Museo de Arte Latinoamericano con colección permanente y muestras temporarias.", "category": "museo", "address": "Av. Figueroa Alcorta 3415", "city": "Buenos Aires", "latitude": -34.5755, "longitude": -58.4050, "price_level": 2},
    {"name": "Estadio Monumental", "description": "Estadio de River Plate, el más grande de Argentina.", "category": "estadio", "address": "Av. Figueroa Alcorta 7597", "city": "Buenos Aires", "latitude": -34.5454, "longitude": -58.4498, "price_level": 2},
    {"name": "Mercado de San Telmo", "description": "Mercado histórico con gastronomía, antigüedades y locales de autor.", "category": "gastronomía", "address": "Carlos Calvo 430", "city": "Buenos Aires", "latitude": -34.6200, "longitude": -58.3703, "price_level": 1},
    {"name": "Complejo Cines Hoyts Abasto", "description": "Cines multipantalla con las últimas estrenos.", "category": "cine", "address": "Av. Corrientes 3247", "city": "Buenos Aires", "latitude": -34.6027, "longitude": -58.4135, "price_level": 2},
    {"name": "Don Julio", "description": "Parrilla porteña clásica, premiada internacionalmente.", "category": "gastronomía", "address": "Guatemala 4691", "city": "Buenos Aires", "latitude": -34.5862, "longitude": -58.4258, "price_level": 3},
]

created_places = []
for p in places_data:
    obj, created = Place.objects.get_or_create(name=p["name"], defaults=p)
    created_places.append(obj)
    if created:
        print(f"  + {obj.name}")

print("Seeding activities...")
activities_data = [
    {"name": "Asado en parque", "description": "Juntate con amigos a hacer un asado al aire libre.", "category": "outdoor", "activity_type": ActivityType.PARK, "min_budget": 2000, "max_budget": 8000, "min_people": 2, "max_people": 20, "indoor": False, "outdoor": True, "score_base": 85},
    {"name": "Cena en restaurante", "description": "Disfrutá una cena en alguno de los mejores restaurantes de la ciudad.", "category": "gastronomía", "activity_type": ActivityType.RESTAURANT, "min_budget": 3000, "max_budget": 15000, "min_people": 1, "max_people": 8, "indoor": True, "outdoor": False, "score_base": 80},
    {"name": "Ir al cine", "description": "Disfrutá la última película en pantalla grande.", "category": "cine", "activity_type": ActivityType.CINEMA, "min_budget": 2500, "max_budget": 4000, "min_people": 1, "max_people": 6, "indoor": True, "outdoor": False, "score_base": 78},
    {"name": "Visitar un museo", "description": "Enriquecé tu cultura visitando museos de arte, historia o ciencia.", "category": "arte", "activity_type": ActivityType.MUSEUM, "min_budget": 0, "max_budget": 2000, "min_people": 1, "max_people": 10, "indoor": True, "outdoor": False, "score_base": 72},
    {"name": "Partido de fútbol", "description": "Viví la emoción de ver un partido en vivo.", "category": "deportes", "activity_type": ActivityType.SPORTS, "min_budget": 5000, "max_budget": 20000, "min_people": 1, "max_people": 50, "indoor": False, "outdoor": True, "score_base": 90},
    {"name": "Salir a un bar", "description": "Tomá algo con amigos en un bar con buena música.", "category": "música", "activity_type": ActivityType.BAR, "min_budget": 2000, "max_budget": 6000, "min_people": 2, "max_people": 10, "indoor": True, "outdoor": True, "score_base": 82},
    {"name": "Gaming night", "description": "Jugá videojuegos con amigos durante la noche.", "category": "gaming", "activity_type": ActivityType.GAMING, "min_budget": 0, "max_budget": 500, "min_people": 1, "max_people": 4, "indoor": True, "outdoor": False, "score_base": 70},
    {"name": "Tour turístico", "description": "Recorrés los sitios más emblemáticos de la ciudad con un guía.", "category": "turismo", "activity_type": ActivityType.TOURISM, "min_budget": 3000, "max_budget": 8000, "min_people": 1, "max_people": 20, "indoor": False, "outdoor": True, "score_base": 75},
    {"name": "Shopping center", "description": "Recorrés shoppings y centros comerciales.", "category": "shopping", "activity_type": ActivityType.SHOPPING, "min_budget": 0, "max_budget": 50000, "min_people": 1, "max_people": 5, "indoor": True, "outdoor": False, "score_base": 60},
    {"name": "Concierto en vivo", "description": "Disfrutá de un show musical en vivo.", "category": "música", "activity_type": ActivityType.CONCERT, "min_budget": 5000, "max_budget": 30000, "min_people": 1, "max_people": 100, "indoor": False, "outdoor": True, "score_base": 95},
]

for a in activities_data:
    obj, created = Activity.objects.get_or_create(name=a["name"], defaults=a)
    if created:
        print(f"  + {obj.name}")

print("Seeding events...")
admin_user = User.objects.filter(role="admin").first()
colón = next((p for p in created_places if "Colón" in p.name), None)
malba = next((p for p in created_places if "MALBA" in p.name), None)
monumental = next((p for p in created_places if "Monumental" in p.name), None)

events_data = [
    {
        "title": "Noche de Ópera en el Colón",
        "description": "La Traviata de Verdi presentada por la Orquesta Estable del Teatro Colón.",
        "category": "música",
        "start_date": timezone.now() + timedelta(days=7),
        "end_date": timezone.now() + timedelta(days=7, hours=3),
        "minimum_age": 0,
        "capacity": 2500,
        "price": 15000,
        "status": EventStatus.PUBLISHED,
        "place": colón,
        "organizer": admin_user,
    },
    {
        "title": "Exposición de Arte Contemporáneo",
        "description": "Muestra colectiva de artistas latinoamericanos emergentes.",
        "category": "arte",
        "start_date": timezone.now() + timedelta(days=3),
        "end_date": timezone.now() + timedelta(days=30),
        "minimum_age": 0,
        "capacity": 500,
        "price": 1500,
        "status": EventStatus.PUBLISHED,
        "place": malba,
        "organizer": admin_user,
    },
    {
        "title": "Clásico River vs Boca",
        "description": "El superclásico del fútbol argentino en el Monumental.",
        "category": "deportes",
        "start_date": timezone.now() + timedelta(days=14),
        "end_date": timezone.now() + timedelta(days=14, hours=2),
        "minimum_age": 0,
        "capacity": 84567,
        "price": 12000,
        "status": EventStatus.PUBLISHED,
        "place": monumental,
        "organizer": admin_user,
    },
    {
        "title": "Festival de Música Electrónica",
        "description": "Una noche de sets de DJs internacionales y nacionales.",
        "category": "música",
        "start_date": timezone.now() + timedelta(days=5),
        "end_date": timezone.now() + timedelta(days=5, hours=6),
        "minimum_age": 18,
        "capacity": 3000,
        "price": 8000,
        "status": EventStatus.PUBLISHED,
        "place": None,
        "organizer": admin_user,
    },
    {
        "title": "Feria del Libro Independiente",
        "description": "Editoras independientes, autores y lectores en un encuentro cultural.",
        "category": "cultura",
        "start_date": timezone.now() + timedelta(days=2),
        "end_date": timezone.now() + timedelta(days=9),
        "minimum_age": 0,
        "capacity": 1000,
        "price": 0,
        "status": EventStatus.PUBLISHED,
        "place": None,
        "organizer": admin_user,
    },
]

for e in events_data:
    if not Event.objects.filter(title=e["title"]).exists():
        Event.objects.create(**e)
        print(f"  + {e['title']}")

print("\n✓ Seed completado.")
