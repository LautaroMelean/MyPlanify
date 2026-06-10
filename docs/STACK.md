# STACK.md
# Stack Tecnológico Oficial

## 1. Principio

> Ningún agente puede cambiar tecnología, librería principal, framework o patrón de arquitectura sin aprobación del Orchestrator y registro ADR.

---

## 2. Backend

| Componente | Tecnología oficial | Versión / Nota |
|---|---|---|
| Lenguaje | Python | 3.13 |
| Framework | Django | 5.2 |
| API | Django REST Framework | API principal del sistema |
| Autenticación | JWT | Access Token + Refresh Token |
| Tareas async | Celery | Procesamiento de tareas en segundo plano |
| Cache / broker | Redis | Cache y broker para Celery |

---

## 3. Base de datos

| Componente | Tecnología |
|---|---|
| Motor principal | PostgreSQL |
| Migraciones | Django Migrations |
| Backups | Dump automático diario de base de datos |
| Multi-tenant | No aplica (Single-tenant) |

### Consideraciones de base de datos

- PostgreSQL será la única fuente de verdad para los datos del sistema.
- Todas las entidades principales deberán incluir `created_at` y `updated_at`.
- Las migraciones deberán mantenerse versionadas junto al código fuente.
- Los backups deberán poder restaurarse completamente en un entorno nuevo.

---

## 4. Frontend

| Componente | Tecnología |
|---|---|
| Framework | React |
| Build tool | Vite |
| Lenguaje | TypeScript |
| Estilos | Tailwind CSS |
| Estado cliente | Zustand |
| Server state | TanStack Query |
| Formularios | React Hook Form |
| Validaciones | Zod |
| Íconos | Lucide React |

### Consideraciones Frontend

- Toda la lógica de negocio debe residir en el backend.
- React solo será responsable de presentación y experiencia de usuario.
- Las validaciones críticas deberán ejecutarse también en backend.
- El frontend consumirá únicamente endpoints oficiales de la API.

---

## 5. DevOps

| Componente | Tecnología |
|---|---|
| Contenedores | Docker + Docker Compose |
| Proxy | Nginx |
| SSL | Let's Encrypt + Certbot |
| CI/CD | GitHub Actions |
| Logs | Docker Logs + Sentry |
| Observabilidad | Sentry |

### Objetivos DevOps

- Entornos reproducibles mediante Docker.
- Despliegues automatizados mediante GitHub Actions.
- Monitoreo centralizado de errores.
- Configuración basada en variables de entorno.

---

## 6. Testing

| Capa | Herramienta |
|---|---|
| Backend unit tests | Pytest |
| API tests | Pytest + APIClient |
| Frontend tests | Vitest + Testing Library |
| E2E | Playwright |
| Lint | Ruff + ESLint |
| Format | Black + Prettier |

### Cobertura mínima

- Toda lógica de negocio crítica debe poseer tests.
- Los endpoints principales deben poseer pruebas de integración.
- Los flujos principales del usuario deben poseer pruebas E2E.

---

## 7. Integraciones externas

| Servicio | API | Propósito |
|---|---|---|
| Clima | OpenWeather API | Obtener clima actual y pronóstico |
| Mapas | Google Maps API | Visualización de mapas y navegación |
| Geolocalización | Google Geocoding API | Conversión entre direcciones y coordenadas |
| Lugares | Google Places API | Restaurantes, bares, cafeterías, cines y puntos de interés |
| Eventos | Ticketmaster Discovery API | Consulta de eventos, espectáculos y actividades |
| Autenticación Social | Google OAuth | Inicio de sesión con Google |

### Reglas de integración

- Ninguna API externa debe ser consumida directamente desde el frontend.
- Todas las integraciones deberán pasar por el backend.
- Los errores de APIs externas deberán manejarse de forma controlada.
- Se deberá implementar cache cuando sea apropiado para reducir consumo de cuota.

---

## 8. Convenciones de versiones

- Backend y frontend deben tener versiones documentadas.
- Las migraciones deben ser reproducibles.
- Los cambios de API deben ser compatibles o versionados.
- Las dependencias críticas deben fijarse mediante lockfiles.
- Los cambios tecnológicos relevantes deberán registrarse mediante ADR.

---

## 9. Librerías prohibidas sin autorización

- Librerías abandonadas.
- Librerías sin mantenimiento.
- Librerías que dupliquen funcionalidades existentes.
- Librerías que agreguen peso excesivo al frontend.
- Librerías que afecten seguridad o privacidad sin revisión.
- Librerías instaladas únicamente por conveniencia sin justificación técnica.

---

## 10. Comandos base

```bash
# Backend
python manage.py migrate
python manage.py runserver
pytest

# Frontend
npm install
npm run dev
npm run build
npm run test

# Docker
docker compose up -d --build
docker compose logs -f
```

## 11. Decisiones tecnológicas aprobadas

### Backend

- Python 3.13
- Django 5.2
- Django REST Framework
- JWT Authentication
- Celery
- Redis

### Frontend

- React
- Vite
- TypeScript
- Tailwind CSS
- Zustand
- TanStack Query
- React Hook Form
- Zod

### Base de datos

- PostgreSQL

### Infraestructura

- Docker
- Docker Compose
- Nginx
- GitHub Actions
- Sentry

### APIs externas

- OpenWeather API
- Google Maps API
- Google Geocoding API
- Google Places API
- Ticketmaster Discovery API
- Google OAuth