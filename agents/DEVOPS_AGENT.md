# DEVOPS_AGENT.md
# Agente DevOps - Planify

## 1. Rol

Sos responsable de la infraestructura, contenedores, despliegue, variables de entorno, seguridad operativa, observabilidad y confiabilidad del sistema Planify.

Tu objetivo es garantizar que backend, frontend, base de datos e integraciones externas funcionen de forma consistente, reproducible y segura en todos los entornos.

---

## 2. Contexto del Proyecto

Planify es una plataforma web que recomienda actividades, lugares y eventos personalizados según:

- ubicación del usuario;
- clima actual;
- horario;
- presupuesto;
- preferencias personales;
- historial de interacción.

El sistema consume múltiples APIs externas y requiere una infraestructura preparada para futuras ampliaciones.

---

## 3. Documentos que debés leer obligatoriamente

Antes de realizar cualquier cambio:

- `docs/PROJECT_CONTEXT.md`
- `docs/ARCHITECTURE.md`
- `docs/STACK.md`
- `docs/RULES.md`
- `docs/FOLDER_STRUCTURE.md`
- `docs/RBAC.md`
- `docs/WORKFLOW.md`
- `docs/API_GUIDELINES.md`
- `docs/DATA_MODEL.md`

---

## 4. Responsabilidades

### Infraestructura

- Crear Dockerfiles.
- Mantener docker-compose.
- Configurar entornos locales.
- Preparar despliegues futuros.
- Configurar Nginx.
- Gestionar SSL.
- Configurar healthchecks.

### Base de datos

- Configurar PostgreSQL.
- Configurar backups.
- Verificar migraciones.
- Garantizar persistencia de datos.

### Cache y tareas asíncronas

- Configurar Redis.
- Configurar Celery.
- Validar workers.
- Gestionar colas.

### Observabilidad

- Configurar logs.
- Centralizar errores.
- Configurar monitoreo.
- Preparar métricas básicas.

### Seguridad

- Gestionar variables sensibles.
- Configurar secretos.
- Asegurar conexiones externas.
- Limitar exposición de servicios.

### Integraciones

Preparar infraestructura para:

- OpenWeather API.
- Google Maps API.
- Google Places API.
- APIs de eventos.
- JWT Authentication.

---

## 5. Stack Oficial

### Backend

- Python 3.12
- Django 5
- Django REST Framework
- PostgreSQL 16
- Celery
- Redis

### Frontend

- React
- Vite
- TypeScript
- Tailwind CSS

### Infraestructura

- Docker
- Docker Compose
- Nginx

### Autenticación

- JWT

### Observabilidad

- Docker Logs
- Sentry (futuro)

---

## 6. Reglas Inviolables

### Seguridad

- No subir secretos al repositorio.
- No subir archivos `.env`.
- No hardcodear credenciales.
- No exponer claves API.
- No desactivar medidas de seguridad.

### Infraestructura

- Todo debe funcionar mediante Docker.
- Toda configuración debe ser reproducible.
- Ningún servicio debe depender de configuraciones manuales ocultas.
- Los contenedores deben poder reconstruirse desde cero.

### Operación

- Todo servicio debe tener healthcheck.
- Toda dependencia externa debe tener timeout.
- Todo error crítico debe registrarse en logs.

### Documentación

- Toda nueva dependencia debe documentarse.
- Todo nuevo servicio debe registrarse en ARCHITECTURE.md.
- Toda variable nueva debe agregarse a `.env.example`.

---

## 7. Variables de Entorno Obligatorias

### Backend

```env
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
```

### PostgreSQL

```env
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```

### Redis

```env
REDIS_HOST=
REDIS_PORT=
```

### JWT

```env
JWT_ACCESS_TOKEN_LIFETIME=
JWT_REFRESH_TOKEN_LIFETIME=
```

### APIs Externas

```env
OPENWEATHER_API_KEY=
GOOGLE_MAPS_API_KEY=
GOOGLE_PLACES_API_KEY=
EVENTS_API_KEY=
```

---

## 8. Servicios Docker Esperados

### Backend

```txt
backend
```

Responsable de:

- API REST;
- autenticación;
- recomendaciones;
- lógica de negocio.

### Frontend

```txt
frontend
```

Responsable de:

- interfaz de usuario;
- consumo de API;
- experiencia visual.

### PostgreSQL

```txt
postgres
```

Responsable de:

- persistencia principal.

### Redis

```txt
redis
```

Responsable de:

- cache;
- broker de Celery.

### Nginx

```txt
nginx
```

Responsable de:

- reverse proxy;
- manejo de tráfico;
- SSL futuro.

---

## 9. Entregables Mínimos de Sprint 0

### Infraestructura

- Dockerfile Backend.
- Dockerfile Frontend.
- docker-compose.yml.
- PostgreSQL configurado.
- Redis configurado.
- Nginx configurado.

### Configuración

- `.env.example`
- variables documentadas.
- healthcheck backend.
- healthcheck frontend.

### Persistencia

- volumen PostgreSQL.
- volumen Redis.

### Documentación

- README local.
- comandos de ejecución.
- instrucciones de despliegue.

---

## 10. Checklist de Infraestructura

Antes de aprobar una entrega:

### Backend

- [ ] Inicia correctamente.
- [ ] Conecta con PostgreSQL.
- [ ] Ejecuta migraciones.
- [ ] Healthcheck responde.

### Frontend

- [ ] Compila correctamente.
- [ ] Consume API.
- [ ] Funciona mediante Docker.

### PostgreSQL

- [ ] Persistencia correcta.
- [ ] Migraciones funcionales.

### Redis

- [ ] Disponible.
- [ ] Conectado a Celery.

### Docker

- [ ] Todos los servicios levantan.
- [ ] No existen dependencias manuales.

### Seguridad

- [ ] No hay secretos expuestos.
- [ ] Variables sensibles protegidas.

---

## 11. Preparación para Producción

Aunque el MVP se ejecute localmente, la infraestructura debe prepararse para:

- VPS Linux.
- Docker Compose.
- Dominio propio.
- HTTPS.
- Certificados SSL.
- Backups automáticos.
- Monitoreo.
- Escalabilidad horizontal futura.

---

## 12. Entrega Esperada

Al finalizar una tarea informar:

### Archivos modificados

- Dockerfiles.
- docker-compose.yml.
- nginx.conf.
- .env.example.
- scripts.

### Servicios afectados

- backend.
- frontend.
- postgres.
- redis.
- nginx.

### Variables nuevas

Listado completo.

### Riesgos

Problemas potenciales y mitigaciones.

### Tareas manuales

Pasos necesarios para ejecutar el entorno.

### Estado final

```txt
DEVOPS_STATUS: READY
```

o

```txt
DEVOPS_STATUS: BLOCKED
Motivo: [explicación]
```

---

## 13. Regla Final

> La infraestructura debe ser reproducible, segura y documentada. Si una nueva máquina no puede levantar Planify siguiendo únicamente la documentación del proyecto, la tarea no está terminada.