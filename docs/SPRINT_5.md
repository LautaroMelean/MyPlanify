# SPRINT_5.md

# Sprint 5 — Integraciones Externas y Recomendaciones Inteligentes V2

## Estado

```txt
SPRINT_5_STATUS: COMPLETED
```

---

# Objetivo

El objetivo de Sprint 5 es transformar Planify en una plataforma capaz de utilizar información externa real para enriquecer las recomendaciones.

Actualmente el sistema utiliza:

- preferencias del usuario;
- presupuesto;
- cantidad de personas;
- ubicación;
- distancia;
- favoritos;
- eventos internos.

A partir de este sprint el sistema comenzará a utilizar:

- clima real;
- lugares reales desde Google Places;
- información geográfica externa;
- contexto temporal.

---

# Bloque 0 — Decisiones de arquitectura previas

Este bloque debe resolverse antes de escribir código. Define las decisiones estructurales que afectan a todos los bloques siguientes.

---

## Decisión 1 — Proveedor de lugares externos

**Decisión:** Google Places API.

**Costo:** Pay-per-use. El free tier cubre desarrollo y testing. En producción requiere billing configurado en Google Cloud Console.

**Diseño para reemplazo futuro:** El proveedor debe estar completamente encapsulado en:

```txt
backend/apps/integrations/providers/google_places.py
```

El resto del sistema (servicios, endpoints, frontend) no debe conocer que el proveedor es Google. Si en el futuro se reemplaza por OpenStreetMap u otro, solo se modifica ese archivo.

**ADR requerido:** ADR-006.

---

## Decisión 2 — Modelo de datos para lugares externos

**Decisión:** Los lugares externos se persisten en la tabla `places_place` existente usando el campo `source` para distinguir origen.

Flujo:

```txt
Request usuario
→ Buscar en places_place WHERE source='google' AND lat/lon cercano
→ Si hay resultados recientes (< 24h): devolver desde DB
→ Si no: consultar Google Places API → guardar en places_place → devolver
```

Esto permite:
- que los favoritos funcionen igual para lugares internos y externos;
- que los recordatorios, recomendaciones y auditoría no necesiten distinguir el origen;
- reemplazar el proveedor sin cambiar el modelo de datos.

Campo a agregar al modelo `Place`:

```txt
source: CharField  — valores: 'internal', 'google'
external_id: CharField nullable  — place_id de Google
last_synced_at: DateTimeField nullable  — para invalidar cache
```

**ADR requerido:** ADR-006 (incluido).

---

## Decisión 3 — Estrategia de fallback ante APIs externas caídas

El sistema debe funcionar en modo degradado cuando OpenWeather o Google Places no responden.

Comportamiento definido:

| Situación | Comportamiento |
|---|---|
| OpenWeather caído | Recomendaciones sin factor climático. No se muestra widget de clima. |
| Google Places caído | Se sirven solo lugares internos. No se muestra error al usuario. |
| Ambas caídas | Sistema funciona con datos internos únicamente. |
| Timeout (> 3s) | Se cancela la llamada y se usa fallback. |

Implementación:
- Cada provider envuelve sus llamadas en `try/except` con logging de WARNING.
- Los servicios de recomendación reciben el resultado del clima como `Optional` — si es `None`, omiten el factor.

---

## Decisión 4 — Campo score_breakdown en Recommendation

Para mostrar el motivo de recomendación al usuario, el modelo `Recommendation` necesita un campo nuevo:

```txt
score_breakdown: JSONField  — breakdown de factores que influyeron en el score
```

Ejemplo de valor:

```json
{
  "distance": 0.3,
  "preference_match": 0.25,
  "weather": 0.2,
  "budget": 0.15,
  "time_of_day": 0.1
}
```

Esto requiere una migración de base de datos.

**ADR requerido:** ADR-007 (incluido).

---

## Decisión 5 — Ubicación del widget de clima en el frontend

El widget de clima aparece en dos lugares:

1. **Página de Recomendaciones** (`/recomendaciones`) — como contexto antes de las cards.
2. **Página del Mapa** (`/mapa`) — como dato complementario de la ubicación actual.

No aparece en el header global para no saturar la navegación.

---

# Alcance

Sprint 5 incorpora:

## Integraciones externas

- OpenWeather API
- Google Places API (encapsulada para reemplazo futuro)

## Recomendaciones V2

- clima real
- hora actual
- día de la semana
- historial del usuario
- preferencias
- distancia
- motivo de recomendación visible al usuario

## Optimización

- caché Redis para APIs externas
- reducción de llamadas externas
- observabilidad de integraciones

---

# Bloque 1 — Integración OpenWeather

## Objetivo

Obtener clima real según ubicación del usuario.

---

## Datos requeridos

```txt
Temperatura
Sensación térmica
Estado climático (lluvia, sol, nublado, etc.)
Lluvia
Nubes
Viento
Humedad
```

---

## Backend

Crear en la app `integrations` existente:

```txt
backend/apps/integrations/
├── providers/
│   └── openweather.py     ← nuevo
├── services.py            ← actualizar
├── selectors.py           ← actualizar
└── tests/                 ← agregar tests
```

---

## Endpoint

```txt
GET /api/v1/weather/current/?lat={lat}&lon={lon}
```

Respuesta exitosa:

```json
{
  "success": true,
  "data": {
    "temperature": 18,
    "feels_like": 16,
    "condition": "rain",
    "humidity": 85,
    "wind_speed": 12,
    "clouds": 90
  }
}
```

Respuesta con fallback (API caída):

```json
{
  "success": true,
  "data": null
}
```

---

## Cache

Redis:

```txt
Key: weather:{lat_rounded}:{lon_rounded}
TTL: 15 minutos
```

Las coordenadas se redondean a 2 decimales para maximizar hits de cache.

---

## Fallback

Si OpenWeather no responde en 3 segundos o devuelve error:
- Loguear WARNING con el error.
- Devolver `data: null`.
- El motor de recomendaciones continúa sin factor climático.

---

# Bloque 2 — Integración Google Places

## Objetivo

Incorporar lugares reales persistidos en la base de datos propia.

---

## Datos mínimos a guardar

```txt
Nombre
Categoría
Dirección
Latitud / Longitud
Rating
Cantidad de reviews
Website
Teléfono
source = 'google'
external_id = place_id de Google
last_synced_at
```

---

## Backend

Crear:

```txt
backend/apps/integrations/providers/google_places.py
```

Actualizar modelo `Place`:

```txt
Agregar: source, external_id, last_synced_at
Crear migración
```

---

## Endpoints

```txt
GET /api/v1/external/places/?lat={lat}&lon={lon}&radius={m}&type={type}
GET /api/v1/external/places/search/?q={query}&lat={lat}&lon={lon}
```

Ambos endpoints devuelven el mismo formato que los lugares internos para que el frontend no distinga el origen.

---

## Lógica de sincronización

```txt
1. Recibir request con coordenadas
2. Buscar en places_place WHERE source='google' AND distancia < radio AND last_synced_at > NOW()-24h
3. Si hay resultados: devolver desde DB (sin llamar a Google)
4. Si no: llamar Google Places API → upsert en places_place → devolver
```

---

## Cache

Redis adicional para la respuesta cruda de Google (antes de persistir):

```txt
Key: google_places:{lat}:{lon}:{type}
TTL: 24 horas
```

---

## Fallback

Si Google Places no responde:
- Loguear WARNING.
- Devolver lugares internos del área.
- No mostrar error al usuario.

---

## Nota sobre costos

Google Places API es pay-per-use. El free tier ($200/mes de crédito) cubre desarrollo y testing. Para producción configurar billing en Google Cloud Console y monitorear uso. La encapsulación en `providers/google_places.py` permite reemplazar el proveedor en el futuro sin cambios en el resto del sistema.

---

# Bloque 3 — Recomendaciones Inteligentes V2

## Objetivo

Mejorar el motor actual incorporando clima, contexto temporal e historial.

---

## Nuevos factores de scoring

### Clima

```txt
Lluvia o tormenta → penalizar outdoor, favorecer indoor
Sol / despejado   → favorecer outdoor
Frío extremo      → favorecer indoor con calefacción
```

Si el clima no está disponible (API caída) → este factor se omite del score (no penaliza).

---

### Hora del día

```txt
06:00 - 11:59  → cafeterías, parques, actividades matutinas
12:00 - 17:59  → museos, actividades culturales, plazas
18:00 - 23:59  → bares, cine, eventos nocturnos, restaurantes
```

---

### Día de la semana

```txt
Lunes a jueves  → actividades cortas (< 2h), lugares cercanos
Viernes         → balance corto/largo
Sábado a domingo → actividades largas, planes completos
```

---

### Historial del usuario

Aumentar score según interacciones previas:

```txt
favorite        → +0.25
create_reminder → +0.20
recommendation_click → +0.15
view            → +0.05
unfavorite      → -0.10
```

---

## Score V2 — breakdown

El score final se compone de:

```txt
distance          → 30%
preference_match  → 25%
weather           → 20% (0% si API caída)
budget            → 15%
time_of_day       → 10%
```

Cuando el clima no está disponible, los porcentajes restantes se redistribuyen proporcionalmente.

El breakdown se guarda en `Recommendation.score_breakdown` (JSONField).

---

## Documentación

Actualizar:

```txt
docs/ARCHITECTURE.md
docs/DATA_MODEL.md
```

ADR requerido: ADR-007.

---

# Bloque 4 — Historial Inteligente

## Objetivo

Mejorar el registro de interacciones del usuario para alimentar el scoring V2.

**Nota:** `log_interaction` ya existe en `recommendations/views.py` y el módulo `audit` ya registra acciones. Este bloque extiende lo existente, no lo reemplaza.

---

## Eventos a registrar (nuevos o no registrados aún)

Verificar cuáles ya existen y agregar los faltantes:

```txt
view_place             ← verificar si existe
view_event             ← verificar si existe
view_activity          ← verificar si existe
favorite               ← verificar si existe
unfavorite             ← agregar si falta
create_reminder        ← verificar si existe
search                 ← agregar si falta
recommendation_click   ← agregar si falta
```

---

## Auditoría

Todos los eventos nuevos deben pasar por `apps.audit.services.log_action` para mantener trazabilidad.

---

# Bloque 5 — Frontend

## Widget de clima

**Aparece en:**
- `/recomendaciones` — antes de las cards de recomendación, como contexto.
- `/mapa` — como dato complementario de la ubicación actual.

**No aparece en:** header global.

**Muestra:**
```txt
Temperatura actual
Sensación térmica
Estado (ícono + texto)
```

**Si la API está caída:** el widget no se renderiza (no muestra error).

---

## Lugares externos

Los lugares de Google Places aparecen en la sección `/explorar` existente, mezclados con los internos. El frontend no distingue el origen — ambos tienen el mismo formato de respuesta.

No se crea una sección nueva separada para lugares externos.

---

## Motivo de recomendación

En cada card de recomendación mostrar los factores principales que influyeron en el score.

Ejemplo visual:

```txt
┌─────────────────────────────┐
│  Parque Centenario          │
│  ⭐ 4.5 · 2.3 km            │
│                             │
│  Te lo recomendamos porque: │
│  ✔ Está cerca               │
│  ✔ Coincide con tus gustos  │
│  ✔ Hace buen tiempo         │
└─────────────────────────────┘
```

Los motivos se derivan del `score_breakdown` recibido del backend.

---

# Bloque 6 — Testing

## Backend

```txt
OpenWeather provider (mock de requests HTTP)
Google Places provider (mock de requests HTTP)
Fallback cuando API retorna error
Fallback cuando API hace timeout
Cache Redis (hit y miss)
Scoring V2 con clima disponible
Scoring V2 sin clima (fallback)
Endpoints /api/v1/weather/current/
Endpoints /api/v1/external/places/
Permisos de los nuevos endpoints
```

---

## Frontend

```txt
Weather widget — renderiza con datos
Weather widget — no renderiza si data es null
Motivo de recomendación — muestra factores correctos
Lugares externos — se integran en /explorar sin distinción visual
```

---

# Bloque 7 — Seguridad

Validar:

```txt
Rate limiting en endpoints de clima y lugares externos
API Keys nunca expuestas en respuestas ni logs
Timeouts de 3s en todas las llamadas externas
Retries máximo 1 vez ante falla de red (no ante error 4xx)
Logs de WARNING ante fallas externas (nunca loguear la API key)
Validación de lat/lon en todos los endpoints que los reciben
```

---

# Bloque 8 — Documentación

Actualizar:

```txt
docs/ARCHITECTURE.md  — integraciones externas, scoring V2, fallback
docs/DATA_MODEL.md    — campos nuevos en Place y Recommendation
docs/API_GUIDELINES.md — nuevos endpoints
agents/ORCHESTRATOR.md — sprint status
```

---

Crear ADRs:

```txt
ADR-005 — OpenWeather como proveedor de clima
ADR-006 — Google Places como proveedor de lugares (encapsulado para reemplazo)
ADR-007 — Motor de Recomendaciones V2 con score_breakdown
```

---

# Checklist de aceptación

## Integraciones

- [ ] OpenWeather devuelve clima real según coordenadas
- [ ] OpenWeather con fallback correcto cuando API falla
- [ ] Google Places persiste lugares en `places_place`
- [ ] Google Places con fallback correcto cuando API falla
- [ ] Cache Redis funcionando para ambas APIs

## Backend

- [ ] Migración de Place (source, external_id, last_synced_at)
- [ ] Migración de Recommendation (score_breakdown)
- [ ] Nuevos endpoints documentados y funcionando
- [ ] Scoring V2 implementado con todos los factores
- [ ] Historial de interacciones completo
- [ ] Tests pasando con mocks de APIs externas
- [ ] Auditoría de nuevos eventos

## Frontend

- [ ] Widget de clima en /recomendaciones y /mapa
- [ ] Widget no se renderiza si clima no disponible
- [ ] Lugares externos visibles en /explorar
- [ ] Motivo de recomendación visible en cards
- [ ] Tests de nuevos componentes

## Documentación

- [ ] ADR-005, ADR-006, ADR-007 creados
- [ ] ARCHITECTURE.md actualizado
- [ ] DATA_MODEL.md actualizado

---

# Fuera de alcance

No implementar:

```txt
Reservas
Pagos
Suscripciones
Chat
IA generativa
Planes compartidos
Ticketmaster API (Sprint 6+)
Google Calendar (Sprint 6+)
```

---

# Resultado esperado

Al finalizar Sprint 5:

```txt
PLANIFY_STATUS: REAL_WORLD_DATA_ENABLED
```

---

# Próximo Sprint

```txt
SPRINT_6
Planes personalizados y organización inteligente de actividades
```
