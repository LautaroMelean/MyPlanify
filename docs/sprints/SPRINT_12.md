# SPRINT_12.md

# Sprint 12 — Pulido de Presentación y Correcciones de UX

## Estado

```txt
SPRINT_12_STATUS: DONE
```

---

## 1. Objetivo del Sprint

Preparar Planify para una presentación pública puliendo la interfaz, corrigiendo inconsistencias visuales y mejorando la robustez del backend del Planner.

Al terminar este sprint, Planify tiene:

- **UI consistente**: spinners, estados vacíos, formateo de fechas/precios unificados.
- **Cards más ricas**: hover con zoom, franja de color por tipo de actividad, badges coherentes.
- **Planner más robusto**: `generate_plan()` con fallback progresivo igual que Sorprendeme.
- **Navbar más inteligente**: active state con `startsWith`, íconos diferenciados.
- **171 tests pasando** (frontend).

---

## 2. Alcance

### Backend

| Cambio | Archivo | Descripción |
|---|---|---|
| Fallback progresivo en `generate_plan()` | `apps/planner/services.py` | Igual que `generate_surprise_plan()`: 3 fases (city+budget → city → sin filtros). Evita planes vacíos cuando no hay datos para la ciudad elegida. |
| Dropdown de ciudades limitado a CABA | `frontend/…/PlannerForm.tsx` | La DB solo tiene datos de Buenos Aires. Eliminar "Otras ciudades" evita mostrar siempre los mismos 30 registros genéricos para Córdoba/Rosario. |

### Frontend

#### Páginas

| Página | Cambio |
|---|---|
| `MyPlansPage` | Spinner de carga animado, `EmptyState` component, fechas en español (`"1 jul. 2026"`), conteo de actividades en lugar de "N ítems", confirmación antes de borrar, ícono `<Plus />`, hover `shadow-md` |
| `PlanDetailPage` | Spinner de carga animado, `EmptyState` para plan no encontrado y plan vacío, presupuesto formateado (`$5.000`), `max-w-3xl`, `focus-visible:ring` en botón volver |

#### Componentes de cards

| Componente | Cambio |
|---|---|
| `PlaceCard` | Zoom de imagen en hover (`group-hover:scale-105 transition-transform duration-300`) |
| `EventCard` | Zoom de imagen en hover, precio sin decimales (`$1.500`), placeholder imagen en `indigo-50`, `place_name` en `gray-500` |
| `ActivityCard` | Franja de color en header según tipo (restaurante=naranja, museo=azul, bar=violeta, parque=verde, etc.), `isFree()` robusto para `'0'`/`'0.00'`/`0` |

#### Planner

| Componente | Cambio |
|---|---|
| `PlanItemCard` | Label de tipo sin `uppercase tracking-wide`, `generation_reason` con ícono Zap (antes: `<blockquote>`-style), skeleton shimmer en lugar de `"Cargando..."`, botones de reorden en `opacity-30` siempre visibles |
| `ItineraryView` | Slot vacío con dashed border en lugar de texto itálico |

#### Navbar

| Cambio | Descripción |
|---|---|
| `isActive` con `startsWith` | La sección activa se resalta en sub-rutas (`/planes/123` resalta "Planner") |
| `<Clock />` para Recordatorios | Diferencia visualmente Notificaciones (`Bell`) de Recordatorios (`Clock`) |
| Mobile badge limpio | Eliminado badge doble en Notificaciones del menú mobile |

---

## 3. Tests actualizados

Los tests de `PlannerForm`, `MyPlansPage` e `ItineraryView` se actualizaron para reflejar los nuevos textos y comportamientos:

```txt
PlannerForm.test.tsx   — city "Córdoba" → "Palermo" (Córdoba ya no está en el dropdown)
MyPlansPage.test.tsx   — "no tenés planes guardados" → "Todavía no tenés planes"
ItineraryView.test.tsx — "Sin ítems en este horario" → "Sin actividades para este horario"
```

**Resultado**: 171/171 tests pasando.

---

## 4. Decisiones de diseño

### Por qué limitar ciudades a CABA

La DB tiene 2.379 actividades con `city="Buenos Aires"` y solo 30 con `city=""` (genéricas). Para Córdoba, Rosario, etc. solo las 30 genéricas coincidían — el usuario veía siempre el mismo conjunto sin importar qué ciudad elegía. La solución correcta es:

1. Corto plazo: ocultar ciudades sin datos (este sprint).
2. Largo plazo: importar datos de otras ciudades vía GCBA equivalentes o Overpass.

### Por qué `generate_plan()` necesitaba fases de fallback

`generate_plan()` solo usaba fase 1 (estricta). Si el presupuesto era bajo o la ciudad sin datos, devolvía un plan con 0 ítems. Ahora usa la misma lógica de 3 fases que `generate_surprise_plan()`, garantizando al menos algo útil en cualquier caso.

---

## 5. Definition of Done

- [x] 171 tests frontend pasando
- [x] TypeScript sin errores
- [x] Backend: `generate_plan()` con 3 fases de fallback
- [x] Frontend: spinner en MyPlansPage y PlanDetailPage
- [x] Frontend: `EmptyState` component en todos los estados vacíos de planes
- [x] Frontend: fechas y precios formateados en español
- [x] Frontend: cards con hover de imagen
- [x] Frontend: ActivityCard con franja de color
- [x] Frontend: PlanItemCard pulido
- [x] Frontend: Navbar con `startsWith` y `<Clock />`
- [x] Documentación: SPRINT_12.md, ADR-020, README actualizado

---

## 6. Próximo Sprint (candidatos)

```txt
SPRINT_13 (pendiente)

Candidatos:
  — Datos de otras ciudades (Córdoba, Rosario) vía Overpass o fuentes equivalentes
  — OAuth login con Google para reducir fricción de registro
  — Notificaciones push (Web Push API)
  — Parser completo de opening_hours con feriados argentinos
  — ActivityCard con imagen (usar image_url del modelo Activity enriquecido)
  — Maps: mostrar actividades GCBA en mapa junto a lugares OSM
```
