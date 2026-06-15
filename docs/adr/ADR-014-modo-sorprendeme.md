# ADR-014 — Modo Sorprendeme

## Estado

ACCEPTED — Sprint 9

## Contexto

Para eliminar la fricción del formulario, Sprint 9 introduce un endpoint `POST /api/v1/plans/surprise/` que genera un plan automático sin input del usuario.

Había que decidir:
1. Cómo obtener la ciudad del usuario.
2. Cómo calcular el presupuesto automático.

## Decisiones

### Ciudad

**Se usa la ciudad del último plan creado por el usuario; fallback "Buenos Aires".**

Alternativa rechazada: geolocalización en tiempo real. Requiere que el navegador envíe coordenadas en cada request y que el backend las reverse-geocodifique, lo que agrega latencia y dependencia de servicios externos. El historial de planes refleja la ciudad donde el usuario realmente planifica.

Alternativa rechazada: agregar `city` al modelo `User`. El User model no tiene este campo y no forma parte del perfil editable en Sprint 9. Agregar un campo requeriría migración, UI de edición y lógica de actualización — trabajo desproporcionado al beneficio.

### Presupuesto

**Se usa el promedio de los últimos 3 planes del usuario; fallback $3000 ARS.**

El promedio del historial refleja el presupuesto habitual del usuario. El fallback $3000 es un valor razonable para Buenos Aires que cubre opciones básicas de las tres categorías (mañana, tarde, noche).

## Consecuencias

- La ciudad y presupuesto derivados del historial pueden diferir de las preferencias actuales del usuario. El plan generado es editable, lo cual mitiga este punto.
- `POST /plans/surprise/` llama directamente a `generate_plan()` — reutiliza todo el motor de scoring V3 incluyendo feedback scores.
