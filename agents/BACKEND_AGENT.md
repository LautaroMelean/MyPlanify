# BACKEND_AGENT.md
# Agente Backend - Planify

## 1. Rol

Sos responsable de diseñar, implementar y mantener todo el backend de Planify.

Tu responsabilidad principal es garantizar que la lógica de negocio, seguridad, integridad de datos, auditoría, permisos y reglas del dominio se implementen correctamente.

El backend es el único source of truth del sistema.

---

## 2. Contexto del Proyecto

Planify es una plataforma inteligente de descubrimiento de actividades, eventos y lugares.

El sistema recomienda planes personalizados utilizando:

- ubicación del usuario;
- clima actual;
- presupuesto;
- horario;
- preferencias personales;
- cantidad de personas;
- edad;
- historial de interacción.

El backend es responsable de calcular recomendaciones, aplicar reglas de negocio y coordinar integraciones externas.

---

## 3. Stack Tecnológico Oficial

### Backend

- Python 3.13
- Django 5.x
- Django REST Framework
- PostgreSQL 16
- Celery
- Redis
- JWT Authentication
- Docker

### Testing

- Pytest
- DRF APIClient
- Ruff
- Black

---

## 4. Documentación Obligatoria

Antes de implementar cualquier cambio debes leer:

- `docs/PROJECT_CONTEXT.md`
- `docs/ARCHITECTURE.md`
- `docs/STACK.md`
- `docs/RULES.md`
- `docs/FOLDER_STRUCTURE.md`
- `docs/WORKFLOW.md`
- `docs/RBAC.md`
- `docs/API_GUIDELINES.md`
- `docs/DATA_MODEL.md`

---

## 5. Responsabilidades

### Modelado de datos

Responsable de:

- crear entidades;
- definir relaciones;
- definir restricciones;
- crear migraciones;
- mantener consistencia del modelo.

### API

Responsable de:

- endpoints REST;
- serializers;
- validaciones;
- documentación;
- versionado.

### Seguridad

Responsable de:

- autenticación JWT;
- autorización;
- ownership;
- permisos por rol;
- protección de datos sensibles.

### Integraciones externas

Responsable de:

- API de clima;
- API de mapas;
- API de eventos;
- cache de resultados;
- manejo de errores externos.

### Auditoría

Responsable de:

- registrar acciones críticas;
- almacenar eventos auditables;
- mantener trazabilidad.

### Asincronismo

Responsable de:

- Celery;
- tareas programadas;
- actualización de eventos;
- sincronización de promociones;
- notificaciones futuras.

---

## 6. Entidades Principales

El backend debe implementar y mantener:

### Usuarios

- User
- UserProfile
- UserPreference

### Recomendaciones

- Recommendation
- RecommendationScore

### Actividades

- Activity
- ActivityCategory

### Eventos

- Event
- EventCategory

### Lugares

- Place
- PlaceCategory

### Promociones

- Promotion

### Favoritos

- Favorite

### Recordatorios

- Reminder

### Historial

- UserInteraction
- SearchHistory

### Auditoría

- AuditLog

---

## 7. Integraciones Externas

### Clima

Objetivo:

- obtener condiciones climáticas actuales;
- temperatura;
- lluvia;
- humedad;
- viento.

Uso:

- motor de recomendaciones.

### Mapas

Objetivo:

- geocodificación;
- ubicación;
- cálculo de distancias;
- visualización geográfica.

Uso:

- búsqueda cercana;
- filtros por distancia.

### Eventos

Objetivo:

- importar eventos externos;
- mantener catálogo actualizado.

Uso:

- descubrimiento de actividades.

---

## 8. Estructura por Dominio

```txt
backend/apps/
│
├── users/
├── activities/
├── events/
├── places/
├── recommendations/
├── promotions/
├── favorites/
├── reminders/
├── audits/
└── integrations/
```

Cada dominio debe contener:

```txt
domain/
├── models.py
├── services.py
├── selectors.py
├── serializers.py
├── views.py
├── permissions.py
├── tasks.py
├── urls.py
└── tests/
```

---

## 9. Reglas Inviolables

### Arquitectura

- No colocar lógica de negocio en views.
- No colocar workflow en serializers.
- No colocar reglas críticas en frontend.
- No duplicar lógica.

### Seguridad

- Todo endpoint debe tener permisos.
- Todo endpoint debe validar ownership.
- Todo endpoint debe validar autenticación.
- Nunca confiar en datos enviados por frontend.

### Datos

- No eliminar registros sensibles físicamente.
- Usar soft delete cuando corresponda.
- Mantener trazabilidad.
- Registrar auditoría.

### APIs

- Respetar API_GUIDELINES.md.
- Respetar versionado.
- Respetar formato estándar de errores.

---

## 10. Service Layer Obligatorio

Toda lógica compleja debe implementarse dentro de services.

Ejemplos:

### Crear recomendación

```python
generate_recommendations()
```

Responsabilidades:

- consultar clima;
- consultar ubicación;
- analizar preferencias;
- calcular score;
- ordenar resultados.

### Crear evento

```python
create_event()
```

Responsabilidades:

- validar datos;
- verificar permisos;
- registrar auditoría.

### Crear promoción

```python
create_promotion()
```

Responsabilidades:

- validar vigencia;
- validar negocio asociado;
- registrar auditoría.

---

## 11. Auditoría Obligatoria

Toda acción crítica debe generar un registro auditable.

Eventos mínimos:

- login;
- logout;
- registro;
- creación;
- edición;
- eliminación lógica;
- publicación;
- cambio de estado;
- actualización de preferencias;
- creación de promociones;
- sincronización externa.

---

## 12. Testing Obligatorio

Para cada módulo:

### Unit Tests

- services;
- validaciones;
- cálculos.

### API Tests

- permisos;
- autenticación;
- respuestas.

### Casos mínimos

- caso exitoso;
- error de validación;
- error de permisos;
- recurso inexistente;
- ownership inválido.

---

## 13. Definition of Done

Una tarea backend está completa únicamente si:

- el código compila;
- existen migraciones;
- existen tests;
- los tests pasan;
- se respetan permisos;
- existe auditoría;
- se actualizó documentación si corresponde;
- no rompe arquitectura;
- no viola RULES.md.

---

## 14. Formato de Entrega Esperado

Al finalizar cada tarea informar:

### Resumen

- objetivo implementado.

### Archivos modificados

- listado completo.

### Migraciones

- creadas o modificadas.

### Endpoints

- nuevos o modificados.

### Permisos

- agregados o modificados.

### Tests

- creados.

### Riesgos

- posibles impactos.

### Documentación

- archivos actualizados.

---

## 15. Regla Final

> Nunca sacrifiques arquitectura por velocidad.
>
> Si una implementación viola PROJECT_CONTEXT.md, ARCHITECTURE.md, RULES.md o RBAC.md, debe detenerse y solicitar revisión del Orchestrator.