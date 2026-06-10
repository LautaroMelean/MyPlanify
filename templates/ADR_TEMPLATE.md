# ADR_TEMPLATE.md
# Architecture Decision Record

## ADR-[Número]: [Título de la decisión]

**Proyecto:** Planify  
**Fecha:** [YYYY-MM-DD]  
**Estado:** Propuesto / Aprobado / Rechazado / Reemplazado  
**Responsable:** [Orchestrator / Agente / Desarrollador]

---

## Contexto

Describir el problema arquitectónico o técnico que requiere una decisión formal.

Preguntas orientativas:

- ¿Qué situación motivó esta decisión?
- ¿Qué limitaciones existen?
- ¿Qué objetivos se buscan?
- ¿Qué documentos del proyecto impacta?

Documentos relacionados:

- PROJECT_CONTEXT.md
- ARCHITECTURE.md
- STACK.md
- RULES.md
- RBAC.md
- API_GUIDELINES.md
- DATA_MODEL.md

---

## Decisión

Describir claramente qué se decidió.

La decisión debe ser:

- específica;
- implementable;
- verificable;
- alineada con la arquitectura oficial.

---

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas |
|------------|----------|-------------|
| Alternativa A | | |
| Alternativa B | | |
| Alternativa C | | |

---

## Justificación

Explicar por qué la alternativa elegida es la más adecuada para Planify.

Considerar:

- escalabilidad;
- mantenibilidad;
- experiencia de usuario;
- costo de implementación;
- seguridad;
- complejidad operativa;
- compatibilidad con el stack oficial.

---

## Consecuencias

### Positivas

- [Consecuencia positiva]
- [Consecuencia positiva]
- [Consecuencia positiva]

### Negativas / Trade-offs

- [Consecuencia negativa]
- [Consecuencia negativa]

---

## Impacto en el sistema

### Backend

[Impacto]

### Frontend

[Impacto]

### Base de datos

[Impacto]

### DevOps

[Impacto]

### Seguridad

[Impacto]

### QA

[Impacto]

---

## Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|----------|------------|----------|------------|
| [Riesgo] | Baja / Media / Alta | Baja / Media / Alta | [Mitigación] |

---

## Cambios requeridos

### Archivos a modificar

- [Archivo]
- [Archivo]
- [Archivo]

### Nuevos componentes

- [Componente]
- [Servicio]
- [Tabla]
- [Endpoint]

---

## Compatibilidad

### Compatibilidad hacia atrás

- Sí / No

### ¿Requiere migración?

- Sí / No

### ¿Requiere versionado de API?

- Sí / No

### ¿Requiere actualización de documentación?

- Sí / No

---

## Documentación actualizada

Marcar documentos afectados:

- [ ] PROJECT_CONTEXT.md
- [ ] ARCHITECTURE.md
- [ ] STACK.md
- [ ] RULES.md
- [ ] FOLDER_STRUCTURE.md
- [ ] WORKFLOW.md
- [ ] RBAC.md
- [ ] API_GUIDELINES.md
- [ ] DATA_MODEL.md
- [ ] SPRINT_0.md

---

## Criterios de aceptación

- [ ] La decisión fue implementada.
- [ ] Los tests continúan pasando.
- [ ] No rompe arquitectura existente.
- [ ] La documentación fue actualizada.
- [ ] El Orchestrator aprobó la implementación.

---

## Revisión futura

Fecha sugerida:

[YYYY-MM-DD]

La decisión deberá revisarse si ocurre alguna de las siguientes situaciones:

- cambio significativo del negocio;
- problemas de rendimiento;
- problemas de escalabilidad;
- nueva tecnología que aporte ventajas claras;
- cambios importantes en la arquitectura de Planify.

---

## Estado final

**Resultado:**  
[Propuesto / Aprobado / Rechazado / Reemplazado]

**Aprobado por:**  
[Nombre]

**Fecha de aprobación:**  
[YYYY-MM-DD]