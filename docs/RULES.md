# RULES.md

# Constitución del Proyecto

Este documento contiene las reglas inviolables del proyecto.

Todo agente IA y todo desarrollador humano debe obedecerlas.

---

## 1. Reglas de arquitectura

- El backend es el source of truth.
- La lógica de negocio compleja vive exclusivamente en `services`.
- Los serializers validan estructura y formato, no gobiernan reglas de negocio.
- El frontend no decide permisos, recomendaciones, workflow ni reglas críticas.
- No se crea una carpeta nueva sin actualizar `FOLDER_STRUCTURE.md`.
- No se agrega una dependencia nueva sin justificarla.
- No se rompe compatibilidad de API sin registrar ADR.
- Toda integración externa debe pasar por el backend.
- Ninguna API externa debe ser consumida directamente desde el frontend.
- Ninguna funcionalidad debe implementarse fuera de la arquitectura definida.

---

## 2. Reglas de seguridad

- Todo endpoint debe tener permisos explícitos.
- Ningún usuario debe acceder a datos fuera de su alcance.
- No se guardan secretos en el repositorio.
- No se hardcodean tokens, claves ni credenciales.
- Toda exportación sensible debe ser auditable.
- Los errores no deben exponer stack traces en producción.
- Toda autenticación debe validarse mediante JWT.
- Las contraseñas deben almacenarse únicamente mediante hashing seguro.
- Ninguna información sensible debe enviarse al frontend sin necesidad funcional.

---

## 3. Reglas de frontend

- Usar componentes reutilizables.
- No duplicar lógica de negocio.
- No hardcodear estados si vienen del backend.
- No mezclar estilos sin convención.
- Mantener diseño responsive.
- Manejar loading, empty y error states.
- Usar Lucide React como sistema de íconos.
- No crear pantallas que no estén conectadas al flujo real.
- Todo listado debe contemplar estados vacíos.
- Toda acción relevante debe brindar feedback visual al usuario.
- La experiencia de usuario debe priorizar simplicidad y rapidez.

---

## 4. Reglas de backend

- Toda mutación compleja debe pasar por un service.
- Toda creación relevante debe tener tests.
- Toda entidad sensible debe ser auditable.
- Toda transición de estado debe validarse en backend.
- No usar `count() + 1` para códigos críticos.
- No hacer queries globales innecesarias.
- No retornar más campos de los necesarios.
- Toda integración externa debe estar encapsulada en servicios específicos.
- Toda lógica de recomendaciones debe ejecutarse exclusivamente en backend.
- Toda validación crítica debe ejecutarse en backend.

---

## 5. Reglas de base de datos

- PostgreSQL es la única fuente oficial de datos.
- Toda entidad principal debe incluir:
  - `created_at`
  - `updated_at`
- Las relaciones deben definirse explícitamente.
- No se permite duplicación innecesaria de datos.
- Toda migración debe ser reproducible.
- Los borrados físicos deben evitarse cuando sea posible.
- Priorizar eliminación lógica (`soft delete`) para entidades relevantes.

---

## 6. Reglas de API

- Usar nombres consistentes.
- Responder errores con formato estándar.
- Paginar listados grandes.
- Soportar filtros explícitos.
- Documentar endpoints.
- No crear endpoints duplicados.
- Versionar cambios incompatibles.
- Mantener respuestas predecibles y consistentes.
- Utilizar HTTP Status Codes correctos.
- Toda API debe devolver estructuras uniformes.

### Formato estándar de respuesta

```json
{
  "success": true,
  "data": {}
}
```

### Formato estándar de error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Descripción del error"
  }
}
```

---

## 7. Reglas del motor de recomendaciones

- Todas las recomendaciones deben calcularse en backend.
- El clima debe influir en el score de recomendación.
- La distancia debe influir en el score de recomendación.
- Los intereses del usuario deben influir en el score de recomendación.
- El presupuesto debe influir en el score de recomendación.
- El horario debe influir en el score de recomendación.
- El sistema debe permitir agregar nuevos factores de recomendación sin modificar la arquitectura existente.
- Ninguna recomendación debe depender exclusivamente de una única variable.
- El algoritmo debe ser desacoplado y extensible.

---

## 8. Reglas de integraciones externas

- Todas las APIs externas deben tener manejo de errores.
- Las respuestas externas deben validarse antes de persistirse.
- Las APIs externas deben estar desacopladas mediante servicios.
- Implementar cache cuando reduzca llamadas innecesarias.
- El fallo de una API externa no debe derribar el sistema completo.
- Toda integración nueva debe documentarse en `ARCHITECTURE.md`.
- Ninguna API externa debe ser consumida directamente desde el frontend.

---

## 9. Reglas de testing

- Toda funcionalidad crítica debe poseer tests.
- Todo service debe tener pruebas unitarias.
- Los endpoints principales deben tener pruebas de integración.
- Los flujos principales del usuario deben poseer pruebas E2E.
- No se considera terminada una funcionalidad sin criterios de aceptación verificables.
- Todo bug corregido debe incluir un test que prevenga regresiones futuras.

---

## 10. Reglas de IA / agentes

- Ningún agente improvisa arquitectura.
- Ningún agente modifica archivos fuera de su scope sin permiso del Orchestrator.
- Ningún agente elimina código sin explicar impacto.
- Todo cambio debe informar archivos modificados.
- Todo cambio debe tener criterios de aceptación.
- Si falta información, el agente debe preguntar o marcar supuesto.
- No se programan features durante Sprint 0.
- Ningún agente puede modificar tecnologías definidas en `STACK.md`.
- Ningún agente puede modificar reglas definidas en `RULES.md` sin aprobación explícita.

---

## 11. Reglas de documentación

- Todo módulo nuevo debe quedar documentado.
- Toda decisión importante debe registrarse como ADR.
- Toda regla de negocio nueva debe agregarse a `PROJECT_CONTEXT.md` o `WORKFLOW.md`.
- Toda modificación de estructura debe reflejarse en `FOLDER_STRUCTURE.md`.
- Toda nueva integración debe documentarse en `ARCHITECTURE.md`.
- La documentación debe mantenerse sincronizada con el código.
- Ningún cambio importante debe implementarse sin actualizar la documentación correspondiente.

---

## 12. Regla de oro

> Si un cambio puede romper arquitectura, seguridad, permisos, workflow, recomendaciones o datos, debe ser revisado por el Orchestrator antes de implementarse.