# SPRINT_0.md

# Sprint 0 - Cimientos del Proyecto

## 1. Regla de oro

> No se programan funcionalidades de negocio complejas durante Sprint 0.

El objetivo de Sprint 0 es construir la base técnica y arquitectónica de Planify para que las futuras funcionalidades puedan desarrollarse de forma ordenada, segura y escalable.

---

## 2. Objetivos del Sprint 0

Al finalizar Sprint 0 el proyecto debe contar con:

- arquitectura definida;
- documentación completa;
- backend operativo;
- frontend operativo;
- autenticación funcional;
- permisos base;
- base de datos configurada;
- Docker funcional;
- comunicación frontend-backend;
- estructura modular lista para crecimiento.

---

## 3. Distribución recomendada

| Área | Porcentaje |
|---|---:|
| Arquitectura y documentación | 30% |
| Backend base | 25% |
| Frontend base | 20% |
| Infraestructura y DevOps | 20% |
| Testing inicial | 5% |

---

## 4. Backend base

### Entregables obligatorios

- Repositorio Django configurado.
- Django REST Framework instalado.
- PostgreSQL conectado.
- Redis configurado.
- Configuración mediante variables de entorno.
- Sistema JWT funcionando.
- Modelo de Usuario implementado.
- Roles básicos definidos.
- Healthcheck disponible.
- Estructura modular basada en dominios.
- Service Layer implementada.
- Configuración inicial de auditoría.
- Configuración inicial de logs.
- Tests mínimos funcionando.

### Módulos a crear

```txt
backend/apps/

users/
events/
places/
activities/
promotions/
favorites/
recommendations/
notifications/
core/
audit/
```

### NO implementar todavía

- Motor de recomendaciones.
- Algoritmo de scoring.
- Favoritos completos.
- Eventos reales.
- Integraciones externas.
- Recordatorios.
- Promociones automáticas.

---

## 5. Frontend base

### Entregables obligatorios

- React + Vite.
- TypeScript.
- Tailwind CSS.
- TanStack Query.
- Zustand.
- React Hook Form.
- Zod.
- Cliente HTTP centralizado.
- Sistema de autenticación.
- Sistema de rutas.
- Layout principal.
- Página Home temporal.
- Página Login.
- Página Registro.
- Página Perfil básica.
- Componentes reutilizables.

### Componentes base

```txt
Button
Input
Card
Modal
Badge
Avatar
Navbar
Sidebar
Loading
EmptyState
ErrorState
```

### NO implementar todavía

- Diseño final.
- Dashboard completo.
- Mapa interactivo.
- Recomendaciones inteligentes.
- Calendario de eventos.
- Gestión avanzada de favoritos.

---

## 6. Base de datos inicial

### Entidades mínimas

#### User

```txt
id
email
password
first_name
last_name
role
created_at
updated_at
```

#### UserPreference

```txt
id
user_id
category
value
```

### Preparar estructura para futuras entidades

```txt
Event
Place
Activity
Promotion
Favorite
Recommendation
Notification
AuditLog
```

Las tablas pueden existir vacías o parcialmente implementadas.

---

## 7. Integraciones externas

Durante Sprint 0 solamente se preparará la infraestructura para futuras integraciones.

### APIs previstas

- Google Maps API
- Google Places API
- OpenWeather API
- Ticketmaster API
- Google OAuth

### Permitido

- Crear servicios vacíos.
- Crear interfaces.
- Configurar variables de entorno.

### Prohibido

- Consumir APIs reales.
- Implementar lógica de negocio dependiente de APIs externas.

---

## 8. DevOps inicial

### Entregables obligatorios

- Dockerfile Backend.
- Dockerfile Frontend.
- Docker Compose.
- PostgreSQL.
- Redis.
- Nginx.
- Variables de entorno.
- Scripts de inicialización.
- README de instalación.
- Healthchecks.

### Estructura esperada

```txt
docker/

nginx/
scripts/

docker-compose.yml
.env.example
```

---

## 9. Seguridad inicial

### Implementar

- JWT Authentication.
- Password hashing.
- Roles básicos.
- Permisos base.
- Variables sensibles fuera del repositorio.
- CORS configurado.
- Validaciones mínimas.

### No implementar aún

- MFA.
- OAuth completo.
- Rate limiting avanzado.
- Sistemas antifraude.

---

## 10. Testing inicial

### Backend

- Tests de autenticación.
- Tests de permisos.
- Tests de healthcheck.

### Frontend

- Render básico.
- Login.
- Rutas protegidas.

### Objetivo mínimo

```txt
Cobertura inicial >= 40%
```

---

## 11. Documentación obligatoria

Antes de avanzar a Sprint 1 deben existir y estar completos:

- PROJECT_CONTEXT.md
- ARCHITECTURE.md
- STACK.md
- RULES.md
- FOLDER_STRUCTURE.md
- WORKFLOW.md
- RBAC.md
- API_GUIDELINES.md
- SPRINT_0.md

---

## 12. Checklist de finalización

### Backend

- [ ] Django funcionando
- [ ] PostgreSQL conectado
- [ ] Redis conectado
- [ ] JWT funcionando
- [ ] Roles funcionando
- [ ] Healthcheck funcionando
- [ ] Tests básicos funcionando

### Frontend

- [ ] React funcionando
- [ ] Tailwind funcionando
- [ ] Auth funcionando
- [ ] Rutas funcionando
- [ ] Cliente API funcionando

### DevOps

- [ ] Docker funcionando
- [ ] Contenedores levantan correctamente
- [ ] Variables de entorno configuradas

### Documentación

- [ ] Toda la documentación completada
- [ ] Arquitectura validada
- [ ] Stack validado
- [ ] Permisos definidos

---

## 13. No permitido en Sprint 0

- Motor de recomendaciones final.
- Sistema de puntuación inteligente.
- Eventos reales.
- Promociones reales.
- Consumo de APIs externas.
- Integración con Ticketmaster.
- Integración con Google Maps.
- Calendario completo.
- Recordatorios automáticos.
- Notificaciones push.
- IA aplicada a recomendaciones.
- Dashboards avanzados.
- Métricas de negocio.

---

## 14. Salida de Sprint 0

El Sprint 0 estará aprobado cuando:

- El proyecto pueda ejecutarse localmente.
- Backend y frontend se comuniquen correctamente.
- Exista autenticación funcional.
- Existan permisos básicos.
- La base de datos migre sin errores.
- Docker funcione correctamente.
- La estructura modular esté completa.
- Los tests mínimos pasen correctamente.
- La documentación esté alineada y actualizada.

---

## 15. Resultado esperado

Al finalizar Sprint 0, Planify deberá estar preparado para comenzar Sprint 1 y desarrollar las primeras funcionalidades de negocio:

- eventos;
- lugares;
- actividades;
- favoritos;
- promociones;
- recomendaciones.

Sin necesidad de modificar la arquitectura principal.

---

## 16. Estado oficial

### Si todo está completo

```txt
SPRINT_0_STATUS: READY_FOR_FEATURES
```

### Si falta algún requisito

```txt
SPRINT_0_STATUS: BLOCKED

Motivo:
[Falta documentación, infraestructura o arquitectura]
```