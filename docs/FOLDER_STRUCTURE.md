# FOLDER_STRUCTURE.md

# Estructura de Carpetas IA-Ready

## 1. Principio

La estructura de carpetas define responsabilidades.

Los agentes IA no deben mezclar dominios ni escribir código en cualquier lugar.

Cada módulo debe representar un dominio real del negocio.

---

## 2. Estructura oficial de Planify

```txt
project/
├── agents/
│   ├── ORCHESTRATOR.md
│   ├── BACKEND_AGENT.md
│   ├── FRONTEND_AGENT.md
│   ├── DEVOPS_AGENT.md
│   ├── SECURITY_AGENT.md
│   └── QA_AGENT.md
│
├── docs/
│   ├── PROJECT_CONTEXT.md
│   ├── ARCHITECTURE.md
│   ├── STACK.md
│   ├── RULES.md
│   ├── FOLDER_STRUCTURE.md
│   ├── WORKFLOW.md
│   ├── RBAC.md
│   ├── API_GUIDELINES.md
│   └── SPRINT_0.md
│
├── backend/
│   ├── apps/
│   │   ├── users/
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── permissions.py
│   │   │   ├── selectors.py
│   │   │   ├── urls.py
│   │   │   └── tests/
│   │   │
│   │   ├── places/
│   │   ├── events/
│   │   ├── activities/
│   │   ├── recommendations/
│   │   ├── favorites/
│   │   ├── promotions/
│   │   ├── notifications/
│   │   ├── weather/
│   │   ├── integrations/
│   │   └── audit/
│   │
│   ├── config/
│   │   ├── settings/
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── profile/
│   │   │   ├── recommendations/
│   │   │   ├── events/
│   │   │   ├── places/
│   │   │   ├── favorites/
│   │   │   ├── promotions/
│   │   │   └── map/
│   │   │
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── store/
│   │   └── types/
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── docker/
│   ├── nginx/
│   └── scripts/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 3. Responsabilidades por carpeta

| Carpeta | Responsabilidad | Agente principal |
|----------|----------|----------|
| `agents/` | Instrucciones operativas para agentes IA | Orchestrator |
| `docs/` | Documentación oficial del proyecto | Orchestrator |
| `backend/` | API, reglas de negocio y persistencia | Backend Agent |
| `frontend/` | Interfaz de usuario y experiencia | Frontend Agent |
| `docker/` | Infraestructura y despliegue | DevOps Agent |
| `.github/` | Automatizaciones CI/CD | DevOps Agent |
| `checklists/` | Control de calidad | QA Agent |

---

## 4. Dominios del Backend

### users

Responsable de:

- usuarios
- autenticación
- perfiles
- preferencias

### places

Responsable de:

- lugares
- bares
- restaurantes
- cafeterías
- puntos de interés

### events

Responsable de:

- eventos
- festivales
- recitales
- actividades programadas

### activities

Responsable de:

- actividades sugeridas
- categorización
- restricciones

### recommendations

Responsable de:

- motor de recomendaciones
- scoring
- personalización
- ranking

### favorites

Responsable de:

- favoritos del usuario
- historial de guardados

### promotions

Responsable de:

- descuentos
- beneficios
- promociones

### notifications

Responsable de:

- recordatorios
- alertas
- notificaciones futuras

### weather

Responsable de:

- clima actual
- pronóstico
- adaptación de recomendaciones

### integrations

Responsable de:

- Google Maps
- Google Places
- OpenWeather
- Ticketmaster
- OAuth

### audit

Responsable de:

- auditoría
- logs funcionales
- trazabilidad

---

## 5. Reglas de separación

- `frontend/` no contiene lógica de negocio crítica.
- `services.py` contiene reglas de negocio.
- `selectors.py` contiene consultas complejas de lectura.
- `permissions.py` contiene permisos específicos.
- `integrations/` centraliza llamadas a APIs externas.
- `recommendations/` centraliza todo el motor de recomendación.
- `frontend/features/` agrupa funcionalidades por dominio.
- `frontend/components/` contiene únicamente componentes reutilizables.
- Ningún módulo debe depender directamente de otro módulo sin pasar por services.

---

## 6. Convenciones de organización

- Un dominio = una responsabilidad principal.
- Los nombres de carpetas deben estar en inglés.
- Los nombres deben ser descriptivos.
- Evitar carpetas genéricas como:
  - misc
  - temp
  - random
  - helpers gigantes

---

## 7. Prohibiciones

- No crear `utils.py` gigante con lógica mezclada.
- No crear `components/misc`.
- No crear endpoints fuera del módulo correspondiente.
- No mezclar lógica de dominios.
- No duplicar validaciones críticas entre frontend y backend.
- No consumir APIs externas directamente desde el frontend.
- No crear carpetas nuevas sin documentarlas aquí.
- No colocar lógica de recomendaciones fuera del módulo `recommendations`.

---

## 8. Regla de oro

> Si una funcionalidad nueva no tiene una ubicación clara dentro de esta estructura, primero debe actualizarse este documento antes de implementar código.