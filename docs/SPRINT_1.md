# SPRINT_1.md

# Sprint 1 - MVP Funcional Inicial de Planify

## 1. Objetivo del Sprint

Construir la primera versión funcional de Planify permitiendo:

- Registro e inicio de sesión de usuarios.
- Gestión básica de perfiles.
- Obtención de ubicación del usuario.
- Consulta de clima mediante API externa.
- Visualización de actividades, eventos y lugares.
- Sistema de favoritos.
- Motor básico de recomendaciones contextuales.
- Primer mapa interactivo funcional.

---

## 2. Alcance

### Incluido

- Autenticación JWT.
- Registro de usuarios.
- Login y logout.
- Perfil de usuario.
- Preferencias del usuario.
- Geolocalización.
- Integración con API de clima.
- CRUD de Places.
- CRUD de Activities.
- CRUD de Events.
- Sistema de favoritos.
- Endpoints de recomendaciones.
- Visualización de mapa.
- Auditoría básica.
- Notificaciones internas simples.

### Excluido

- Motor de IA avanzado.
- Machine Learning.
- Aplicación móvil.
- Pagos.
- Reservas.
- Redes sociales.
- Chat.
- Sistema de reviews.
- Gamificación.
- Notificaciones push.

---

## 3. Módulos a implementar

| Módulo | Prioridad |
|----------|----------|
| Users | Alta |
| Authentication | Alta |
| Preferences | Alta |
| Places | Alta |
| Activities | Alta |
| Events | Alta |
| Favorites | Alta |
| Recommendations | Alta |
| Maps | Media |
| Notifications | Media |
| Audit Logs | Media |

---

## 4. Backend

### Apps Django a crear

```txt
backend/apps/

users/
places/
activities/
events/
favorites/
recommendations/
notifications/
audit/
core/
```

---

### Entidades mínimas

Implementar según:

```txt
docs/DATA_MODEL.md
```

Entidades MVP:

```txt
User
UserPreference
Place
Activity
Event
Favorite
Recommendation
Notification
AuditLog
```

---

### Endpoints mínimos

#### Auth

```txt
POST   /api/v1/auth/register/
POST   /api/v1/auth/login/
POST   /api/v1/auth/logout/
POST   /api/v1/auth/refresh/
GET    /api/v1/auth/me/
```

---

#### Users

```txt
GET    /api/v1/users/me/
PATCH  /api/v1/users/me/
```

---

#### Preferences

```txt
GET    /api/v1/preferences/
POST   /api/v1/preferences/
PATCH  /api/v1/preferences/{id}/
DELETE /api/v1/preferences/{id}/
```

---

#### Places

```txt
GET    /api/v1/places/
GET    /api/v1/places/{id}/
POST   /api/v1/places/
PATCH  /api/v1/places/{id}/
DELETE /api/v1/places/{id}/
```

---

#### Activities

```txt
GET    /api/v1/activities/
GET    /api/v1/activities/{id}/
POST   /api/v1/activities/
PATCH  /api/v1/activities/{id}/
DELETE /api/v1/activities/{id}/
```

---

#### Events

```txt
GET    /api/v1/events/
GET    /api/v1/events/{id}/
POST   /api/v1/events/
PATCH  /api/v1/events/{id}/
DELETE /api/v1/events/{id}/
```

---

#### Favorites

```txt
GET    /api/v1/favorites/
POST   /api/v1/favorites/
DELETE /api/v1/favorites/{id}/
```

---

#### Recommendations

```txt
GET /api/v1/recommendations/
```

---

## 5. Integraciones externas

### Weather API

Responsabilidad:

```txt
Obtener clima actual del usuario.
```

Datos utilizados:

```txt
Temperatura
Condición climática
Probabilidad de lluvia
```

Uso:

```txt
Filtrar actividades indoor/outdoor.
```

---

### Maps API

Responsabilidad:

```txt
Mostrar actividades y lugares cercanos.
```

Funciones:

```txt
Mapa interactivo
Marcadores
Distancia
Geolocalización
```

---

## 6. Frontend

### Pantallas iniciales

#### Públicas

```txt
Landing
Login
Registro
```

---

#### Privadas

```txt
Home
Explorar
Mapa
Favoritos
Perfil
Configuración
```

---

### Componentes base

```txt
Navbar
Sidebar
Footer
SearchBar
FiltersPanel
ActivityCard
EventCard
PlaceCard
RecommendationCard
MapComponent
FavoriteButton
LoadingState
EmptyState
ErrorState
```

---

## 7. Motor de recomendación MVP

### Variables consideradas

```txt
Clima
Ubicación
Presupuesto
Cantidad de personas
Horario
Preferencias
```

---

### Fórmula inicial

```txt
Score =
preferencias +
distancia +
clima +
presupuesto +
popularidad
```

---

### Objetivo

Generar recomendaciones simples basadas en reglas.

Sin IA.

Sin Machine Learning.

---

## 8. Testing obligatorio

### Backend

```txt
Auth Tests
Permissions Tests
CRUD Tests
Recommendation Tests
Favorite Tests
API Tests
```

---

### Frontend

```txt
Component Tests
Page Tests
Navigation Tests
```

---

### E2E

```txt
Registro
Login
Guardar favorito
Consultar recomendaciones
```

---

## 9. Criterios de aceptación

### Backend

- Todas las migraciones ejecutan correctamente.
- Todos los endpoints responden.
- JWT funcional.
- Permisos aplicados.
- Auditoría funcionando.

---

### Frontend

- Navegación funcional.
- Responsive básico.
- Integración API completa.
- Estados loading/error/empty implementados.

---

### Integración

- Usuario puede registrarse.
- Usuario puede iniciar sesión.
- Usuario puede configurar preferencias.
- Usuario puede consultar actividades.
- Usuario puede guardar favoritos.
- Usuario puede visualizar lugares en el mapa.
- Usuario recibe recomendaciones.

---

## 10. Definition of Done

Sprint 1 estará completo cuando:

- Todos los módulos MVP funcionen.
- Existan tests mínimos.
- Exista documentación actualizada.
- Backend y frontend estén integrados.
- Docker siga funcionando.
- No existan errores críticos abiertos.

---

## 11. Salida esperada

Al finalizar Sprint 1:

```txt
SPRINT_1_STATUS: MVP_FUNCTIONAL
```

Planify deberá poder ser utilizado por usuarios reales para:

- descubrir actividades;
- explorar lugares;
- visualizar eventos;
- guardar favoritos;
- recibir recomendaciones contextuales.