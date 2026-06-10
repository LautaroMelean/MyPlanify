# SPRINT_2.md

# Sprint 2 - Motor de Recomendaciones y Descubrimiento

## 1. Regla de oro

> Sprint 2 incorpora la inteligencia funcional de Planify utilizando los cimientos construidos en Sprint 0 y Sprint 1.

No se permiten cambios arquitectónicos mayores sin ADR aprobado.

---

# 2. Objetivo general

Construir el primer flujo de valor completo para el usuario:

```txt
Registro
→ Configuración de preferencias
→ Descubrimiento de actividades
→ Recomendaciones personalizadas
→ Favoritos
→ Recordatorios
→ Notificaciones
```

Al finalizar Sprint 2, un usuario deberá poder recibir sugerencias relevantes según sus preferencias.

---

# 3. Módulos incluidos

| Módulo | Estado |
|----------|----------|
| User Preferences | Sprint 2 |
| Activities | Sprint 2 |
| Places | Sprint 2 |
| Events | Sprint 2 |
| Recommendation Engine V1 | Sprint 2 |
| Favorites | Sprint 2 |
| Reminders | Sprint 2 |
| Notifications | Sprint 2 |

---

# 4. Backend

## Entidades a implementar

### UserPreference

```txt
User
 └── UserPreference
```

Permite almacenar gustos e intereses.

Ejemplos:

```txt
Música
Cine
Gaming
Tecnología
Deportes
Gastronomía
Turismo
```

---

### Place

Lugares físicos.

Ejemplos:

```txt
Restaurantes
Museos
Parques
Bares
Cines
```

---

### Event

Eventos asociados a lugares.

Ejemplos:

```txt
Conciertos
Festivales
Exposiciones
Eventos deportivos
```

---

### Activity

Actividades recomendables.

Ejemplos:

```txt
Ir al cine
Visitar museo
Salir a comer
Hacer deporte
```

---

### Favorite

Guardado de actividades, lugares o eventos.

---

### Reminder

Recordatorios programados.

---

### Notification

Notificaciones del sistema.

---

### Recommendation

Resultado del motor de recomendaciones.

---

# 5. Services obligatorios

Crear service layer para:

```txt
recommendation_service.py

favorites_service.py

reminder_service.py

notification_service.py

user_preference_service.py
```

Ninguna lógica compleja debe vivir en views.

---

# 6. API a implementar

## Preferencias

```txt
GET    /api/v1/preferences/

POST   /api/v1/preferences/

PATCH  /api/v1/preferences/{id}/

DELETE /api/v1/preferences/{id}/
```

---

## Actividades

```txt
GET /api/v1/activities/

GET /api/v1/activities/{id}/
```

---

## Lugares

```txt
GET /api/v1/places/

GET /api/v1/places/{id}/
```

---

## Eventos

```txt
GET /api/v1/events/

GET /api/v1/events/{id}/
```

---

## Favoritos

```txt
GET    /api/v1/favorites/

POST   /api/v1/favorites/

DELETE /api/v1/favorites/{id}/
```

---

## Recordatorios

```txt
GET    /api/v1/reminders/

POST   /api/v1/reminders/

DELETE /api/v1/reminders/{id}/
```

---

## Recomendaciones

```txt
GET /api/v1/recommendations/
```

---

## Notificaciones

```txt
GET   /api/v1/notifications/

PATCH /api/v1/notifications/{id}/read/
```

---

# 7. Frontend

## Pantallas nuevas

### Onboarding de preferencias

```txt
/ onboarding/preferences
```

Permite seleccionar intereses.

---

### Explorar actividades

```txt
/activities
```

---

### Explorar eventos

```txt
/events
```

---

### Explorar lugares

```txt
/places
```

---

### Recomendaciones

```txt
/recommendations
```

Pantalla principal de valor.

---

### Favoritos

```txt
/favorites
```

---

### Recordatorios

```txt
/reminders
```

---

### Notificaciones

```txt
/notifications
```

---

# 8. Recommendation Engine V1

## Objetivo

Generar recomendaciones simples utilizando reglas determinísticas.

---

## Factores de score

| Factor | Peso |
|----------|----------:|
| Preferencias del usuario | 40 |
| Categoría coincidente | 25 |
| Popularidad | 15 |
| Cercanía geográfica | 10 |
| Historial de interacción | 10 |

---

## Fórmula inicial

```txt
RecommendationScore =
PreferenceMatch +
CategoryMatch +
Popularity +
Distance +
InteractionHistory
```

---

## Fuera de alcance

No incluir:

```txt
Machine Learning
IA Generativa
Embeddings
LLMs
Deep Learning
```

Eso quedará para Sprint 4+.

---

# 9. Auditoría

Registrar:

```txt
favorite_created

favorite_removed

reminder_created

reminder_deleted

recommendation_generated

notification_read

preference_created

preference_updated
```

---

# 10. Seguridad

Validaciones obligatorias:

- Usuario autenticado.
- Ownership obligatorio.
- JWT válido.
- Scope own.
- Auditoría activa.
- Rate limit en endpoints públicos.

---

# 11. Testing

## Backend

Tests mínimos:

```txt
CRUD UserPreference

CRUD Favorites

CRUD Reminders

Recommendations

Permissions

Ownership

Audit Logs
```

---

## Frontend

Tests mínimos:

```txt
Pantallas cargan

Estados loading

Estados empty

Estados error

Protección de rutas

Favoritos

Recordatorios
```

---

## E2E

Flujo completo:

```txt
Registro

→ Login

→ Configurar preferencias

→ Ver recomendaciones

→ Guardar favorito

→ Crear recordatorio

→ Recibir notificación
```

---

# 12. Definition of Done

Sprint 2 estará completo cuando:

- existan recomendaciones funcionales;
- existan favoritos;
- existan recordatorios;
- existan notificaciones;
- existan preferencias configurables;
- frontend y backend estén integrados;
- existan tests mínimos;
- exista auditoría;
- exista documentación actualizada;
- QA apruebe los flujos.

---

# 13. Salida del Sprint

Al finalizar:

```txt
SPRINT_2_STATUS: READY_FOR_SPRINT_3
```

Si falta algún requisito:

```txt
SPRINT_2_STATUS: BLOCKED

Motivo: [explicación]
```