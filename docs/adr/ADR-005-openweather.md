# ADR-005 — OpenWeather como proveedor de clima

## Estado

Aprobado — Sprint 5

## Contexto

El motor de recomendaciones necesita datos climáticos reales para ajustar el scoring (penalizar outdoor en lluvia, favorecer indoor, etc.). Se evaluó usar datos estáticos de clima, scraping, o una API real.

## Decisión

Usar OpenWeather API (endpoint `/data/2.5/weather`) encapsulado en `apps/integrations/providers/openweather.py`.

- Timeout: 3s. Si la API no responde, el provider retorna `None`.
- Caché Redis: key `weather:{lat_r}:{lon_r}`, TTL 15 minutos. Las coordenadas se redondean a 2 decimales para maximizar hits.
- Fallback: cuando el provider retorna `None`, el motor de recomendaciones omite el factor climático del scoring. El endpoint público retorna `data: null`. El widget de clima en el frontend no se renderiza.
- La API key nunca se loguea. Los logs de error solo incluyen coordenadas y mensaje de excepción.
- Endpoint público: `GET /api/v1/weather/current/?lat=&lon=`

## Consecuencias

- El sistema funciona sin API key configurada (degrada gracefully).
- El widget de clima en `/recomendaciones` y `/mapa` solo aparece cuando hay ubicación del usuario y la API responde.
- Reemplazar el proveedor requiere solo modificar `providers/openweather.py` y actualizar este ADR.
