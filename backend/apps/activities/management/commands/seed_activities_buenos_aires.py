"""
Seed de actividades curadas para Buenos Aires.
Cubre cultura, aire libre, deportes, tango, entretenimiento y gastronomía experiencial.
"""
from django.core.management.base import BaseCommand
from apps.activities.models import Activity, ActivityType

CITY = "Buenos Aires"

# (name, description, category, activity_type, min_budget, max_budget, min_people, max_people, indoor, outdoor, score_base)
ACTIVITIES = [
    # ─── Museos y cultura ────────────────────────────────────────────────────
    (
        "Visita al MALBA",
        "Recorrido por el Museo de Arte Latinoamericano de Buenos Aires, con colección permanente de artistas como Frida Kahlo, Diego Rivera y Xul Solar. Exposiciones temporales todo el año.",
        "Museo", ActivityType.MUSEUM, 1200, 2500, 1, 20, True, False, 88,
    ),
    (
        "Museo Nacional de Bellas Artes",
        "Entrada gratuita al museo más importante del país. Obras de Rembrandt, Rodin, Goya, y la colección argentina más grande del mundo. En el corazón de Recoleta.",
        "Museo", ActivityType.MUSEUM, 0, 0, 1, 30, True, False, 85,
    ),
    (
        "MAMBA — Museo de Arte Moderno",
        "Arte contemporáneo argentino e internacional en San Telmo. Colección de más de 7.000 obras, con exposiciones que rotan frecuentemente. Edificio industrial reciclado con onda.",
        "Museo", ActivityType.MUSEUM, 600, 1500, 1, 20, True, False, 82,
    ),
    (
        "Planetario Galileo Galilei",
        "Shows astronómicos en la cúpula proyectable del Planetario de Palermo. Ideal para ir con amigos o curiosos del universo. Rodea un lago precioso en el parque.",
        "Cultura", ActivityType.MUSEUM, 500, 1200, 1, 15, True, False, 80,
    ),
    (
        "Museo Histórico Nacional",
        "Recorre la historia argentina desde la Revolución de Mayo hasta la actualidad. En el Parque Lezama de San Telmo, uno de los barrios más pintorescos de BA.",
        "Museo", ActivityType.MUSEUM, 0, 500, 1, 20, True, False, 72,
    ),
    (
        "Museo de Ciencias Naturales Bernardino Rivadavia",
        "Dinosaurios, meteoritos y colecciones de historia natural en el corazón del Parque Centenario. Entrada libre los domingos. Ideal para curiosos de todas las edades.",
        "Museo", ActivityType.MUSEUM, 0, 800, 1, 20, True, False, 75,
    ),
    (
        "Museo Xul Solar",
        "La casa-museo del excéntrico artista Xul Solar, amigo de Borges y genio visionario. Obras surrealistas únicas en el mundo, en un petit hotel de Palermo.",
        "Museo", ActivityType.MUSEUM, 800, 1500, 1, 15, True, False, 78,
    ),
    (
        "El Ateneo Grand Splendid",
        "Una de las librerías más bellas del mundo, instalada en un teatro de 1919 en Recoleta. Los palcos son rincones de lectura. Imprescindible aunque no compres nada.",
        "Cultura", ActivityType.TOURISM, 0, 2000, 1, 10, True, False, 90,
    ),
    (
        "Tour por el Teatro Colón",
        "Visita guiada al teatro de ópera más importante de Latinoamérica y uno de los mejores del mundo. Arquitectura imponente, acústica perfecta e historia en cada rincón.",
        "Cultura", ActivityType.TOURISM, 2500, 5000, 1, 20, True, False, 92,
    ),
    (
        "CCK — Centro Cultural Kirchner",
        "El centro cultural más grande de Latinoamérica, instalado en el antiguo Correo Central. Exposiciones de arte, música en vivo, teatro y la ballena azul. Entrada libre.",
        "Cultura", ActivityType.CONCERT, 0, 500, 1, 30, True, False, 87,
    ),
    (
        "Usina del Arte",
        "Complejo cultural en La Boca con conciertos clásicos, jazz y música experimental. El edificio es una usina de 1916 reciclada como espacio artístico de vanguardia.",
        "Cultura", ActivityType.CONCERT, 0, 3000, 1, 20, True, False, 83,
    ),
    (
        "Fundación PROA (La Boca)",
        "Galería de arte contemporáneo en La Boca con las mejores exposiciones temporales de Buenos Aires. Terraza con vista al Riachuelo. Entrada accesible.",
        "Cultura", ActivityType.MUSEUM, 800, 2000, 1, 20, True, False, 82,
    ),
    (
        "Café Tortoni",
        "El café más antiguo y famoso de Buenos Aires (1858), en Avenida de Mayo. Shows de tango nocturnos, billares y una atmósfera de otro siglo. Turístico pero auténtico.",
        "Café", ActivityType.RESTAURANT, 1500, 4000, 1, 10, True, False, 80,
    ),
    (
        "Confitería Las Violetas",
        "Café histórico en Almagro (1884) con vitrales, mármoles y una carta de facturas y tortas que no tiene rival. El desayuno porteño perfecto.",
        "Café", ActivityType.RESTAURANT, 1200, 3000, 1, 8, True, False, 77,
    ),

    # ─── Aire libre y parques ────────────────────────────────────────────────
    (
        "Reserva Ecológica Costanera Sur",
        "Caminata o bicicleta por la reserva natural más grande de CABA, a metros del centro. Más de 300 especies de aves, laguna, y la mejor vista del skyline porteño al atardecer.",
        "Parque", ActivityType.PARK, 0, 0, 1, None, False, True, 92,
    ),
    (
        "Parque Tres de Febrero (Bosques de Palermo)",
        "El pulmón verde de Buenos Aires: lagos para remar, pérgola de las rosas, pista de patinaje y decenas de actividades al aire libre. Ideal para una tarde de domingo.",
        "Parque", ActivityType.PARK, 0, 1500, 1, None, False, True, 88,
    ),
    (
        "Jardín Japonés de Buenos Aires",
        "El jardín japonés más grande fuera de Japón, en el corazón de Palermo. Peces koi, puentes, pabellones y una casa de té auténtica. Muy tranquilo y fotogénico.",
        "Parque", ActivityType.PARK, 1000, 2000, 1, 10, False, True, 86,
    ),
    (
        "Jardín Botánico Carlos Thays",
        "Más de 5.500 especies de plantas en 7 hectáreas en el centro de Palermo. Jardines temáticos por continente, invernadero, esculturas y gatos en libertad. Entrada libre.",
        "Parque", ActivityType.PARK, 0, 0, 1, None, False, True, 84,
    ),
    (
        "Parque Centenario",
        "El parque favorito de Caballito: anfiteatro al aire libre, pérgola, laguna con patos y ferias los fines de semana. Vida de barrio genuina de Buenos Aires.",
        "Parque", ActivityType.PARK, 0, 500, 1, None, False, True, 78,
    ),
    (
        "Parque Lezama (San Telmo)",
        "El parque más histórico de Buenos Aires, con esculturas, anfiteatro y vista al Riachuelo. A metros de la Feria de San Telmo, perfecto para combinar.",
        "Parque", ActivityType.PARK, 0, 0, 1, None, False, True, 75,
    ),
    (
        "Paseo por la Costanera Norte",
        "Caminar o andar en bici por la costanera del Río de la Plata: viento, mar marrón, puestas de sol épicas y parrillas populares. La versión popular del río.",
        "Parque", ActivityType.PARK, 0, 2000, 1, None, False, True, 72,
    ),

    # ─── Deportes y actividades físicas ──────────────────────────────────────
    (
        "Tour en bicicleta por Palermo (EcoBici)",
        "Explorá Palermo en bicicleta usando las EcoBici (sistema público). Pasás por el Botánico, el Japonés, la Reserva y la Costa. Gratis con registro o con tour privado.",
        "Deporte", ActivityType.SPORTS, 0, 2000, 1, 8, False, True, 88,
    ),
    (
        "Kayak en el Río de la Plata",
        "Sesión de kayak con instructores en el Delta del Tigre o la Costanera Sur. Una perspectiva única de Buenos Aires desde el agua. Para principiantes y avanzados.",
        "Deporte", ActivityType.SPORTS, 4000, 9000, 1, 8, False, True, 85,
    ),
    (
        "Clase de escalada en búlder (Boulder World)",
        "Escalada en bloque sin arnés en el rocodromo cubierto más grande de BA. No necesitás experiencia previa. Alquilan calzado y hay instructores para principiantes.",
        "Deporte", ActivityType.SPORTS, 3000, 5000, 1, 6, True, False, 82,
    ),
    (
        "Running en Parque Tres de Febrero",
        "Una vuelta al lago del parque son unos 4km, con lindas vistas y mucha gente activa. Sábados hay grupos de running libres. El ambiente es relajado y motivador.",
        "Deporte", ActivityType.SPORTS, 0, 0, 1, 10, False, True, 70,
    ),
    (
        "Yoga al aire libre en Palermo",
        "Clases de yoga gratis o muy económicas en el Parque Tres de Febrero los fines de semana. Instructores voluntarios, cualquier nivel. Llevás tu mat y listo.",
        "Deporte", ActivityType.SPORTS, 0, 1000, 1, 20, False, True, 75,
    ),
    (
        "Fútbol 5 en Buenos Aires",
        "Hay canchitas de fútbol 5 en todos los barrios. Podés armar un partido con amigos o unirte a grupos abiertos. La actividad social más popular de Buenos Aires.",
        "Deporte", ActivityType.SPORTS, 2000, 5000, 5, 10, False, True, 80,
    ),
    (
        "Clase de surf en Costanera",
        "Clases de standup paddle (SUP) en el Río de la Plata. Instructores certificados, equipos incluidos. Ideal para probar algo nuevo un sábado a la mañana.",
        "Deporte", ActivityType.SPORTS, 3500, 7000, 1, 6, False, True, 78,
    ),

    # ─── Tango y cultura porteña ─────────────────────────────────────────────
    (
        "Clase de tango nivel principiante",
        "Una hora de clase de tango con pareja o solo — te asignan compañero. Los mejores estudios están en San Telmo y Palermo. Después de la clase, podés quedarte al milonga.",
        "Cultura", ActivityType.CONCERT, 2000, 5000, 1, None, True, False, 92,
    ),
    (
        "Milonga en La Catedral (Almagro)",
        "La milonga más auténtica de Buenos Aires, en un depósito reciclado de Almagro. Ambiente under y genuino, no turístico. Jueves a domingo desde las 23h. Reservar lugar.",
        "Entretenimiento", ActivityType.CONCERT, 1500, 3000, 1, None, True, False, 90,
    ),
    (
        "Show de tango en San Telmo",
        "Espectáculo de tango profesional en los bares históricos de San Telmo. Bailarines, cantor y orquesta en vivo. Incluye cena opcional. El clásico de Buenos Aires.",
        "Entretenimiento", ActivityType.CONCERT, 5000, 15000, 1, None, True, False, 85,
    ),
    (
        "Tour de murales y graffiti en Palermo",
        "Recorrido guiado a pie por el Soho de Palermo viendo los mejores murales urbanos de artistas argentinos e internacionales. Gratuito o con tour privado. 2hs aprox.",
        "Turismo", ActivityType.TOURISM, 0, 3000, 1, 15, False, True, 85,
    ),
    (
        "Recorrido de conventillos en San Telmo",
        "Caminata por las calles más antiguas de Buenos Aires: el Zanjón de Granados, la Casona de Garay y los conventillos. La historia viva de la inmigración porteña.",
        "Turismo", ActivityType.TOURISM, 0, 4000, 1, 15, False, True, 82,
    ),
    (
        "Tour gastronómico en San Telmo",
        "Un guía te lleva por los puestos más sabrosos del Mercado de San Telmo y sus alrededores: empanadas, choripán, vinos y dulce de leche. 2hs caminando y comiendo.",
        "Turismo", ActivityType.TOURISM, 5000, 12000, 2, 12, False, True, 87,
    ),
    (
        "Recorrido arquitectónico por el Centro",
        "Tour a pie por el microcentro porteño: el Cabildo, la Casa Rosada, la Manzana de las Luces y los pasajes históricos. La mejor forma de conocer la historia de la ciudad.",
        "Turismo", ActivityType.TOURISM, 0, 3000, 1, 20, False, True, 80,
    ),

    # ─── Mercados y ferias ────────────────────────────────────────────────────
    (
        "Feria de San Telmo (domingo)",
        "La feria más famosa de Buenos Aires, todos los domingos en Defensa. Antigüedades, artesanías, artistas callejeros y el mejor ambiente de la ciudad. No te la perdés.",
        "Turismo", ActivityType.TOURISM, 0, 5000, 1, None, False, True, 93,
    ),
    (
        "Mercado de San Telmo",
        "El mercado más antiguo de Buenos Aires (1897): puestos de comida, vinos, quesos, carnicerías gourmet y galerías de arte en el mismo espacio. De jueves a domingo.",
        "Turismo", ActivityType.TOURISM, 1000, 5000, 1, None, True, False, 88,
    ),
    (
        "Feria de Mataderos (domingo)",
        "La feria más folclórica de Buenos Aires: artesanías regionales, locro, asado, folklore, payadores y danzas gauchas. En el barrio de Mataderos, auténtico y popular.",
        "Turismo", ActivityType.TOURISM, 500, 4000, 1, None, False, True, 85,
    ),
    (
        "Mercado del Progreso (Caballito)",
        "El mercado barrial más completo de Buenos Aires: verdulería, pescadería, especias, empanadas y la mejor picada del barrio. Ambiente 100% local, sin turistas.",
        "Gastronomía", ActivityType.RESTAURANT, 500, 3000, 1, 6, True, False, 75,
    ),
    (
        "Feria artesanal de Plaza Francia (Recoleta)",
        "Artesanos locales con joyería, cuero, textiles y arte todos los fines de semana frente al MNBA. El plan de domingo de media tarde en Recoleta.",
        "Turismo", ActivityType.TOURISM, 0, 3000, 1, None, False, True, 78,
    ),
    (
        "Mercado de Pulgas de Colegiales",
        "Antigüedades, vinilo, libros usados y objetos vintage en el mercado de pulgas más porteño de la ciudad. Abierto los fines de semana. A veces hay shows en vivo.",
        "Entretenimiento", ActivityType.TOURISM, 0, 4000, 1, None, True, False, 80,
    ),

    # ─── Entretenimiento indoor ──────────────────────────────────────────────
    (
        "Escape room en Buenos Aires",
        "Resolvé enigmas en equipo con hasta 8 personas en uno de los mejores escape rooms de la ciudad. Temáticas variadas: terror, aventura, detective. 60 minutos de adrenalina.",
        "Entretenimiento", ActivityType.GAMING, 4000, 10000, 2, 8, True, False, 88,
    ),
    (
        "Bowling en Palermo",
        "Bowling en el corazón de Palermo: pistas iluminadas con luz negra, música y hamburguesería integrada. Perfecto para grupos de amigos. Reservar los fines de semana.",
        "Entretenimiento", ActivityType.GAMING, 3000, 7000, 2, 8, True, False, 80,
    ),
    (
        "Laser tag en Buenos Aires",
        "Batalla de laser tag en arenas especialmente diseñadas. Una hora de juego estratégico en equipo. Hay varios locales en Palermo y Caballito.",
        "Entretenimiento", ActivityType.GAMING, 2500, 5000, 2, 16, True, False, 78,
    ),
    (
        "Arcade de videojuegos retro",
        "Arcades con maquinitas clásicas de los 90 en varios spots de Palermo y Villa Crespo. Pinball, Street Fighter, Neo-Geo. Una tarde de nostalgia pura.",
        "Entretenimiento", ActivityType.GAMING, 1000, 3000, 1, 6, True, False, 75,
    ),
    (
        "Bar de juegos de mesa",
        "Bares con cientos de juegos de mesa en Palermo y San Telmo: Catan, Dixit, Codenames, Pandemic. Pedís un trago y jugás horas. Perfecto para grupos.",
        "Entretenimiento", ActivityType.GAMING, 3000, 8000, 2, 10, True, False, 82,
    ),

    # ─── Shows y espectáculos ─────────────────────────────────────────────────
    (
        "Stand-up comedy en Buenos Aires",
        "Buenos Aires tiene una de las mejores escenas de stand-up del mundo hispanohablante. Theatres y boliches en Palermo y San Telmo todas las noches. Muy económico.",
        "Entretenimiento", ActivityType.CONCERT, 1500, 5000, 1, None, True, False, 88,
    ),
    (
        "Teatro independiente en Buenos Aires",
        "La escena teatral porteña es de las más activas del mundo. Centenares de obras independientes cada semana en salas de 50 personas. Una experiencia única.",
        "Cultura", ActivityType.CONCERT, 2000, 6000, 1, None, True, False, 85,
    ),
    (
        "Show de humor musical (Fuerza Bruta / similar)",
        "Espectáculos inmersivos de circo, teatro y música en vivo. Fuerza Bruta es el más conocido a nivel mundial pero hay muchas propuestas similares en CABA.",
        "Entretenimiento", ActivityType.CONCERT, 8000, 18000, 1, None, True, False, 90,
    ),
    (
        "Cine en sala (Cinemark Hoyts Palermo)",
        "Una película en el Cinemark de Palermo o el Village Recoleta con palomitas y la mejor butaca. Ideal para un plan relajado en cualquier día de la semana.",
        "Entretenimiento", ActivityType.CINEMA, 2500, 5000, 1, 6, True, False, 72,
    ),

    # ─── Gastronomía experiencial ─────────────────────────────────────────────
    (
        "Tour de pizza en pizzerías históricas",
        "Un recorrido por las mejores pizzerías de Buenos Aires: El Cuartito, Güerrín, Las Cuartetas. Media masa, fugazzeta y muzarela. El ritual más porteño de todos.",
        "Gastronomía", ActivityType.RESTAURANT, 2500, 6000, 1, 6, True, False, 88,
    ),
    (
        "Brunch en el Mercado de San Telmo",
        "Jueves a domingo, el mercado ofrece el mejor brunch de Buenos Aires: tostadas con palta, jugo de naranja, café de especialidad y medialunas recién horneadas.",
        "Gastronomía", ActivityType.RESTAURANT, 2000, 5000, 1, 6, True, False, 82,
    ),
    (
        "Picada en bodegón histórico",
        "Una picada de salame, queso, aceitunas y vino en uno de los bodegones históricos de San Telmo o el Centro. La versión porteña del aperitivo italiano.",
        "Gastronomía", ActivityType.RESTAURANT, 3000, 8000, 2, 8, True, False, 85,
    ),
    (
        "Cata de vinos en bodega urbana",
        "Varias bodegas y vinotecas en Palermo y San Telmo ofrecen catas con maridaje. Aprendés de uvas argentinas mientras probás 5 o 6 variedades. 90 minutos.",
        "Gastronomía", ActivityType.RESTAURANT, 5000, 12000, 1, 10, True, False, 87,
    ),
    (
        "Café de especialidad en Palermo",
        "Palermo tiene la mejor escena de café de especialidad de Argentina: Lattente, Felicidad, Ninina. Un flat white bien hecho y croissant de manteca. La mañana perfecta.",
        "Café", ActivityType.RESTAURANT, 800, 2500, 1, 4, True, False, 80,
    ),
    (
        "Asado en parrilla tradicional (La Brigada / Don Julio)",
        "Un asado en una de las mejores parrillas de Buenos Aires: bife de chorizo, chorizo, morcilla y vino Malbec. La experiencia gastronómica más argentina que existe.",
        "Gastronomía", ActivityType.RESTAURANT, 8000, 20000, 1, 8, True, False, 93,
    ),

    # ─── Noche porteña ────────────────────────────────────────────────────────
    (
        "Bar de jazz en San Telmo",
        "Thelonious, Notorious o el Café Vinilo — los mejores bares de jazz en vivo de Buenos Aires. Música en vivo de jueves a sábado, tragos artesanales y ambiente íntimo.",
        "Bar", ActivityType.BAR, 3000, 8000, 1, None, True, False, 88,
    ),
    (
        "Cervecería artesanal en Palermo",
        "Palermo tiene decenas de cervecerías artesanales con variedad de estilos. Antares, Buller, Pepita La Pistolera — pinta de IPA o stout con picada. El plan de los jueves.",
        "Bar", ActivityType.BAR, 3000, 8000, 1, None, True, True, 85,
    ),
    (
        "Cócteles en Palermo Hollywood",
        "La calle Fitz Roy y alrededores concentran los mejores bares de cócteles de BA: Florería Atlántico, Presidente Bar. Bartenders premiados y tragos únicos.",
        "Bar", ActivityType.BAR, 5000, 12000, 1, 6, True, False, 87,
    ),
    (
        "Karaoke en Buenos Aires",
        "Karaoke privado o grupal en varios spots de Palermo y Villa Crespo. Cuartos privados con micrófono, pantalla y bebidas. Una noche distinta y muy divertida con amigos.",
        "Entretenimiento", ActivityType.GAMING, 4000, 10000, 2, 12, True, False, 82,
    ),
    (
        "Bares de Puerto Madero de noche",
        "Puerto Madero de noche: bares con vista al Río de la Plata, dique iluminado y la skyline de la ciudad de fondo. Más tranquilo que Palermo, más exclusivo.",
        "Bar", ActivityType.BAR, 5000, 15000, 1, None, True, True, 78,
    ),
]


class Command(BaseCommand):
    help = "Seed de actividades curadas para Buenos Aires"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for row in ACTIVITIES:
            (name, description, category, activity_type,
             min_budget, max_budget, min_people, max_people,
             indoor, outdoor, score_base) = row

            obj, is_new = Activity.objects.update_or_create(
                name=name,
                city=CITY,
                defaults={
                    "description": description,
                    "category": category,
                    "activity_type": activity_type,
                    "min_budget": min_budget,
                    "max_budget": max_budget,
                    "min_people": min_people,
                    "max_people": max_people,
                    "indoor": indoor,
                    "outdoor": outdoor,
                    "score_base": score_base,
                    "is_active": True,
                    "place": None,
                },
            )
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Activities Buenos Aires: {created} creadas, {updated} actualizadas. Total: {created + updated}."
            )
        )
