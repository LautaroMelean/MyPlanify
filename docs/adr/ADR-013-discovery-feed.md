# ADR-013 — Feed de Descubrimiento (Trending Plans)

## Estado

ACCEPTED — Sprint 9

## Contexto

Sprint 9 introduce un feed de planes públicos ordenados por popularidad para fomentar el descubrimiento y el sentido de comunidad. Era necesario decidir el mecanismo de ranking y la fuente de datos.

## Decisión

**Ranking por score = (vistas × 1) + (compartidos × 3)**

Los conteos se calculan en tiempo real desde `InteractionHistory` filtrando por `action="plan_viewed"` y `action="plan_shared"` sobre el período seleccionado (today / weekend / week).

Solo aparecen planes con `is_public=True` y al menos 1 ítem.

El usuario autenticado no ve sus propios planes en el feed (exclusión por `exclude_user`).

## Alternativas rechazadas

- **Curación manual**: requiere moderación humana, no escala y agrega complejidad operativa.
- **Contador dedicado en Plan**: evitaría recalcular desde InteractionHistory pero duplicaría datos y agregaría complejidad al modelo. En Sprint 9 el volumen es bajo — los recuentos en vivo son suficientes.
- **Algoritmo de decay temporal (Hacker News style)**: aumenta la complejidad sin evidencia de que sea necesario en esta etapa. Se puede migrar en Sprint 10+ si el volumen lo justifica.

## Consecuencias

- `GET /api/v1/plans/trending/` es `AllowAny` — los usuarios no autenticados también pueden ver el feed para incentivar el registro.
- Si el volumen de planes crece significativamente, se deberá cachear el resultado o migrar los contadores a campos denormalizados en `Plan`.
