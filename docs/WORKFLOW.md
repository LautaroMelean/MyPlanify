# WORKFLOW.md

# Workflow, Estados y Transiciones

## 1. Objetivo

Definir cómo se mueve el sistema, qué estados existen, qué transiciones son válidas y qué reglas gobiernan los procesos.

Este documento evita que la IA invente flujos paralelos y asegura que todas las transiciones de estado sean consistentes y auditables.

---

## 2. Entidades con workflow

| Entidad | Tiene estados | Documento fuente |
|----------|----------|----------|
| Evento | Sí | PROJECT_CONTEXT.md |
| Promoción | Sí | PROJECT_CONTEXT.md |
| Notificación | Sí | PROJECT_CONTEXT.md |
| Usuario | Sí | PROJECT_CONTEXT.md |
| Lugar | No | PROJECT_CONTEXT.md |
| Actividad | No | PROJECT_CONTEXT.md |
| Recomendación | No | PROJECT_CONTEXT.md |

---

## 3. Workflow de Eventos

### Estados permitidos

| Estado | Descripción | Visible para usuario | Estado final |
|----------|----------|----------|----------|
| draft | Evento en creación | No | No |
| published | Evento publicado | Sí | No |
| cancelled | Evento cancelado | Sí | Sí |
| finished | Evento finalizado | Sí | Sí |

### Transiciones permitidas

| Desde | Hacia | Quién puede hacerlo | Validaciones |
|----------|----------|----------|----------|
| draft | published | Organizador / Admin | Datos obligatorios completos |
| published | cancelled | Organizador / Admin | Motivo obligatorio |
| published | finished | Sistema / Admin | Fecha final alcanzada |

### Transiciones prohibidas

| Desde | Hacia | Motivo |
|----------|----------|----------|
| finished | published | Evento ya finalizado |
| cancelled | published | Requiere crear nuevo evento |

---

## 4. Workflow de Promociones

### Estados permitidos

| Estado | Descripción | Visible para usuario | Estado final |
|----------|----------|----------|----------|
| draft | Promoción en creación | No | No |
| active | Promoción activa | Sí | No |
| expired | Promoción vencida | No | Sí |
| cancelled | Promoción cancelada | No | Sí |

### Transiciones permitidas

| Desde | Hacia | Quién puede hacerlo | Validaciones |
|----------|----------|----------|----------|
| draft | active | Negocio asociado / Admin | Datos completos |
| active | expired | Sistema | Fecha de vencimiento alcanzada |
| active | cancelled | Negocio asociado / Admin | Motivo obligatorio |

### Transiciones prohibidas

| Desde | Hacia | Motivo |
|----------|----------|----------|
| expired | active | Promoción vencida |
| cancelled | active | Debe crearse nuevamente |

---

## 5. Workflow de Notificaciones

### Estados permitidos

| Estado | Descripción | Estado final |
|----------|----------|----------|
| pending | Pendiente de envío | No |
| sent | Enviada | Sí |
| failed | Error de envío | Sí |

### Transiciones permitidas

| Desde | Hacia | Quién puede hacerlo |
|----------|----------|----------|
| pending | sent | Sistema |
| pending | failed | Sistema |

---

## 6. Workflow de Usuarios

### Estados permitidos

| Estado | Descripción |
|----------|----------|
| active | Usuario activo |
| suspended | Usuario suspendido |
| deleted | Usuario eliminado lógicamente |

### Transiciones permitidas

| Desde | Hacia | Quién puede hacerlo |
|----------|----------|----------|
| active | suspended | Admin |
| suspended | active | Admin |
| active | deleted | Usuario / Admin |

---

## 7. Eventos auditables del workflow

Toda transición relevante debe generar un registro auditable.

Eventos mínimos:

- registro de usuario;
- login;
- actualización de perfil;
- creación de evento;
- publicación de evento;
- cancelación de evento;
- creación de promoción;
- activación de promoción;
- cancelación de promoción;
- cambio de estado de usuario;
- creación de recordatorio;
- envío de notificación.

---

## 8. Reglas del motor de recomendaciones

Las recomendaciones no poseen estados persistentes.

Se generan dinámicamente en cada consulta considerando:

- ubicación;
- clima actual;
- presupuesto;
- horario;
- cantidad de personas;
- preferencias del usuario;
- historial de interacción.

Las recomendaciones no se almacenan como workflow.

---

## 9. Reglas de implementación

- Las transiciones se validan exclusivamente en backend.
- El frontend puede ocultar botones, pero nunca decidir la validez final.
- Cada transición relevante genera auditoría.
- Cada transición puede disparar notificaciones.
- Las reglas de workflow deben tener tests.
- Las transiciones automáticas deben ejecutarse mediante tareas programadas (Celery).
- Ningún estado puede modificarse directamente desde la base de datos.

---

## 10. Sprint 0

Durante Sprint 0 no se programan features de negocio.

Sprint 0 debe construir:

- repositorio;
- backend base;
- frontend base;
- autenticación JWT;
- modelo de usuarios;
- estructura modular;
- PostgreSQL;
- Docker;
- Redis;
- Celery;
- CI/CD inicial;
- documentación viva.

---

## 11. Definition of Done para un flujo

Un flujo está completo si:

- el backend valida transiciones;
- el frontend muestra acciones correctas;
- existen tests unitarios;
- existen tests de integración;
- hay auditoría;
- hay manejo de errores;
- está documentado;
- respeta permisos;
- respeta las reglas definidas en RULES.md;
- respeta la arquitectura definida en ARCHITECTURE.md.

---

## 12. Regla de oro

> Ningún cambio de estado puede realizarse fuera del backend ni sin respetar las validaciones definidas en este documento.