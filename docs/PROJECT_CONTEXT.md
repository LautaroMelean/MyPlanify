# PROJECT_CONTEXT.md

# Contexto del Proyecto

## 1. Nombre del proyecto

**Nombre:** `Planify`

**Descripción breve:**

Planify es una aplicación web que recomienda actividades, eventos, lugares y planes personalizados según el clima, la ubicación, el horario, el presupuesto y las preferencias del usuario. El sistema busca facilitar el descubrimiento de opciones de entretenimiento personalizadas en tiempo real.

---

## 2. Problema que resuelve

### Situación actual

- Las personas suelen repetir actividades por no encontrar opciones nuevas o adecuadas para cada situación.
- Encontrar actividades según el clima, ubicación y presupuesto requiere utilizar múltiples aplicaciones diferentes.
- La información de eventos, lugares y promociones se encuentra fragmentada en distintas plataformas.
- No existe una plataforma simple que centralice recomendaciones sociales personalizadas en tiempo real.

### Dolor principal

> Los usuarios pierden tiempo buscando actividades o lugares adecuados según su contexto actual.

---

## 3. Objetivo del sistema

El sistema debe permitir:

- Registro e inicio de sesión de usuarios.
- Gestión de perfiles personalizados.
- Recomendar actividades, eventos y lugares según el contexto del usuario.
- Filtrar planes según presupuesto, horario, día y ubicación.
- Mostrar opciones disponibles en tiempo real dependiendo del clima.
- Permitir que cada usuario configure preferencias y gustos en su perfil.
- Recomendar actividades según la cantidad de personas indicadas por el usuario.
- Filtrar actividades por rango etario.
- Mostrar ofertas, promociones y festividades disponibles en locales asociados.
- Mostrar eventos disponibles en la ciudad cada día.
- Permitir guardar actividades, eventos y lugares favoritos.
- Permitir crear recordatorios para eventos futuros.
- Mostrar actividades y lugares sobre un mapa interactivo.
- Generar planes personalizados compuestos por múltiples actividades, eventos o lugares.
- Aprender progresivamente de las preferencias e interacciones del usuario.
- Recomendar actividades mediante un sistema de puntuación contextual.
- Permitir que negocios asociados publiquen promociones y beneficios.
- Permitir que organizadores mantengan información actualizada de sus eventos.
- Centralizar información relevante para la toma de decisiones de ocio y entretenimiento.

---

## 4. Usuarios principales

| Usuario / Actor | Descripción | Necesidad principal |
|---|---|---|
| Usuario general | Persona que busca actividades o entretenimiento. | Encontrar planes rápidos y personalizados. |
| Administrador | Responsable de gestionar el sistema. | Administrar información y supervisar la plataforma. |
| Negocio asociado | Bar, restaurante o local registrado. | Dar visibilidad a sus servicios, promociones y eventos. |
| Organizador de eventos | Responsable de publicar eventos. | Promocionar actividades y eventos. |
| Moderador | Usuario encargado de validar contenido. | Mantener la calidad y confiabilidad de la información. |

---

## 5. Alcance inicial

### Incluido en el MVP

- Registro e inicio de sesión.
- Geolocalización del usuario.
- Consulta del clima en tiempo real mediante API.
- Visualización de eventos y lugares.
- Sistema de recomendaciones.
- Filtros por presupuesto, categoría y distancia.
- Sistema de favoritos.
- Sistema de recordatorios.
- Mapa interactivo.
- Consulta de promociones activas.

### Fuera de alcance inicial

- Sistema de pagos online.
- Aplicación móvil nativa.
- Compra de entradas dentro de la plataforma.
- Sistema de mensajería entre usuarios.
- Integración con redes sociales.
- Motor de IA avanzado.
- Sistema de suscripciones premium.

---

## 6. Reglas del negocio

| Regla | Descripción | Impacto técnico |
|---|---|---|
| Filtrado por clima | Las actividades deben adaptarse al clima actual. | Integración con API climática. |
| Filtrado por ubicación | El sistema solo mostrará actividades dentro del rango seleccionado. | Geolocalización y mapas. |
| Filtrado por intereses | El sistema priorizará actividades relacionadas con los gustos del usuario. | Uso de preferencias almacenadas. |
| Filtrado por disponibilidad | Las actividades deben mostrarse según disponibilidad. | Validaciones de negocio. |
| Filtrado por presupuesto | El sistema mostrará actividades acordes al presupuesto definido. | Clasificación y filtrado. |
| Filtrado por edad | Se respetarán restricciones etarias. | Validaciones de negocio. |
| Motor de recomendación | Las recomendaciones se calcularán mediante un score contextual. | Algoritmo de scoring. |
| Aprendizaje de preferencias | El sistema registrará interacciones para mejorar recomendaciones futuras. | Historial de interacción. |
| Promociones vigentes | Solo se mostrarán promociones activas. | Validaciones temporales. |

---

## 7. Glosario del dominio

| Término | Definición |
|---|---|
| Actividad | Plan o entretenimiento sugerido al usuario. |
| Evento | Actividad programada con fecha y ubicación definida. |
| Lugar | Ubicación física asociada a actividades o servicios. |
| Plan | Conjunto de actividades, lugares o eventos sugeridos al usuario. |
| PerfilUsuario | Información utilizada para personalizar recomendaciones. |
| HistorialInteraccion | Registro de acciones realizadas por el usuario. |
| Score de recomendación | Valor calculado para determinar la relevancia de una sugerencia. |
| Geolocalización | Ubicación actual obtenida desde el navegador. |
| Outdoor | Actividad al aire libre. |
| Indoor | Actividad en espacios cerrados. |
| API | Servicio externo utilizado por el sistema. |
| MVP | Versión inicial del producto. |

---

## 8. Métricas de éxito

El proyecto será considerado exitoso si:

- El usuario encuentra una actividad relevante en menos de 30 segundos.
- El tiempo promedio de respuesta es menor a 3 segundos.
- Más del 70% de los usuarios utilizan favoritos o recordatorios.
- Las recomendaciones son consistentes con las preferencias configuradas.
- Los usuarios pueden encontrar información útil sin consultar múltiples plataformas externas.

---

## 9. Restricciones conocidas

- Dependencia de APIs externas para clima, mapas y eventos.
- Límites de uso de planes gratuitos.
- Tiempo limitado para desarrollo del MVP.
- Presupuesto reducido para infraestructura.
- Dependencia de la disponibilidad de servicios externos.

---

## 10. Criterios de aceptación del MVP

- El sistema obtiene correctamente la ubicación del usuario.
- El sistema consulta correctamente el clima actual.
- El sistema muestra actividades según clima, ubicación y horario.
- El usuario puede aplicar filtros personalizados.
- El usuario puede guardar actividades favoritas.
- El usuario puede crear recordatorios.
- El usuario puede visualizar lugares y eventos en un mapa interactivo.
- El sistema muestra promociones activas cuando existan.
- El sistema mantiene tiempos de respuesta aceptables.
- El sistema genera recomendaciones acordes a las preferencias configuradas.