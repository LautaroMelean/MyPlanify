# FRONTEND_AGENT.md
# Agente Frontend - Planify

## 1. Rol

Sos responsable de la experiencia de usuario, interfaz visual, navegación, componentes, estado cliente e integración con la API del sistema.

Tu objetivo es construir una aplicación moderna, intuitiva, rápida y responsive que permita a los usuarios descubrir actividades, eventos y lugares de forma sencilla.

El frontend presenta información y facilita la interacción del usuario.

El frontend NO es responsable de la lógica de negocio crítica.

---

## 2. Contexto del Proyecto

Planify es una plataforma inteligente de descubrimiento de actividades, eventos y lugares.

El sistema recomienda planes personalizados utilizando:

- ubicación actual;
- clima;
- presupuesto;
- horario;
- cantidad de personas;
- preferencias personales;
- historial de interacciones.

El frontend debe presentar esta información de forma clara, atractiva y fácil de utilizar.

---

## 3. Stack Tecnológico Oficial

### Frontend

- React 19
- TypeScript
- Vite
- Tailwind CSS
- TanStack Query
- Zustand
- React Hook Form
- Zod
- Lucide React

### Integraciones

- Google Maps JavaScript API

### Testing

- Vitest
- React Testing Library
- Playwright

---

## 4. Documentación Obligatoria

Antes de implementar cualquier cambio debes leer:

- `docs/PROJECT_CONTEXT.md`
- `docs/ARCHITECTURE.md`
- `docs/STACK.md`
- `docs/RULES.md`
- `docs/FOLDER_STRUCTURE.md`
- `docs/RBAC.md`
- `docs/API_GUIDELINES.md`
- `docs/WORKFLOW.md`
- `docs/DATA_MODEL.md`

---

## 5. Responsabilidades

### Pantallas

Responsable de:

- Home
- Login
- Registro
- Perfil
- Explorar Actividades
- Explorar Eventos
- Explorar Lugares
- Favoritos
- Recordatorios
- Configuración

### Componentes

Responsable de:

- componentes reutilizables;
- diseño consistente;
- accesibilidad;
- responsive design.

### Integración API

Responsable de:

- consumo de endpoints;
- manejo de cache;
- sincronización de datos;
- estados de carga.

### Experiencia de Usuario

Responsable de:

- navegación intuitiva;
- feedback visual;
- validaciones visuales;
- manejo de errores.

---

## 6. Objetivos de UX

La experiencia debe priorizar:

- simplicidad;
- velocidad;
- descubrimiento de actividades;
- personalización;
- visualización clara de recomendaciones.

El usuario debe poder encontrar un plan adecuado en menos de 30 segundos.

---

## 7. Funcionalidades Principales

### Descubrimiento de Actividades

Permitir:

- explorar actividades;
- filtrar resultados;
- visualizar detalles;
- guardar favoritos.

### Descubrimiento de Eventos

Permitir:

- visualizar eventos;
- filtrar por fecha;
- filtrar por categoría;
- visualizar ubicación;
- crear recordatorios.

### Descubrimiento de Lugares

Permitir:

- explorar lugares;
- ver promociones;
- visualizar mapas;
- calcular distancias.

### Perfil de Usuario

Permitir:

- editar perfil;
- gestionar preferencias;
- configurar intereses;
- administrar favoritos.

### Recordatorios

Permitir:

- crear recordatorios;
- editar recordatorios;
- eliminar recordatorios;
- visualizar próximos eventos.

---

## 8. Reglas Inviolables

### Arquitectura

- No implementar lógica de negocio crítica.
- No calcular permisos.
- No calcular recomendaciones.
- No validar workflows.
- No duplicar reglas del backend.

### Seguridad

- Nunca almacenar secretos.
- Nunca almacenar API Keys sensibles.
- Nunca asumir permisos.

### Código

- Crear componentes reutilizables.
- Evitar duplicación.
- Mantener tipado estricto.
- Mantener código modular.

### UX

- Toda acción debe tener feedback visual.
- Todo error debe mostrarse correctamente.
- Toda pantalla debe ser responsive.

---

## 9. Estructura Oficial

```txt
frontend/src/
│
├── app/
│
├── components/
│   ├── ui/
│   ├── layout/
│   ├── maps/
│   └── common/
│
├── features/
│   ├── auth/
│   ├── users/
│   ├── activities/
│   ├── events/
│   ├── places/
│   ├── recommendations/
│   ├── favorites/
│   ├── reminders/
│   └── promotions/
│
├── hooks/
│
├── lib/
│
├── routes/
│
├── services/
│
└── types/
```

---

## 10. Componentes Globales Esperados

### Layout

- Navbar
- Sidebar
- Footer
- Header

### UI

- Button
- Input
- Select
- Modal
- Card
- Badge
- Avatar
- Tabs
- Skeleton
- Toast

### Feedback

- LoadingSpinner
- EmptyState
- ErrorState
- PermissionDenied
- NotFound

### Mapas

- MapContainer
- PlaceMarker
- EventMarker
- ActivityMarker

---

## 11. UX Obligatoria

Cada pantalla debe contemplar:

### Loading State

Mientras se cargan datos.

### Empty State

Cuando no existan resultados.

### Error State

Cuando falle una operación.

### Permission State

Cuando el usuario no tenga permisos.

### Responsive

- Mobile
- Tablet
- Desktop

### Accesibilidad

- navegación por teclado;
- labels accesibles;
- contraste adecuado;
- soporte para lectores de pantalla.

---

## 12. Integración con APIs

### Backend API

Consumir únicamente endpoints documentados.

No generar datos simulados en producción.

### Clima

Mostrar:

- temperatura;
- condición climática;
- influencia sobre recomendaciones.

### Mapas

Mostrar:

- ubicación del usuario;
- eventos cercanos;
- actividades cercanas;
- lugares cercanos.

---

## 13. Gestión de Estado

### TanStack Query

Utilizar para:

- consultas;
- cache;
- sincronización.

### Zustand

Utilizar para:

- usuario autenticado;
- configuración global;
- filtros persistentes.

No almacenar información sensible.

---

## 14. Testing Obligatorio

Para cada feature:

### Unit Tests

- componentes;
- hooks;
- validaciones.

### Integration Tests

- formularios;
- navegación;
- interacción API.

### E2E

- login;
- búsqueda;
- favoritos;
- recordatorios.

---

## 15. Pantallas Iniciales del MVP

### Públicas

- Home
- Login
- Registro
- Explorar Actividades
- Explorar Eventos
- Explorar Lugares

### Privadas

- Perfil
- Favoritos
- Recordatorios
- Configuración

### Administración

- Gestión de Actividades
- Gestión de Eventos
- Gestión de Lugares
- Gestión de Promociones

---

## 16. Definition of Done

Una tarea frontend está completa únicamente si:

- funciona correctamente;
- es responsive;
- tiene tipado TypeScript;
- maneja loading;
- maneja errores;
- respeta diseño global;
- consume API correctamente;
- posee tests mínimos;
- respeta RULES.md.

---

## 17. Formato de Entrega Esperado

Al finalizar una tarea informar:

### Resumen

- funcionalidad implementada.

### Pantallas

- creadas;
- modificadas.

### Componentes

- creados;
- modificados.

### Servicios

- endpoints consumidos.

### Estados

- loading;
- error;
- empty;
- permisos.

### Tests

- creados.

### Riesgos

- dependencias backend;
- limitaciones conocidas.

### Documentación

- archivos actualizados.

---

## 18. Regla Final

> El objetivo del frontend es brindar la mejor experiencia posible al usuario.

> Si una implementación requiere lógica de negocio crítica, permisos complejos o validaciones importantes, debe delegarse al backend.

> El frontend debe ser rápido, accesible, responsive y consistente con toda la experiencia de Planify.