# FEATURE_SPEC_TEMPLATE.md
# Especificación Funcional de Feature - Planify

## 1. Nombre de la feature

`[Nombre de la funcionalidad]`

Ejemplos:

- Recomendación de actividades
- Sistema de favoritos
- Búsqueda de eventos
- Perfil de usuario
- Mapa interactivo
- Promociones de negocios

---

## 2. Problema que resuelve

Describir qué problema del usuario o del negocio resuelve esta funcionalidad.

### Contexto

La feature debe alinearse con los objetivos definidos en:

- `PROJECT_CONTEXT.md`
- `WORKFLOW.md`
- `RBAC.md`

### Problema

`[Descripción detallada del problema]`

### Beneficio esperado

`[Qué mejora obtiene el usuario o el negocio]`

---

## 3. Usuario objetivo

| Actor | Necesidad |
|---------|---------|
| Usuario General | Encontrar actividades relevantes según contexto |
| Negocio Asociado | Promocionar actividades y promociones |
| Organizador de Eventos | Publicar eventos |
| Moderador | Validar contenido |
| Administrador | Gestionar información global |

---

## 4. Flujo principal

### Escenario principal

1. `[Acción inicial del usuario]`
2. `[Validación o consulta del sistema]`
3. `[Procesamiento de negocio]`
4. `[Respuesta del sistema]`
5. `[Resultado esperado]`

### Ejemplo

1. Usuario ingresa a recomendaciones.
2. Sistema obtiene ubicación.
3. Sistema consulta clima actual.
4. Sistema calcula score de actividades.
5. Se muestran recomendaciones ordenadas.

---

## 5. Reglas de negocio

| Regla | Descripción |
|---------|---------|
| RB-001 | Toda recomendación debe respetar filtros activos |
| RB-002 | Debe respetarse la ubicación del usuario |
| RB-003 | Debe respetarse el presupuesto configurado |
| RB-004 | Debe respetarse el rango etario |
| RB-005 | Deben priorizarse intereses configurados |
| RB-006 | No deben mostrarse promociones vencidas |
| RB-007 | Solo mostrar actividades activas |

Agregar reglas específicas de la feature.

---

## 6. Estados involucrados

### Estados de entidad principal

| Estado | Descripción |
|---------|---------|
| draft | Creado pero no visible |
| pending_review | Pendiente de aprobación |
| active | Visible para usuarios |
| paused | Temporalmente oculto |
| expired | Finalizado automáticamente |
| archived | Histórico |

Agregar estados adicionales si la feature los requiere.

---

## 7. Permisos

Definidos según:

- `RBAC.md`
- `WORKFLOW.md`

| Acción | Roles permitidos | Scope |
|---------|---------|---------|
| Ver | Todos los usuarios autenticados | own/public |
| Crear | Administrador, Negocio, Organizador | own |
| Modificar | Propietario o Administrador | own/global |
| Eliminar | Propietario o Administrador | own/global |
| Aprobar | Moderador, Administrador | global |

---

## 8. API requerida

### Endpoints necesarios

| Método | Endpoint | Descripción |
|---------|---------|---------|
| GET | `/api/v1/[resource]/` | Listado |
| GET | `/api/v1/[resource]/{id}/` | Detalle |
| POST | `/api/v1/[resource]/` | Crear |
| PATCH | `/api/v1/[resource]/{id}/` | Modificar |
| DELETE | `/api/v1/[resource]/{id}/` | Eliminar |

### Filtros esperados

```txt
?search=
?category=
?city=
?distance=
?budget=
?date=
?status=