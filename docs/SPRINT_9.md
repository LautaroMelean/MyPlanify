# SPRINT_9.md

# Sprint 9 — Descubrimiento, Fluidez y Retención

## Estado

```txt
SPRINT_9_STATUS: PLANNED
```

---

## 1. Objetivo del Sprint

Convertir Planify en una app a la que los usuarios quieran volver. Sprint 8 cerró el ciclo planificación → feedback. Sprint 9 responde a la pregunta: ¿por qué volver mañana?

Al terminar este sprint, un usuario puede:

- Descubrir planes populares de otros usuarios en su ciudad ("Inspirate").
- Generar un plan con un solo click sin completar ningún formulario (Modo Sorprendeme).
- Ver un resumen de su actividad personal: planes completados, lugares visitados, racha semanal.
- Exportar cualquier plan a su calendario (Google Calendar o archivo .ics).
- Editar, reordenar y clonar planes de forma fluida dentro de la app.

---

## 2. Alcance

### Incluido

- Feed de planes públicos populares filtrados por ciudad.
- Opción de copiar un plan ajeno como draft propio.
- Generación de plan automático sin formulario (Modo Sorprendeme).
- Página de actividad personal con métricas de uso y racha semanal.
- Export de plan a .ics y deep link a Google Calendar.
- Edición inline de nota de ítem del plan.
- Reordenamiento de ítems dentro de un slot (botones ↑↓).
- Clonado de plan a nueva fecha.
- Tests backend y frontend para todas las funciones nuevas.
- Documentación y ADRs correspondientes.

### Excluido

- Push notifications nativas (requiere Service Workers y VAPID keys — complejidad desproporcionada al valor en esta etapa).
- Chat o comentarios en planes compartidos (requiere WebSockets — Sprint 10+).
- Drag & drop para reordenar ítems (los botones ↑↓ cubren el caso con menor complejidad técnica).
- Sistema de amigos o seguimiento de usuarios (requiere social graph — fuera del roadmap actual).
- Reservas o compra de entradas dentro del plan.
- IA generativa / NLP para descripción libre del plan.

---

## 3. Módulos a implementar

| Módulo | Prioridad |
|--------|-----------|
| Feed de planes populares (backend + frontend) | Alta |
| Modo Sorprendeme (backend + frontend) | Alta |
| Stats personales / Mi Actividad (backend + frontend) | Alta |
| Export a calendario (.ics + Google Calendar link) | Media |
| Edición avanzada del plan (reordenar, clonar, editar nota) | Media |
| Tests backend + frontend | Alta |
| ADRs + documentación | Alta |

---

## 4. Bloque 1 — Feed de Descubrimiento ("Inspirate")

### Objetivo

Mostrar qué están haciendo otros usuarios en la misma ciudad. Genera pertenencia a una comunidad y es el principal vector de adquisición orgánica: quien descubre un plan lo comparte, quien lo recibe lo usa, quien lo usa crea el suyo.

---

### Backend

Nuevo endpoint:

```txt
GET /api/v1/plans/trending/
```

Parámetros opcionales:

```txt
?city=Buenos Aires
?period=today | weekend | week    (default: week)
?limit=10                         (default: 10, max: 20)
```

Lógica de ranking:

```txt
score_trending = (vistas * 1) + (compartidos * 3)
Solo planes con is_public=True
Solo planes con al menos 1 ítem
Excluir planes del propio usuario autenticado
```

Nuevo endpoint para clonar:

```txt
POST /api/v1/plans/{id}/clone/
```

Body:

```txt
{ "date": "2026-07-20" }
```

Comportamiento:

```txt
Crea un Plan nuevo para el usuario autenticado
Copia todos los PlanItems del plan origen
Status = "draft"
is_public = False
No copia el PlanFeedback ni el slug
```

Nuevo campo en InteractionHistory (ya existe la tabla):

```txt
action: "plan_cloned"
```

---

### Nuevo serializer

```txt
TrendingPlanSerializer
  — id
  — title
  — city
  — date
  — items (count, no detalle)
  — slug
  — view_count   (campo calculado desde InteractionHistory)
  — share_count  (campo calculado desde InteractionHistory)
```

---

### Frontend

Nueva sección en `PlannerPage` (debajo del formulario) o nueva pestaña:

```txt
InspireFeed           — lista de TrendingPlanCard
TrendingPlanCard      — título, ciudad, cantidad de ítems, vistas, botón "Usar como base"
```

Flujo "Usar como base":

```txt
1. Usuario clickea "Usar como base"
2. Modal con selector de fecha
3. POST /api/v1/plans/{id}/clone/ con la fecha elegida
4. Redirige al nuevo PlanDetailPage del plan clonado
```

---

### RBAC

```txt
GET trending: AllowAny (también visible para usuarios no autenticados)
POST clone: IsAuthenticated
```

---

## 5. Bloque 2 — Modo Sorprendeme

### Objetivo

Eliminar la fricción del formulario. Hay un segmento de usuarios que quiere explorar pero no sabe por dónde empezar. Un solo botón resuelve el caso de uso completo.

---

### Backend

Nuevo endpoint:

```txt
POST /api/v1/plans/surprise/
```

Body vacío o parámetros opcionales:

```txt
{
  "date": "2026-07-10"     // opcional — default: mañana
}
```

Lógica del servidor:

```txt
1. Tomar ciudad del perfil del usuario (user.city si existe, si no "Buenos Aires")
2. Calcular presupuesto: promedio de los últimos 3 planes del usuario
   — Si no tiene planes previos: $3000 ARS como default
3. people_count: 1 (default fijo, se puede editar después)
4. Llamar a generate_plan() con esos parámetros
5. Loguear en InteractionHistory: action="plan_surprise"
```

---

### Frontend

Botón prominente en `PlannerPage`:

```txt
Posición: arriba del formulario existente, separado visualmente
Texto: "¡Sorprendeme!"
Ícono: ✨ o 🎲
Estado loading: "Preparando tu plan..."
```

Flujo:

```txt
1. Usuario clickea "¡Sorprendeme!"
2. Spinner con mensaje "Armando algo especial para vos..."
3. POST /api/v1/plans/surprise/
4. Redirige a PlanDetailPage del plan generado
5. Badge "Generado al azar" visible en el plan
```

---

### RBAC

```txt
POST surprise: IsAuthenticated
```

---

## 6. Bloque 3 — Stats Personales / Mi Actividad

### Objetivo

Dar al usuario una razón para sentir que progresa. Sin métricas visibles, el uso se percibe como descartable. Con métricas y racha, se convierte en un hábito.

---

### Backend

Nuevo selector en `apps/dashboard/`:

```txt
get_user_activity_stats(user) → dict
```

Retorna:

```txt
{
  "plans_completed": int,
  "places_visited": int,         // PlanItems únicos de planes completados, entity_type="place"
  "cities_explored": int,        // ciudades únicas en planes completados
  "favorite_category": str,      // categoría más frecuente en PlanFeedback del usuario
  "current_streak_weeks": int,   // semanas consecutivas con al menos 1 plan completado
  "best_streak_weeks": int,
  "total_plans": int,
  "avg_rating_given": float,     // promedio de ratings dados por el usuario en PlanFeedback
}
```

Nuevo endpoint:

```txt
GET /api/v1/dashboard/me/stats/
```

Permiso: `IsAuthenticated` (cualquier rol)

---

### Frontend

Nueva sección en `ProfilePage` (bloque debajo de los datos personales):

```txt
ActivityStatsCard     — grid de métricas: planes completados, lugares, ciudades
StreakBadge           — racha actual en semanas con icono de fuego 🔥
FavoriteCategoryBadge — "Tu categoría favorita: Gastronomía"
```

Alternativa: nueva página `/mi-actividad` enlazada desde `ProfilePage`.

La decisión de página separada vs sección en ProfilePage se toma en implementación según el volumen de datos que devuelva la API.

---

### RBAC

```txt
GET /api/v1/dashboard/me/stats/: IsAuthenticated (todos los roles)
```

---

## 7. Bloque 4 — Export del Plan a Calendario

### Objetivo

El plan existe en la app pero el usuario vive en su calendario. Si no puede llevar el plan a su calendario real, la probabilidad de ejecutarlo cae significativamente.

---

### Backend

No requiere nuevos endpoints. Los datos del plan ya están disponibles via `GET /api/v1/plans/{id}/`.

---

### Frontend

Nuevo botón en `PlanDetailPage`:

```txt
"Exportar a calendario"
```

Al hacer click, menú con dos opciones:

```txt
1. Descargar .ics
2. Agregar a Google Calendar
```

#### Generación del archivo .ics

Lógica en el frontend (sin backend):

```txt
Por cada PlanItem del plan:
  — morning   → hora de inicio: 09:00, duración: 2hs
  — afternoon → hora de inicio: 14:00, duración: 2hs
  — evening   → hora de inicio: 20:00, duración: 2hs

Nombre del evento: nombre de la entidad (place/activity/event)
Descripción: generation_reason del ítem
Fecha: plan.date

Generar string .ics con formato iCalendar RFC 5545
Triggear descarga como archivo: plan-{slug}.ics
```

#### Deep link a Google Calendar

Para cada ítem individual, construir URL:

```txt
https://calendar.google.com/calendar/render?action=TEMPLATE
  &text={nombre del ítem}
  &dates={fecha}T{hora_inicio}/{fecha}T{hora_fin}
  &details={generation_reason}
```

O bien exportar el plan completo como un solo evento de día completo con la lista de ítems en la descripción.

Nuevo componente:

```txt
CalendarExportButton
```

---

## 8. Bloque 5 — Edición Avanzada del Plan

### Objetivo

El planner actual permite agregar y quitar ítems pero no reorganizarlos ni editarlos. Esto hace que el plan generado se sienta rígido. La edición fluida transforma el planner de un generador de sugerencias en una herramienta real de planificación.

---

### Backend

Nuevo endpoint para actualizar ítem:

```txt
PATCH /api/v1/plans/{plan_id}/items/{item_id}/
```

Campos actualizables:

```txt
note   — texto libre del usuario sobre el ítem
order  — nuevo orden dentro del slot (integer)
```

Reglas:

```txt
Solo el propietario del plan puede actualizar sus ítems
Validar que item_id pertenezca al plan_id
log_action en cada actualización
```

Nuevo endpoint para clonar plan propio:

```txt
POST /api/v1/plans/{plan_id}/clone/
```

Ya definido en Bloque 1 — se reutiliza el mismo endpoint.

---

### Frontend

#### Edición inline de nota

En `PlanItemCard`:

```txt
Click en el texto de la nota → modo edición (input inline)
Enter o blur → PATCH /plans/{id}/items/{item_id}/ con nueva nota
Escape → cancela sin guardar
```

#### Reordenamiento de ítems

En `PlanItemCard`, para planes que el usuario posee:

```txt
Botones ↑ ↓ visibles en hover
Click ↑ → intercambia order con el ítem anterior del mismo slot
Click ↓ → intercambia order con el ítem siguiente del mismo slot
PATCH /plans/{id}/items/{item_id}/ con nuevo order
```

#### Clonar plan

En `PlanDetailPage`, nuevo botón:

```txt
"Usar de nuevo"
Modal con selector de fecha
POST /api/v1/plans/{id}/clone/
Redirige al nuevo plan
```

---

### RBAC

```txt
PATCH items: IsAuthenticated + propietario del plan
POST clone: IsAuthenticated
```

---

## 9. Testing obligatorio

### Backend

```txt
tests/test_planner.py (extensión del existente)
  — GET /plans/trending/ devuelve solo planes públicos
  — GET /plans/trending/?city= filtra por ciudad
  — GET /plans/trending/ no incluye planes del usuario autenticado
  — POST /plans/{id}/clone/ crea plan propio con los mismos ítems
  — POST /plans/{id}/clone/ no copia feedback ni slug
  — POST /plans/surprise/ genera plan con datos del perfil del usuario
  — POST /plans/surprise/ usa $3000 de default si el usuario no tiene planes previos
  — PATCH /plans/{id}/items/{item_id}/ actualiza nota
  — PATCH /plans/{id}/items/{item_id}/ actualiza order
  — No propietario no puede PATCH ítems ajenos

tests/test_dashboard.py (nuevo o extensión)
  — GET /api/v1/dashboard/me/stats/ retorna campos esperados
  — plans_completed refleja planes con status=completed
  — current_streak_weeks = 0 si no hay planes completados
  — Unauthenticated no puede acceder
```

### Frontend

```txt
TrendingPlanCard.test.tsx
  — muestra título, ciudad, cantidad de ítems
  — botón "Usar como base" llama a la función de clone

InspireFeed.test.tsx
  — muestra empty state cuando no hay planes trending
  — muestra lista de TrendingPlanCard

ActivityStatsCard.test.tsx
  — muestra planes completados, ciudades, racha
  — muestra "Sin actividad aún" si todos los valores son 0

CalendarExportButton.test.tsx
  — renderiza con las dos opciones (ics, Google Calendar)
  — el link de Google Calendar tiene el formato correcto

PlanItemCard.test.tsx (extensión del existente)
  — muestra botones ↑ ↓ cuando onReorder está definido
  — click en nota activa modo edición
  — Enter en edición llama a onSaveNote con el nuevo valor
```

---

## 10. Criterios de aceptación

### Feed de descubrimiento

- `GET /plans/trending/` devuelve planes públicos ordenados por score (vistas + compartidos).
- Solo aparecen planes con al menos 1 ítem y `is_public=True`.
- El usuario autenticado no ve sus propios planes en el feed.
- El botón "Usar como base" crea una copia en draft para el usuario, conservando los ítems.

### Modo Sorprendeme

- El botón está visible en `PlannerPage` sin necesidad de completar el formulario.
- El plan generado usa la ciudad del perfil del usuario o "Buenos Aires" como fallback.
- El presupuesto calculado refleja el promedio de los últimos 3 planes del usuario.
- El plan generado es idéntico en estructura a uno generado con el formulario estándar.

### Stats personales

- `GET /dashboard/me/stats/` retorna todas las métricas esperadas.
- `plans_completed` refleja solo planes con `status="completed"`.
- `current_streak_weeks` sube si el usuario completa un plan esta semana.
- La sección es visible desde `ProfilePage`.

### Export a calendario

- El archivo .ics descargado es válido y se importa correctamente en Google Calendar y Apple Calendar.
- Cada ítem del plan aparece como evento separado en el horario correspondiente al slot.
- El deep link de Google Calendar pre-rellena fecha, hora y descripción.

### Edición avanzada

- La nota de un ítem se puede editar inline sin recargar la página.
- Los botones ↑↓ reordenan los ítems dentro del mismo slot correctamente.
- Clonar un plan crea uno nuevo con los mismos ítems y status="draft".

---

## 11. Documentación a actualizar

```txt
DATA_MODEL.md
  — Agregar action "plan_cloned" y "plan_surprise" a InteractionHistory
  — Agregar endpoint /plans/trending/ y /plans/surprise/ a la tabla de rutas

API_GUIDELINES.md
  — Documentar endpoints nuevos con ejemplos de request/response

RBAC.md
  — Agregar reglas para /plans/trending/ (AllowAny) y /dashboard/me/stats/ (IsAuthenticated)

docs/adr/ADR-013-discovery-feed.md
  — Decisión: ranking de planes públicos por score (vistas + compartidos)
  — Alternativa rechazada: curación manual

docs/adr/ADR-014-modo-sorprendeme.md
  — Decisión: presupuesto calculado desde historial vs presupuesto fijo
  — Decisión: ciudad desde perfil vs geolocalización en tiempo real

docs/adr/ADR-015-calendar-export.md
  — Decisión: .ics generado en frontend vs backend
  — Slots mapeados a horas fijas (9am / 2pm / 8pm)
```

---

## 12. Definition of Done

Sprint 9 estará completo cuando:

- `GET /plans/trending/` devuelva resultados correctos con el ranking esperado.
- `POST /plans/surprise/` genere un plan válido usando datos del perfil.
- `GET /dashboard/me/stats/` retorne todas las métricas esperadas.
- El archivo .ics se descargue correctamente y sea importable en Google Calendar.
- La edición inline de nota funcione sin recargar la página.
- Los botones ↑↓ reordenen ítems dentro del mismo slot.
- El clon de plan conserve todos los ítems del original.
- Todos los tests pasen (backend + frontend).
- TypeScript sin errores.
- Docker funcionando sin cambios adicionales de configuración.
- Documentación y ADRs actualizados.

---

## 13. Fuera de alcance

```txt
Push notifications nativas (Service Workers + VAPID keys)
Chat o comentarios en planes compartidos
Drag & drop para reordenar ítems
Sistema de amigos o seguidores
Reservas o compra de entradas
IA generativa / NLP para generación de planes por descripción libre
```

---

## 14. Salida esperada

```txt
SPRINT_9_STATUS: DISCOVERY_FLUENCY_RETENTION
```

Al finalizar Sprint 9, Planify tendrá:

- Un feed de descubrimiento que hace que la app se sienta viva y social.
- Una forma de empezar a planificar en un click sin fricción.
- Métricas de actividad que dan al usuario un motivo para volver.
- Integración real con el calendario del usuario para cerrar el ciclo.
- Un planner que se puede editar con fluidez, no solo generar.

---

## 15. Próximo Sprint

```txt
SPRINT_10

Monetización, reservas o integración con proveedores externos
```
