# ADR-006 — Google Places como proveedor de lugares externos

## Estado

Aprobado — Sprint 5

## Contexto

Para mostrar lugares reales (no solo los cargados manualmente) se necesita un proveedor de datos de lugares. Se evaluó OpenStreetMap (gratuito pero datos menos completos) y Google Places (pay-per-use, datos más ricos).

## Decisión

Usar Google Places API (Nearby Search + Text Search) encapsulado en `apps/integrations/providers/google_places.py`.

**Diseño para reemplazo futuro:** el resto del sistema (servicios, endpoints, frontend) no conoce que el proveedor es Google. Si en el futuro se reemplaza, solo se modifica ese archivo.

**Modelo de datos:** los lugares externos se persisten en la tabla `places_place` existente usando:
- `source = 'google'` para distinguir origen.
- `external_id` = place_id de Google.
- `last_synced_at` para invalidación de caché.

**Flujo de sincronización:**
1. Buscar en DB `source='google'` con `last_synced_at > NOW()-24h` dentro del radio.
2. Si hay resultados recientes: devolver desde DB (sin llamar a Google).
3. Si no: llamar Google Places → `update_or_create` por `external_id` → devolver.

**Caché Redis adicional:** key `google_places:{lat}:{lon}:{radius}:{type}`, TTL 24h para la respuesta cruda.

**Timeout:** 3s. Si la API no responde, se sirven solo lugares internos.

**Costo:** pay-per-use. El free tier de Google Cloud ($200/mes de crédito) cubre desarrollo y testing. Producción requiere billing configurado.

## Consecuencias

- Los favoritos, recordatorios y recomendaciones funcionan igual para lugares internos y externos.
- El frontend no distingue el origen (mismo formato de respuesta).
- El sistema degrada gracefully cuando la API de Google no está disponible.
- Reemplazar el proveedor en el futuro no requiere cambios en el modelo de datos ni en el frontend.
