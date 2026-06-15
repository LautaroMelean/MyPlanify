# ADR-015 — Export de Plan a Calendario

## Estado

ACCEPTED — Sprint 9

## Contexto

Los usuarios necesitan llevar los ítems de su plan a su calendario real para maximizar la probabilidad de ejecución.

## Decisión

**El archivo .ics y el link de Google Calendar se generan completamente en el frontend.**

No se agrega ningún endpoint backend para esta funcionalidad.

## Razonamiento

Los datos necesarios (plan.date, items, slots, generation_reason) ya están disponibles en el cliente desde `GET /api/v1/plans/{id}/`. Generar el .ics en frontend reduce latencia, evita una solicitud de red adicional y mantiene el backend sin dependencias de formato de calendario.

## Mapeo de slots a horas

```
morning   → 09:00 – 11:00
afternoon → 14:00 – 16:00
evening   → 20:00 – 22:00
```

Horas fijas son suficientes para MVP. Alternativa rechazada: horas configurables por el usuario — agrega complejidad de UX sin evidencia de demanda.

## Google Calendar deep link

Se genera un link `https://calendar.google.com/calendar/render?action=TEMPLATE&...` con el primer ítem del plan. El usuario puede repetir el proceso para ítems adicionales.

Alternativa rechazada: exportar el plan completo como un único evento de día completo. Pierde la granularidad de los slots y hace que el calendario no refleje las horas reales de las actividades.

## Consecuencias

- El .ics sigue el estándar RFC 5545 y es compatible con Google Calendar, Apple Calendar y Outlook.
- Si en el futuro se necesita exportación masiva o sincronización automática, se deberá agregar un endpoint backend.
