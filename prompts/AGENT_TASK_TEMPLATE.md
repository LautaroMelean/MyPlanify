# AGENT_TASK_TEMPLATE.md
# Plantilla Oficial de Asignación de Tareas - Planify

## Objetivo

Esta plantilla define el formato obligatorio para asignar trabajo a cualquier agente IA dentro del proyecto Planify.

Todo agente deberá respetar:

- Arquitectura definida.
- Stack oficial.
- RBAC.
- Workflow.
- Reglas de negocio.
- API Guidelines.
- Convenciones del proyecto.

Ninguna tarea puede contradecir la documentación oficial.

---

# Tarea

**Nombre corto:**

`[Nombre de la tarea]`

**ID (opcional):**

`TASK-XXX`

**Prioridad:**

- Baja
- Media
- Alta
- Crítica

---

# Contexto

Describir:

- Qué se necesita.
- Por qué se necesita.
- Qué problema resuelve.
- Qué impacto tiene dentro de Planify.

Ejemplo:

```txt
Se necesita implementar el módulo de favoritos para permitir que los usuarios guarden actividades, eventos y lugares para consultarlos posteriormente.
```

---

# Agente responsable

Seleccionar uno:

- Backend Agent
- Frontend Agent
- DevOps Agent
- Security Agent
- QA Agent
- Orchestrator

---

# Agentes secundarios

Indicar agentes que deberán revisar o colaborar.

Ejemplo:

- Backend Agent
- QA Agent
- Security Agent

---

# Dominio afectado

Seleccionar uno o más:

- users
- activities
- places
- events
- recommendations
- favorites
- promotions
- notifications
- reviews
- audits

---

# Documentación obligatoria

Antes de comenzar, el agente debe leer:

- `docs/PROJECT_CONTEXT.md`
- `docs/ARCHITECTURE.md`
- `docs/STACK.md`
- `docs/RULES.md`
- `docs/FOLDER_STRUCTURE.md`

Y además:

### Documentos específicos

- `[Documento adicional 1]`
- `[Documento adicional 2]`

Ejemplo:

```txt
docs/RBAC.md
docs/WORKFLOW.md
docs/API_GUIDELINES.md
```

---

# Alcance

## Incluido

- `[Funcionalidad 1]`
- `[Funcionalidad 2]`
- `[Funcionalidad 3]`

## Excluido

No debe implementarse:

- `[Funcionalidad excluida 1]`
- `[Funcionalidad excluida 2]`
- `[Funcionalidad excluida 3]`

---

# Requisitos funcionales

Listado detallado de comportamientos esperados.

Ejemplo:

- El usuario puede guardar una actividad.
- El usuario puede eliminar una actividad guardada.
- El usuario puede listar sus favoritos.

---

# Requisitos técnicos

La implementación debe:

- Respetar la arquitectura.
- Respetar RBAC.
- Respetar Workflow.
- Respetar API Guidelines.
- Incluir auditoría cuando corresponda.
- Incluir validaciones de seguridad.
- Incluir manejo de errores.

---

# Archivos esperados

Archivos que se espera crear o modificar.

Ejemplo:

```txt
backend/apps/favorites/models.py
backend/apps/favorites/services.py
backend/apps/favorites/views.py
backend/apps/favorites/serializers.py
backend/apps/favorites/tests/
frontend/src/features/favorites/
```

---

# Reglas específicas

Reglas particulares de la tarea.

Ejemplo:

- Solo usuarios autenticados pueden guardar favoritos.
- No permitir duplicados.
- Registrar auditoría de creación y eliminación.

---

# Permisos y seguridad

Responder obligatoriamente:

### ¿Quién puede ejecutar la acción?

`[Rol]`

### ¿Sobre qué recurso?

`[Entidad]`

### ¿Existe ownership?

- Sí
- No

### ¿Debe auditarse?

- Sí
- No

### ¿Debe generar notificación?

- Sí
- No

---

# Criterios de aceptación

La tarea se considera terminada únicamente si:

- [ ] Funciona según lo solicitado.
- [ ] Respeta arquitectura.
- [ ] Respeta permisos.
- [ ] Tiene validaciones.
- [ ] Tiene manejo de errores.
- [ ] Tiene tests.
- [ ] Tiene documentación actualizada.
- [ ] No rompe funcionalidades existentes.

---

# Tests requeridos

## Backend

- [ ] Test de creación.
- [ ] Test de validaciones.
- [ ] Test de permisos.
- [ ] Test de errores.
- [ ] Test de auditoría.

## Frontend

- [ ] Loading state.
- [ ] Empty state.
- [ ] Error state.
- [ ] Flujo principal.
- [ ] Responsive.

## Seguridad

- [ ] Usuario no autenticado.
- [ ] Usuario sin permisos.
- [ ] Intento de acceso indebido.
- [ ] Validación de ownership.

---

# Riesgos

Identificar riesgos potenciales.

Ejemplo:

- Duplicación de datos.
- Problemas de permisos.
- Impacto en rendimiento.
- Dependencia de API externa.

---

# Entrega esperada

El agente deberá responder utilizando el siguiente formato:

```md
# Resultado

## Resumen
[Explicación]

## Archivos creados
[Listado]

## Archivos modificados
[Listado]

## Decisiones tomadas
[Listado]

## Tests implementados
[Listado]

## Riesgos detectados
[Listado]

## Documentación actualizada
[Listado]

## Próximos pasos recomendados
[Listado]
```

---

# Regla final

Si la tarea contradice:

- PROJECT_CONTEXT.md
- ARCHITECTURE.md
- STACK.md
- RULES.md
- WORKFLOW.md
- RBAC.md
- API_GUIDELINES.md

el agente debe detener la implementación y reportar el conflicto antes de continuar.