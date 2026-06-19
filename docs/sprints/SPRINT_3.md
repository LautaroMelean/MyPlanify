# SPRINT_3.md

# Sprint 3 - Experiencia de Usuario y Recomendaciones Avanzadas

## 1. Objetivo

Completar funcionalidades visibles para el usuario final que ya están contempladas en la documentación del proyecto pero aún no fueron implementadas.

Este sprint busca transformar Planify desde una plataforma funcional hacia una experiencia completa de descubrimiento y planificación.

---

## 2. Estado previo

Sprint 0 finalizado.

Sprint 1 finalizado.

Sprint 2 finalizado.

Actualmente existen:

- autenticación JWT;
- perfiles de usuario;
- preferencias;
- lugares;
- eventos;
- actividades;
- favoritos;
- recordatorios;
- notificaciones;
- recomendaciones V1;
- mapa básico;
- auditoría;
- RBAC.

---

## 3. Objetivos del Sprint

### Objetivo principal

Implementar navegación completa, promociones y recomendaciones avanzadas.

---

## 4. Backend

### 4.1 Módulo Promotions

Crear nueva app:

```txt
backend/apps/promotions/
```

Implementar:

```txt
Promotion
PromotionService
PromotionSelector
PromotionSerializer
PromotionViewSet
PromotionPermissions
```

Endpoints:

```txt
GET    /api/v1/promotions/

GET    /api/v1/promotions/{id}/

POST   /api/v1/promotions/

PATCH  /api/v1/promotions/{id}/

DELETE /api/v1/promotions/{id}/
```

Permisos:

```txt
business_owner
admin
moderator
```

Validaciones:

- fecha inicio obligatoria;
- fecha fin obligatoria;
- fecha fin > fecha inicio;
- descuento válido;
- promoción activa.

---

### 4.2 Recomendaciones V2

Incorporar al motor:

#### Presupuesto

Utilizar:

```txt
Activity.min_budget
Activity.max_budget
Event.price
```

#### Cantidad de personas

Utilizar:

```txt
min_people
max_people
```

#### Edad mínima

Utilizar:

```txt
Event.minimum_age
```

#### Horario actual

Mejorar score según:

```txt
mañana
tarde
noche
```

---

### 4.3 Geolocalización real

Agregar:

```txt
latitude
longitude
```

al perfil del usuario.

Calcular:

```txt
distancia usuario ↔ lugar
```

mediante fórmula Haversine.

Incorporar distancia al score.

---

## 5. Frontend

### 5.1 Detalles de entidades

Crear páginas:

```txt
/features/events/pages/EventDetail.tsx

/features/places/pages/PlaceDetail.tsx

/features/activities/pages/ActivityDetail.tsx
```

Mostrar:

- información completa;
- favoritos;
- recordatorios;
- ubicación;
- eventos relacionados;
- promociones relacionadas.

---

### 5.2 Navegación desde Explorar

Las cards deben navegar a:

```txt
/events/:id

/places/:id

/activities/:id
```

---

### 5.3 Pantalla Promociones

Nueva ruta:

```txt
/promociones
```

Contenido:

- promociones activas;
- filtros;
- detalle;
- acceso rápido desde Home.

---

### 5.4 Geolocalización navegador

Implementar:

```txt
navigator.geolocation
```

Permitir:

- obtener ubicación;
- centrar mapa;
- guardar ubicación del usuario;
- mejorar recomendaciones.

---

## 6. Seguridad

Validar:

- permisos promociones;
- ownership promociones;
- auditoría promociones;
- validación coordenadas.

---

## 7. QA

Nuevos casos:

### Promotions

- crear;
- editar;
- eliminar;
- expirar.

### Recomendaciones

- presupuesto;
- edad;
- personas;
- proximidad.

### Navegación

- detalle actividad;
- detalle evento;
- detalle lugar.

---

## 8. Archivos esperados

Backend:

```txt
apps/promotions/*
```

Frontend:

```txt
features/promotions/*
features/events/pages/EventDetail.tsx
features/places/pages/PlaceDetail.tsx
features/activities/pages/ActivityDetail.tsx
```

---

## 9. Definition of Done

Sprint 3 estará completo cuando:

- exista módulo Promotions;
- existan detalles navegables;
- exista geolocalización real;
- recomendaciones utilicen presupuesto;
- recomendaciones utilicen edad;
- recomendaciones utilicen cantidad de personas;
- recomendaciones utilicen distancia;
- existan tests backend;
- documentación actualizada.

---

## 10. Salida esperada

Al finalizar:

```txt
SPRINT_3_STATUS: READY
```