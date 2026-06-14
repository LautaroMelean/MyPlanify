# ADR-007 — Motor de Recomendaciones V2 con score_breakdown

## Estado

Aprobado — Sprint 5

## Contexto

El motor V1 (Sprint 2-3) calcula un score numérico pero no lo expone de forma estructurada. Para que el usuario entienda por qué se le recomienda algo, se necesita un desglose de factores. Además, V1 no considera el día de la semana ni distingue el tipo de interacción del usuario.

## Decisión

### Campo score_breakdown

Agregar `score_breakdown: JSONField` al modelo `Recommendation`. Almacena la contribución numérica de cada factor al score final:

```json
{
  "preference": 40.0,
  "popularity": 7.5,
  "interaction": 2.5,
  "weather": 8.0,
  "distance": 10.0,
  "budget": 10.0,
  "time_of_day": 5.0,
  "day_of_week": 5.0
}
```

### Nuevos factores V2

**Día de la semana (`day_of_week_modifier`):**
- Fin de semana (Sáb/Dom): +5 para outdoor, museos, parques, turismo.
- Semana (Lun-Jue): +3 para cafés, bares, restaurantes (salidas cortas).

**Interacciones ponderadas por tipo (`interaction_score_v2`):**
- `favorite` → +0.25
- `create_reminder` → +0.20
- `recommendation_click` → +0.15
- `view` → +0.05
- `unfavorite` → -0.10

V1 solo verificaba si había alguna interacción (binario). V2 acumula pesos por tipo.

### Nuevas interacciones registradas

- `unfavorite`: al eliminar un favorito (en `favorites/services.py`).
- `create_reminder`: al crear un recordatorio (en `notifications/services.py`).
- `recommendation_click`: endpoint `POST /api/v1/recommendations/click/`.

### Razones en el frontend

El `score_breakdown` se expone en el serializer. El frontend deriva etiquetas legibles para el usuario (ej: "Coincide con tus gustos", "Está cerca de vos", "Ideal para el clima actual").

## Consecuencias

- Registros de `Recommendation` previos tienen `score_breakdown = {}` (JSONField default). El frontend lo maneja mostrando el texto plano `recommendation_reason` como fallback.
- El motor V2 usa `openweather_provider` (con caché Redis) en vez de llamar directamente a OpenWeather, reduciendo latencia en generación de recomendaciones.
- Agregar nuevos factores en el futuro solo requiere modificar `services.py` y el dict de breakdown.
