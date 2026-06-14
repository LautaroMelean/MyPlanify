"""
Pobla la base de datos con datos realistas de Buenos Aires.
Uso: python manage.py seed_data
     python manage.py seed_data --clear   (borra todo primero)
"""
from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone


def img(seed: str, w=800, h=500) -> str:
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


PLACES_DATA = [
    # ── Cafés ────────────────────────────────────────────────────────────────
    {
        "name": "Café Tortoni",
        "description": "El café más antiguo y emblemático de Buenos Aires, fundado en 1858. Tango en vivo, medialunas y el mejor café con leche de la ciudad.",
        "category": "Café",
        "address": "Av. de Mayo 829",
        "city": "Buenos Aires",
        "latitude": -34.6087, "longitude": -58.3775,
        "phone": "+54 11 4342-4328",
        "website": "https://cafetortoni.com.ar",
        "image_url": img("tortoni"), "price_level": 2,
    },
    {
        "name": "La Biela",
        "description": "Histórico café frente al Cementerio de la Recoleta. Punto de encuentro de artistas e intelectuales porteños desde 1850.",
        "category": "Café",
        "address": "Av. Quintana 600",
        "city": "Buenos Aires",
        "latitude": -34.5873, "longitude": -58.3929,
        "phone": "+54 11 4804-0449",
        "website": "",
        "image_url": img("labiela-cafe"), "price_level": 2,
    },
    {
        "name": "El Federal",
        "description": "Bar notable de San Telmo con más de 150 años de historia. Madera, espejo y el aroma del café recién hecho.",
        "category": "Café",
        "address": "Carlos Calvo 599",
        "city": "Buenos Aires",
        "latitude": -34.6195, "longitude": -58.3721,
        "phone": "+54 11 4300-4313",
        "website": "",
        "image_url": img("elfederal"), "price_level": 1,
    },
    {
        "name": "Ninina Bakery",
        "description": "Panadería y cafetería con el mejor banana bread de Palermo. Ambiente tranquilo, luz natural y wifi.",
        "category": "Café",
        "address": "Gorriti 4738",
        "city": "Buenos Aires",
        "latitude": -34.5883, "longitude": -58.4215,
        "phone": "+54 11 4833-6800",
        "website": "https://ninina.com",
        "image_url": img("ninina-bakery"), "price_level": 2,
    },
    {
        "name": "Full City Coffee",
        "description": "Tercera ola del café en Buenos Aires. Especialidad en pour over, aeropress y espresso de origen único.",
        "category": "Café",
        "address": "Honduras 4999",
        "city": "Buenos Aires",
        "latitude": -34.5870, "longitude": -58.4255,
        "phone": "",
        "website": "",
        "image_url": img("fullcity-coffee"), "price_level": 2,
    },
    # ── Gastronomía / Restaurantes ────────────────────────────────────────────
    {
        "name": "Don Julio",
        "description": "Considerada una de las mejores parrillas de Argentina. Vinos premium y cortes de carne madurados a la vista.",
        "category": "Gastronomía",
        "address": "Guatemala 4691",
        "city": "Buenos Aires",
        "latitude": -34.5886, "longitude": -58.4260,
        "phone": "+54 11 4831-9564",
        "website": "https://parrilladonjulio.com",
        "image_url": img("donjulio-parrilla"), "price_level": 4,
    },
    {
        "name": "Mercado de San Telmo",
        "description": "Histórico mercado cubierto con puestos de comida, antigüedades y productos regionales. Ideal para el mediodía.",
        "category": "Gastronomía",
        "address": "Carlos Calvo 430",
        "city": "Buenos Aires",
        "latitude": -34.6204, "longitude": -58.3732,
        "phone": "",
        "website": "https://mercadodesantelmo.com",
        "image_url": img("mercado-santelmo"), "price_level": 1,
    },
    {
        "name": "La Malbequería",
        "description": "Restaurante de cocina argentina contemporánea. Reconocida por su selección de Malbec y sus empanadas artesanales.",
        "category": "Gastronomía",
        "address": "Thames 1880",
        "city": "Buenos Aires",
        "latitude": -34.5916, "longitude": -58.4288,
        "phone": "+54 11 4775-5800",
        "website": "",
        "image_url": img("malbequeria"), "price_level": 3,
    },
    {
        "name": "El Preferido de Palermo",
        "description": "Bar de barrio con más de 100 años. Tapas, vermut y una carta de vinos que nadie espera pero todos agradecen.",
        "category": "Gastronomía",
        "address": "Jorge Luis Borges 2108",
        "city": "Buenos Aires",
        "latitude": -34.5853, "longitude": -58.4340,
        "phone": "+54 11 4774-6585",
        "website": "",
        "image_url": img("preferido-palermo"), "price_level": 2,
    },
    {
        "name": "Gran Dabbang",
        "description": "Cocina de autor con influencias asiáticas y latinoamericanas. El plato del día siempre sorprende.",
        "category": "Gastronomía",
        "address": "Scalabrini Ortiz 1543",
        "city": "Buenos Aires",
        "latitude": -34.5937, "longitude": -58.4395,
        "phone": "+54 11 4832-1186",
        "website": "",
        "image_url": img("gran-dabbang"), "price_level": 3,
    },
    # ── Bares ─────────────────────────────────────────────────────────────────
    {
        "name": "Florería Atlántico",
        "description": "Bar subterráneo con entrada por una florería. Cócteles de autor premiados a nivel mundial. Ambiente íntimo y único.",
        "category": "Bar",
        "address": "Arroyo 872",
        "city": "Buenos Aires",
        "latitude": -34.5934, "longitude": -58.3817,
        "phone": "+54 11 4313-6093",
        "website": "https://floreriaatlantico.com.ar",
        "image_url": img("floreria-atlantico"), "price_level": 3,
    },
    {
        "name": "Frank's Bar",
        "description": "Bar speakeasy: entrá por la cabina telefónica. Cócteles clásicos y jazz en vivo los jueves.",
        "category": "Bar",
        "address": "Aráoz 1445",
        "city": "Buenos Aires",
        "latitude": -34.5945, "longitude": -58.4251,
        "phone": "+54 11 4777-6541",
        "website": "",
        "image_url": img("franks-bar"), "price_level": 3,
    },
    {
        "name": "Astor Palermo",
        "description": "Bar de vermut y tapas en Villa Crespo. Ambiente barrial, música en vivo los fines de semana.",
        "category": "Bar",
        "address": "Corrientes 5729",
        "city": "Buenos Aires",
        "latitude": -34.5993, "longitude": -58.4454,
        "phone": "",
        "website": "",
        "image_url": img("astor-bar"), "price_level": 2,
    },
    {
        "name": "Verne Club",
        "description": "Club literario con bar y sala de lectura. Cócteles con nombres de personajes de ciencia ficción.",
        "category": "Bar",
        "address": "Medrano 1475",
        "city": "Buenos Aires",
        "latitude": -34.6034, "longitude": -58.4293,
        "phone": "",
        "website": "",
        "image_url": img("verne-club"), "price_level": 2,
    },
    # ── Museos ─────────────────────────────────────────────────────────────────
    {
        "name": "MALBA",
        "description": "Museo de Arte Latinoamericano de Buenos Aires. Colección permanente de arte del siglo XX y exposiciones temporarias internacionales.",
        "category": "Museo",
        "address": "Av. Figueroa Alcorta 3415",
        "city": "Buenos Aires",
        "latitude": -34.5755, "longitude": -58.4074,
        "phone": "+54 11 4808-6500",
        "website": "https://malba.org.ar",
        "image_url": img("malba-museo"), "price_level": 1,
    },
    {
        "name": "Museo Nacional de Bellas Artes",
        "description": "La colección más importante de arte argentino y latinoamericano. Entrada gratuita. Ideal para una tarde cultural.",
        "category": "Museo",
        "address": "Av. del Libertador 1473",
        "city": "Buenos Aires",
        "latitude": -34.5793, "longitude": -58.3902,
        "phone": "+54 11 5288-9900",
        "website": "https://mnba.gob.ar",
        "image_url": img("bellas-artes"), "price_level": 0,
    },
    {
        "name": "Planetario Galileo Galilei",
        "description": "Espectáculos astronómicos y el telescopio más grande de Buenos Aires. Las noches de viernes hay observación gratuita.",
        "category": "Museo",
        "address": "Av. Sarmiento s/n",
        "city": "Buenos Aires",
        "latitude": -34.5683, "longitude": -58.4103,
        "phone": "+54 11 4771-9393",
        "website": "https://planetario.buenos-aires.gob.ar",
        "image_url": img("planetario"), "price_level": 1,
    },
    {
        "name": "MAMBA",
        "description": "Museo de Arte Moderno de Buenos Aires en San Telmo. Colección de más de 7000 obras y exposiciones de artistas emergentes.",
        "category": "Museo",
        "address": "Av. San Juan 350",
        "city": "Buenos Aires",
        "latitude": -34.6194, "longitude": -58.3691,
        "phone": "+54 11 4342-3001",
        "website": "https://mamba.org.ar",
        "image_url": img("mamba-santelmo"), "price_level": 1,
    },
    # ── Parques ────────────────────────────────────────────────────────────────
    {
        "name": "Parque Tres de Febrero",
        "description": "Los Bosques de Palermo: 400 hectáreas de parque con lago para remar, rosedal, planetario y jogging. El pulmón de la ciudad.",
        "category": "Parque",
        "address": "Av. del Libertador 3000",
        "city": "Buenos Aires",
        "latitude": -34.5676, "longitude": -58.4178,
        "phone": "",
        "website": "",
        "image_url": img("bosques-palermo"), "price_level": 0,
    },
    {
        "name": "Reserva Ecológica Costanera Sur",
        "description": "Reserva natural urbana con 350 especies de aves y vistas al Río de la Plata. Ideal para bicicleta y avistaje de fauna.",
        "category": "Parque",
        "address": "Av. Tristán Achával Rodríguez 1550",
        "city": "Buenos Aires",
        "latitude": -34.6143, "longitude": -58.3542,
        "phone": "",
        "website": "",
        "image_url": img("reserva-ecologica"), "price_level": 0,
    },
    {
        "name": "Parque Centenario",
        "description": "Parque con lago central, feria de libros los fines de semana, anfiteatro y canchas de tenis. El corazón de Caballito.",
        "category": "Parque",
        "address": "Av. Díaz Vélez y Lillo",
        "city": "Buenos Aires",
        "latitude": -34.6175, "longitude": -58.4373,
        "phone": "",
        "website": "",
        "image_url": img("parque-centenario"), "price_level": 0,
    },
    # ── Turismo / Cultura ──────────────────────────────────────────────────────
    {
        "name": "Teatro Colón",
        "description": "Uno de los cinco mejores teatros de ópera del mundo. Visitas guiadas disponibles todos los días. Acústica incomparable.",
        "category": "Entretenimiento",
        "address": "Cerrito 628",
        "city": "Buenos Aires",
        "latitude": -34.6009, "longitude": -58.3833,
        "phone": "+54 11 4378-7344",
        "website": "https://teatrocolon.org.ar",
        "image_url": img("teatro-colon"), "price_level": 2,
    },
    {
        "name": "El Ateneo Grand Splendid",
        "description": "Librería instalada en un antiguo teatro de ópera. Considerada una de las librerías más bellas del mundo por National Geographic.",
        "category": "Turismo",
        "address": "Av. Santa Fe 1860",
        "city": "Buenos Aires",
        "latitude": -34.5972, "longitude": -58.3935,
        "phone": "+54 11 4813-6052",
        "website": "",
        "image_url": img("ateneo-libreria"), "price_level": 0,
    },
    {
        "name": "Caminito",
        "description": "Calle-museo a cielo abierto en La Boca. Colores vibrantes, tango en la calle y arte popular bonaerense.",
        "category": "Turismo",
        "address": "Caminito s/n",
        "city": "Buenos Aires",
        "latitude": -34.6352, "longitude": -58.3637,
        "phone": "",
        "website": "",
        "image_url": img("caminito-boca"), "price_level": 0,
    },
    {
        "name": "Palacio Barolo",
        "description": "Rascacielos de 1923 inspirado en la Divina Comedia de Dante. Visitas nocturnas con vistas 360° de Buenos Aires.",
        "category": "Turismo",
        "address": "Av. de Mayo 1370",
        "city": "Buenos Aires",
        "latitude": -34.6107, "longitude": -58.3819,
        "phone": "+54 11 4381-1885",
        "website": "https://pbarolo.com.ar",
        "image_url": img("palacio-barolo"), "price_level": 1,
    },
    {
        "name": "Cementerio de la Recoleta",
        "description": "Cementerio histórico considerado uno de los más bellos del mundo. Mausoleos art déco y la tumba de Eva Perón.",
        "category": "Turismo",
        "address": "Junín 1760",
        "city": "Buenos Aires",
        "latitude": -34.5876, "longitude": -58.3936,
        "phone": "",
        "website": "",
        "image_url": img("recoleta-cementerio"), "price_level": 0,
    },
    # ── Entretenimiento ────────────────────────────────────────────────────────
    {
        "name": "Centro Cultural Recoleta",
        "description": "Centro cultural con múltiples salas de exposición, teatro y cine. Programación gratuita varios días a la semana.",
        "category": "Entretenimiento",
        "address": "Junín 1930",
        "city": "Buenos Aires",
        "latitude": -34.5875, "longitude": -58.3929,
        "phone": "+54 11 5288-6500",
        "website": "https://centroculturalrecoleta.org",
        "image_url": img("ccrecoleta"), "price_level": 0,
    },
    {
        "name": "La Catedral del Tango",
        "description": "Milonga informal en una fábrica reciclada de Almagro. El mejor lugar para aprender tango en Buenos Aires.",
        "category": "Entretenimiento",
        "address": "Sarmiento 4006",
        "city": "Buenos Aires",
        "latitude": -34.6078, "longitude": -58.4268,
        "phone": "",
        "website": "",
        "image_url": img("catedral-tango"), "price_level": 1,
    },
    {
        "name": "Complejo Art Media",
        "description": "Complejo de cines con las salas más modernas de Buenos Aires. 3D, IMAX y butacas reclinables.",
        "category": "Cine",
        "address": "Corrientes 6333",
        "city": "Buenos Aires",
        "latitude": -34.5980, "longitude": -58.4620,
        "phone": "+54 11 4856-0010",
        "website": "https://artmedia.com.ar",
        "image_url": img("cines-artmedia"), "price_level": 2,
    },
    # ── Deporte ───────────────────────────────────────────────────────────────
    {
        "name": "Estadio Monumental",
        "description": "El estadio más grande de América del Sur. Tours disponibles toda la semana. Sede de River Plate y la Selección Argentina.",
        "category": "Deporte",
        "address": "Av. Figueroa Alcorta 7597",
        "city": "Buenos Aires",
        "latitude": -34.5453, "longitude": -58.4496,
        "phone": "+54 11 4787-1200",
        "website": "https://estadiomonumental.com",
        "image_url": img("monumental-river"), "price_level": 2,
    },
    {
        "name": "Club de Tenis Palermo",
        "description": "Canchas de tenis y padel al aire libre en Palermo. Alquiler por hora, clases grupales e individuales.",
        "category": "Deporte",
        "address": "Av. Tornquist 1426",
        "city": "Buenos Aires",
        "latitude": -34.5702, "longitude": -58.4089,
        "phone": "+54 11 4772-9858",
        "website": "",
        "image_url": img("club-tenis"), "price_level": 2,
    },
]

# ─── Actividades ──────────────────────────────────────────────────────────────
ACTIVITIES_DATA = [
    {
        "name": "Asado porteño en casa",
        "description": "Aprendé a hacer un asado argentino como corresponde: el fuego, los cortes, el chimichurri. Ideal para grupos.",
        "category": "Gastronomía",
        "activity_type": "restaurant",
        "min_budget": Decimal("2000"), "max_budget": Decimal("6000"),
        "min_people": 2, "max_people": 12,
        "indoor": True, "outdoor": True, "score_base": 90,
    },
    {
        "name": "Paseo en bici por Palermo",
        "description": "Recorrido de 2 horas por los Bosques de Palermo, el Rosedal y la Costanera Norte. Para todos los niveles.",
        "category": "Deporte",
        "activity_type": "sports",
        "min_budget": Decimal("0"), "max_budget": Decimal("500"),
        "min_people": 1, "max_people": None,
        "indoor": False, "outdoor": True, "score_base": 85,
    },
    {
        "name": "Clase de tango para principiantes",
        "description": "Una hora de clase con instructor certificado en La Catedral del Tango. No hace falta pareja ni experiencia previa.",
        "category": "Entretenimiento",
        "activity_type": "concert",
        "min_budget": Decimal("1500"), "max_budget": Decimal("3000"),
        "min_people": 1, "max_people": 20,
        "indoor": True, "outdoor": False, "score_base": 88,
    },
    {
        "name": "Tour de murales en La Boca",
        "description": "Recorrido a pie por los barrios de La Boca y San Telmo para conocer el arte urbano que transformó la ciudad.",
        "category": "Turismo",
        "activity_type": "tourism",
        "min_budget": Decimal("0"), "max_budget": Decimal("1000"),
        "min_people": 1, "max_people": None,
        "indoor": False, "outdoor": True, "score_base": 80,
    },
    {
        "name": "Visita guiada al MALBA",
        "description": "Recorrido con guía por la colección permanente del MALBA. Duración 90 minutos. Incluye entrada al museo.",
        "category": "Museo",
        "activity_type": "museum",
        "min_budget": Decimal("800"), "max_budget": Decimal("1800"),
        "min_people": 1, "max_people": 15,
        "indoor": True, "outdoor": False, "score_base": 78,
    },
    {
        "name": "Kayak en el Delta del Tigre",
        "description": "Excursión en kayak por los canales del Tigre. Medio día de aventura a 30 minutos de Buenos Aires.",
        "category": "Deporte",
        "activity_type": "sports",
        "min_budget": Decimal("3000"), "max_budget": Decimal("6000"),
        "min_people": 1, "max_people": 8,
        "indoor": False, "outdoor": True, "score_base": 82,
    },
    {
        "name": "Clase de cocina argentina",
        "description": "Aprendé a cocinar empanadas, locro y dulce de leche casero. Incluye degustación y recetario.",
        "category": "Gastronomía",
        "activity_type": "restaurant",
        "min_budget": Decimal("3500"), "max_budget": Decimal("7000"),
        "min_people": 2, "max_people": 10,
        "indoor": True, "outdoor": False, "score_base": 84,
    },
    {
        "name": "Fútbol 5 en Palermo",
        "description": "Cancha techada de fútbol 5. Alquiler por hora con pelota incluida. Duchas disponibles.",
        "category": "Deporte",
        "activity_type": "sports",
        "min_budget": Decimal("500"), "max_budget": Decimal("2000"),
        "min_people": 10, "max_people": 10,
        "indoor": False, "outdoor": True, "score_base": 75,
    },
    {
        "name": "Picnic en el Rosedal",
        "description": "Tarde de picnic en el Rosedal de Palermo. El lugar más romántico de Buenos Aires con 18.000 rosas en flor.",
        "category": "Parque",
        "activity_type": "park",
        "min_budget": Decimal("500"), "max_budget": Decimal("2000"),
        "min_people": 1, "max_people": None,
        "indoor": False, "outdoor": True, "score_base": 76,
    },
    {
        "name": "Escape Room Microcentro",
        "description": "60 minutos para escapar. Temáticas de suspenso y aventura. Grupos de 2 a 6 personas. Dificultad: media-alta.",
        "category": "Entretenimiento",
        "activity_type": "gaming",
        "min_budget": Decimal("2000"), "max_budget": Decimal("5000"),
        "min_people": 2, "max_people": 6,
        "indoor": True, "outdoor": False, "score_base": 82,
    },
    {
        "name": "Vermut y tapas en San Telmo",
        "description": "Recorrido por los bares históricos de San Telmo con aperitivo y tapas porteñas. El ritual del domingo.",
        "category": "Bar",
        "activity_type": "bar",
        "min_budget": Decimal("1500"), "max_budget": Decimal("4000"),
        "min_people": 2, "max_people": 8,
        "indoor": True, "outdoor": True, "score_base": 83,
    },
    {
        "name": "Yoga al amanecer en el Parque",
        "description": "Clase de yoga outdoor al amanecer en el Parque Tres de Febrero. Esterilla incluida. Todos los niveles.",
        "category": "Deporte",
        "activity_type": "sports",
        "min_budget": Decimal("500"), "max_budget": Decimal("1500"),
        "min_people": 1, "max_people": 20,
        "indoor": False, "outdoor": True, "score_base": 74,
    },
    {
        "name": "Visita nocturna al Palacio Barolo",
        "description": "Tour nocturno por el Palacio Barolo con telescopio y vistas 360° de Buenos Aires. Duración: 2 horas.",
        "category": "Turismo",
        "activity_type": "tourism",
        "min_budget": Decimal("2000"), "max_budget": Decimal("4000"),
        "min_people": 1, "max_people": 30,
        "indoor": True, "outdoor": False, "score_base": 86,
    },
    {
        "name": "Workshop de cerámica",
        "description": "Taller de cerámica para principiantes. Aprendé a tornear y crear tus propias piezas. Materiales incluidos.",
        "category": "Arte",
        "activity_type": "gaming",
        "min_budget": Decimal("3000"), "max_budget": Decimal("6000"),
        "min_people": 1, "max_people": 10,
        "indoor": True, "outdoor": False, "score_base": 72,
    },
    {
        "name": "Noche de bares en Palermo",
        "description": "Recorrido por 4 bares icónicos de Palermo con cóctel de bienvenida en cada uno. Guía incluido.",
        "category": "Bar",
        "activity_type": "bar",
        "min_budget": Decimal("3000"), "max_budget": Decimal("8000"),
        "min_people": 2, "max_people": 10,
        "indoor": True, "outdoor": False, "score_base": 81,
    },
    {
        "name": "Fotografía urbana en el barrio",
        "description": "Salida fotográfica por San Telmo y La Boca. Técnicas de fotografía callejera con instructor profesional.",
        "category": "Arte",
        "activity_type": "tourism",
        "min_budget": Decimal("1500"), "max_budget": Decimal("4000"),
        "min_people": 1, "max_people": 8,
        "indoor": False, "outdoor": True, "score_base": 73,
    },
    {
        "name": "Cata de vinos argentinos",
        "description": "Degustación de 6 vinos cuidadosamente seleccionados con maridaje de quesos y fiambres. Sommelier a cargo.",
        "category": "Gastronomía",
        "activity_type": "restaurant",
        "min_budget": Decimal("3500"), "max_budget": Decimal("7000"),
        "min_people": 2, "max_people": 12,
        "indoor": True, "outdoor": False, "score_base": 85,
    },
    {
        "name": "Senderismo en la Reserva Ecológica",
        "description": "Caminata guiada por la Reserva Ecológica Costanera Sur. Avistaje de aves y flora autóctona. Duración: 3 horas.",
        "category": "Deporte",
        "activity_type": "park",
        "min_budget": Decimal("0"), "max_budget": Decimal("500"),
        "min_people": 1, "max_people": None,
        "indoor": False, "outdoor": True, "score_base": 77,
    },
    {
        "name": "Clases de salsa porteña",
        "description": "Aprende salsa con ritmo porteño en una academia de Almagro. Tres niveles disponibles. Primer clase gratuita.",
        "category": "Entretenimiento",
        "activity_type": "concert",
        "min_budget": Decimal("1000"), "max_budget": Decimal("2500"),
        "min_people": 1, "max_people": 20,
        "indoor": True, "outdoor": False, "score_base": 79,
    },
    {
        "name": "Mateada cultural en el Parque",
        "description": "Encuentro informal con mate, facturas y conversación sobre cultura argentina. Los domingos a las 11.",
        "category": "Café",
        "activity_type": "restaurant",
        "min_budget": Decimal("200"), "max_budget": Decimal("800"),
        "min_people": 2, "max_people": None,
        "indoor": False, "outdoor": True, "score_base": 68,
    },
]

# ─── Eventos (próximos 60 días) ───────────────────────────────────────────────
def make_events(now):
    return [
        {
            "title": "Noche de Jazz en Palermo",
            "description": "Cuatro bandas de jazz en el patio del Centro Cultural Borges. Barra de tragos y entrada libre.",
            "category": "Música",
            "start_date": now + timedelta(days=3, hours=20),
            "end_date": now + timedelta(days=3, hours=24),
            "price": Decimal("0"), "minimum_age": 18, "capacity": 300,
            "image_url": img("jazz-palermo"),
        },
        {
            "title": "Feria del Libro de Buenos Aires",
            "description": "La mayor feria editorial de América Latina. Miles de títulos, presentaciones de autores y talleres para chicos y grandes.",
            "category": "Cultura",
            "start_date": now + timedelta(days=7),
            "end_date": now + timedelta(days=7, hours=8),
            "price": Decimal("600"), "minimum_age": 0, "capacity": 5000,
            "image_url": img("feria-libro"),
        },
        {
            "title": "Festival de Tango Porteño",
            "description": "Milonga masiva en el Obelisco. Shows de parejas profesionales y pista abierta para el público. Entrada gratuita.",
            "category": "Entretenimiento",
            "start_date": now + timedelta(days=5, hours=19),
            "end_date": now + timedelta(days=5, hours=24),
            "price": Decimal("0"), "minimum_age": 0, "capacity": 2000,
            "image_url": img("festival-tango"),
        },
        {
            "title": "Mercado de Diseño Palermo",
            "description": "Más de 100 diseñadores independientes de moda, objetos y arte. El mejor mercado de diseño de Buenos Aires.",
            "category": "Shopping",
            "start_date": now + timedelta(days=2, hours=11),
            "end_date": now + timedelta(days=2, hours=20),
            "price": Decimal("0"), "minimum_age": 0, "capacity": 1000,
            "image_url": img("mercado-diseno"),
        },
        {
            "title": "Exposición: Arte y Naturaleza",
            "description": "Muestra de arte contemporáneo en el MALBA con artistas de 12 países. Obras que dialogan con el medioambiente.",
            "category": "Arte",
            "start_date": now + timedelta(days=1, hours=10),
            "end_date": now + timedelta(days=1, hours=20),
            "price": Decimal("1200"), "minimum_age": 0, "capacity": 500,
            "image_url": img("expo-arte-naturaleza"),
        },
        {
            "title": "Stand Up Comedy - Coco Sily",
            "description": "Noche de comedia en el Teatro Metropolitan. Una hora de humor porteño sin filtro. Prohibido para menores.",
            "category": "Entretenimiento",
            "start_date": now + timedelta(days=4, hours=21),
            "end_date": now + timedelta(days=4, hours=23),
            "price": Decimal("4500"), "minimum_age": 18, "capacity": 400,
            "image_url": img("standup-comedy"),
        },
        {
            "title": "Maratón de Buenos Aires 2026",
            "description": "42K por el centro histórico de Buenos Aires. Categorías: 5K, 10K, 21K y 42K. Inscripción previa obligatoria.",
            "category": "Deporte",
            "start_date": now + timedelta(days=21, hours=7),
            "end_date": now + timedelta(days=21, hours=13),
            "price": Decimal("3500"), "minimum_age": 16, "capacity": 10000,
            "image_url": img("maraton-bsas"),
        },
        {
            "title": "Cena Maridaje — Cocina de Autor",
            "description": "Menú de 5 pasos con maridaje de vinos de Mendoza y Patagonia. Cupo limitado a 20 personas.",
            "category": "Gastronomía",
            "start_date": now + timedelta(days=6, hours=20),
            "end_date": now + timedelta(days=6, hours=24),
            "price": Decimal("12000"), "minimum_age": 18, "capacity": 20,
            "image_url": img("cena-maridaje"),
        },
        {
            "title": "Concierto: Fito Páez en vivo",
            "description": "El Gran Rex recibe al ídolo del rock nacional en un show de 3 horas con invitados especiales.",
            "category": "Música",
            "start_date": now + timedelta(days=12, hours=21),
            "end_date": now + timedelta(days=12, hours=24),
            "price": Decimal("8000"), "minimum_age": 14, "capacity": 1200,
            "image_url": img("fito-paez"),
        },
        {
            "title": "Workshop: Fotografía con iPhone",
            "description": "Taller de 4 horas para aprender a sacar fotos profesionales con el celular. Recorrido por San Telmo incluido.",
            "category": "Arte",
            "start_date": now + timedelta(days=8, hours=10),
            "end_date": now + timedelta(days=8, hours=14),
            "price": Decimal("3500"), "minimum_age": 0, "capacity": 15,
            "image_url": img("workshop-foto"),
        },
        {
            "title": "Feria Gastronómica de Palermo",
            "description": "30 puestos de street food de todo el mundo en el Parque Rivadavia. Comida, música y cerveza artesanal.",
            "category": "Gastronomía",
            "start_date": now + timedelta(days=9, hours=12),
            "end_date": now + timedelta(days=9, hours=21),
            "price": Decimal("0"), "minimum_age": 0, "capacity": 3000,
            "image_url": img("feria-gastronomica"),
        },
        {
            "title": "Noche de Cumbia en La Catedral",
            "description": "DJ set de cumbia clásica y villera en la mítica Catedral del Tango. Las puertas abren a las 23.",
            "category": "Entretenimiento",
            "start_date": now + timedelta(days=2, hours=23),
            "end_date": now + timedelta(days=3, hours=4),
            "price": Decimal("1500"), "minimum_age": 18, "capacity": 500,
            "image_url": img("cumbia-catedral"),
        },
        {
            "title": "Expo Arte Digital — Buenos Aires",
            "description": "Primera gran exposición de arte generativo e IA en Argentina. Obras interactivas y talleres de creación digital.",
            "category": "Arte",
            "start_date": now + timedelta(days=15, hours=11),
            "end_date": now + timedelta(days=15, hours=21),
            "price": Decimal("2000"), "minimum_age": 0, "capacity": 800,
            "image_url": img("expo-arte-digital"),
        },
        {
            "title": "Torneo Abierto de Padel",
            "description": "Torneo amateur con categorías A, B y C. Trofeos para los 3 primeros de cada categoría. Inscripción abierta.",
            "category": "Deporte",
            "start_date": now + timedelta(days=10, hours=9),
            "end_date": now + timedelta(days=10, hours=18),
            "price": Decimal("2500"), "minimum_age": 16, "capacity": 64,
            "image_url": img("torneo-padel"),
        },
        {
            "title": "Festival de Cine Latinoamericano",
            "description": "10 días de cine independiente latinoamericano en el MALBA. Competencia oficial y sección especial de documentales.",
            "category": "Cine",
            "start_date": now + timedelta(days=14, hours=16),
            "end_date": now + timedelta(days=14, hours=22),
            "price": Decimal("1200"), "minimum_age": 13, "capacity": 300,
            "image_url": img("festival-cine"),
        },
        {
            "title": "Clase Abierta de Yoga — Palermo",
            "description": "Clase gratuita de yoga en el Parque Tres de Febrero. Todos los niveles. Llevá tu esterilla.",
            "category": "Deporte",
            "start_date": now + timedelta(days=1, hours=8),
            "end_date": now + timedelta(days=1, hours=9, minutes=30),
            "price": Decimal("0"), "minimum_age": 0, "capacity": 50,
            "image_url": img("yoga-palermo"),
        },
        {
            "title": "Muestra: Frida Kahlo — La Mirada",
            "description": "Retrospectiva de la obra de Frida Kahlo con 80 obras originales y documentos históricos. Imperdible.",
            "category": "Arte",
            "start_date": now + timedelta(days=0, hours=10),
            "end_date": now + timedelta(days=0, hours=20),
            "price": Decimal("2500"), "minimum_age": 0, "capacity": 200,
            "image_url": img("frida-kahlo-expo"),
        },
        {
            "title": "Cata de Cervezas Artesanales",
            "description": "Degustación de 8 estilos de cerveza artesanal con maridaje de snacks. Cervecero a cargo de la explicación.",
            "category": "Gastronomía",
            "start_date": now + timedelta(days=3, hours=18),
            "end_date": now + timedelta(days=3, hours=21),
            "price": Decimal("4000"), "minimum_age": 18, "capacity": 30,
            "image_url": img("cata-cerveza"),
        },
        {
            "title": "Noche de Bares — Ruta Porteña",
            "description": "Recorrido guiado por 5 bares históricos de Buenos Aires. Con copa de bienvenida en cada parada.",
            "category": "Entretenimiento",
            "start_date": now + timedelta(days=4, hours=19),
            "end_date": now + timedelta(days=4, hours=24),
            "price": Decimal("3500"), "minimum_age": 18, "capacity": 25,
            "image_url": img("noche-bares"),
        },
        {
            "title": "Concierto Electrónico — Avant Art",
            "description": "Noche de música electrónica experimental en Niceto Club. Cuatro DJs de escena internacional.",
            "category": "Música",
            "start_date": now + timedelta(days=6, hours=23),
            "end_date": now + timedelta(days=7, hours=5),
            "price": Decimal("3000"), "minimum_age": 18, "capacity": 600,
            "image_url": img("electronica-niceto"),
        },
    ]


class Command(BaseCommand):
    help = "Seed database with Buenos Aires places, activities and events"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Delete existing data before seeding")

    def handle(self, *args, **options):
        from apps.places.models import Place
        from apps.activities.models import Activity
        from apps.events.models import Event, EventStatus
        from apps.promotions.models import Promotion

        if options["clear"]:
            self.stdout.write("Limpiando datos existentes...")
            seed_names = [p["name"] for p in PLACES_DATA]
            Place.objects.filter(name__in=seed_names).delete()
            Activity.objects.filter(name__in=[a["name"] for a in ACTIVITIES_DATA]).delete()
            Event.objects.filter(title__in=[e["title"] for e in make_events(timezone.now())]).delete()

        now = timezone.now()

        # ── Places ────────────────────────────────────────────────────────────
        self.stdout.write("Creando lugares...")
        places = {}
        for p in PLACES_DATA:
            place, created = Place.objects.get_or_create(
                name=p["name"],
                defaults={**p, "source": "internal", "is_active": True},
            )
            places[p["name"]] = place
            if created:
                self.stdout.write(f"  + {place.name}")

        # ── Activities ────────────────────────────────────────────────────────
        self.stdout.write("Creando actividades...")
        activity_place_map = {
            "Clase de tango para principiantes": "La Catedral del Tango",
            "Visita guiada al MALBA": "MALBA",
            "Yoga al amanecer en el Parque": "Parque Tres de Febrero",
            "Visita nocturna al Palacio Barolo": "Palacio Barolo",
            "Senderismo en la Reserva Ecológica": "Reserva Ecológica Costanera Sur",
            "Escape Room Microcentro": None,
            "Paseo en bici por Palermo": "Parque Tres de Febrero",
            "Picnic en el Rosedal": "Parque Tres de Febrero",
        }
        for a in ACTIVITIES_DATA:
            place_name = activity_place_map.get(a["name"])
            activity, created = Activity.objects.get_or_create(
                name=a["name"],
                defaults={
                    **{k: v for k, v in a.items() if k != "name"},
                    "place": places.get(place_name) if place_name else None,
                    "is_active": True,
                },
            )
            if created:
                self.stdout.write(f"  + {activity.name}")

        # ── Events ────────────────────────────────────────────────────────────
        self.stdout.write("Creando eventos...")
        event_place_map = {
            "Noche de Jazz en Palermo": "Centro Cultural Recoleta",
            "Festival de Tango Porteño": "La Catedral del Tango",
            "Mercado de Diseño Palermo": "Parque Tres de Febrero",
            "Exposición: Arte y Naturaleza": "MALBA",
            "Stand Up Comedy - Coco Sily": "Teatro Colón",
            "Noche de Cumbia en La Catedral": "La Catedral del Tango",
            "Festival de Cine Latinoamericano": "MALBA",
            "Clase Abierta de Yoga — Palermo": "Parque Tres de Febrero",
            "Muestra: Frida Kahlo — La Mirada": "Centro Cultural Recoleta",
            "Concierto Electrónico — Avant Art": "La Catedral del Tango",
            "Feria Gastronómica de Palermo": "Parque Tres de Febrero",
        }
        for e in make_events(now):
            place_name = event_place_map.get(e["title"])
            event, created = Event.objects.get_or_create(
                title=e["title"],
                defaults={
                    **{k: v for k, v in e.items() if k != "title"},
                    "place": places.get(place_name) if place_name else None,
                    "status": EventStatus.PUBLISHED,
                },
            )
            if created:
                self.stdout.write(f"  + {event.title}")

        # ── Promotions ────────────────────────────────────────────────────────
        self.stdout.write("Creando promociones...")
        promos = [
            ("Don Julio", "Happy Hour — 2x1 en vinos", "15% en vinos de autor de lunes a jueves de 18 a 20hs.", 15),
            ("Florería Atlántico", "Cóctel de Temporada", "20% de descuento en cócteles de temporada los miércoles.", 20),
            ("MALBA", "Entrada Nocturna — Jueves", "Entrada con 30% de descuento los jueves después de las 18hs.", 30),
            ("Café Tortoni", "Desayuno Porteño", "10% de descuento en el desayuno completo de lunes a viernes antes de las 10hs.", 10),
            ("Club de Tenis Palermo", "Primera Clase Gratis", "Primera clase de tenis o padel sin cargo para nuevos socios.", 100),
        ]
        for place_name, title, desc, discount in promos:
            place = places.get(place_name)
            if place:
                Promotion.objects.get_or_create(
                    place=place,
                    title=title,
                    defaults={
                        "description": desc,
                        "discount_percentage": Decimal(str(discount)),
                        "start_date": now,
                        "end_date": now + timedelta(days=30),
                        "status": "active",
                    },
                )
                self.stdout.write(f"  + {title}")

        counts = {
            "places": Place.objects.count(),
            "activities": Activity.objects.count(),
            "events": Event.objects.filter(status="published").count(),
        }
        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Seed completo: {counts['places']} lugares, "
            f"{counts['activities']} actividades, {counts['events']} eventos publicados."
        ))
