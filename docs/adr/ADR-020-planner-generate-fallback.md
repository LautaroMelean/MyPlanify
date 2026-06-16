# ADR-020 — Fallback progresivo en `generate_plan()`

**Fecha:** 2026-06-16  
**Estado:** Aceptado  
**Sprint:** 12

---

## Contexto

`generate_plan()` (el endpoint que usa el PlannerForm cuando el usuario elige fecha, ciudad y presupuesto) solo ejecutaba **fase 1**: filtros estrictos de `city + budget_per_slot + people_count`.

Síntoma observado: al seleccionar ciudades sin datos propios en la DB (Córdoba, Rosario, etc.), el planner generaba un plan con 0 ítems. El usuario veía "Este plan no tiene ítems aún" sin ninguna explicación.

Paradójicamente, `generate_surprise_plan()` ya tenía relajación progresiva de 3 fases (implementada en Sprint 11). Existía inconsistencia: el mismo usuario que presionaba ¡Sorprendeme! obtenía un plan con 3 actividades, pero al generar un plan con el formulario obtenía 0.

---

## Decisión

Aplicar la misma lógica de **3 fases progresivas** a `generate_plan()`:

```
Fase 1 (estricta):   city + budget_per_slot + people_count
Fase 2 (relajada):   city solamente, sin restricciones de budget/people
Fase 3 (minimal):    sin filtros — catálogo completo
```

El loop continúa hasta completar los 3 slots (morning/afternoon/evening), acumulando resultados entre fases y deduplicando entidades ya usadas.

---

## Alternativas descartadas

### A. Mantener fase única y mostrar mensaje claro

Devolver el plan vacío con un mensaje en el frontend: "No encontramos opciones para esa ciudad".

**Descartado porque**: el dropdown de ciudades ya fue limitado a CABA (donde sí hay datos), por lo que el caso de plan vacío no debería ocurrir normalmente. Si ocurre por restricciones de presupuesto muy bajas, es mejor mostrar algo que nada.

### B. Fase 2 únicamente (sin fase 3)

Relajar solo presupuesto/personas, pero mantener el filtro de ciudad siempre.

**Descartado porque**: si el presupuesto es `$0` y la ciudad tiene pocas actividades, la fase 2 puede igualmente no encontrar 3 candidatos. La fase 3 es el safety net necesario.

---

## Consecuencias

**Positivas:**
- El usuario siempre recibe algo al generar un plan, incluso con presupuesto bajo.
- Comportamiento consistente entre `generate_plan()` y `generate_surprise_plan()`.
- `generation_reason` en cada `PlanItem` refleja de qué fase viene la sugerencia.

**Negativas / Trade-offs:**
- Un plan generado en fase 3 puede contener actividades irrelevantes geográficamente (aunque el dropdown limita a CABA, donde la mayoría de los datos están).
- Si en el futuro se agregan muchas ciudades, la fase 3 podría mezclar contenido de distintas ciudades. En ese momento se podría añadir un filtro de "ciudad o sin ciudad asignada" en fase 3.

---

## Referencias

- `backend/apps/planner/services.py` → `generate_plan()`, `_collect_candidates()`
- ADR-014 — Modo Sorprendeme (misma lógica de relajación para surprise plan)
- ADR-019 — Relajación progresiva original (solo para surprise plan)
- SPRINT_12.md
