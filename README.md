# Planify

**Planify** is a web platform that recommends personalized activities, events, places, and plans in real time based on user location, current weather, schedule, budget, and personal preferences.

---

## Quick Start (Docker)

### 1. Copy environment file

```bash
cp .env.example .env
```

Edit `.env` and set a strong `SECRET_KEY` for production.

### 2. Start all services

```bash
docker compose up -d --build
```

Services started:
- **Backend** (Django) → http://localhost:8000
- **Frontend** (React) → http://localhost:5173
- **Nginx** (reverse proxy) → http://localhost:80
- **PostgreSQL** → localhost:5432
- **Redis** → localhost:6379

### 3. Check health

```bash
curl http://localhost:8000/api/v1/health/
```

---

## Local Development (without Docker)

### Backend

```bash
cd backend

# Create virtualenv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example ../.env
# Edit .env: set POSTGRES_HOST=localhost, REDIS_HOST=localhost

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start dev server
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Running tests

```bash
# Backend tests
cd backend
pytest

# Backend tests with coverage
pytest --cov=apps --cov-report=term

# Frontend tests
cd frontend
npm run test
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13, Django 5.2, Django REST Framework |
| Auth | JWT (access + refresh tokens) |
| Database | PostgreSQL 17 |
| Cache / Tasks | Redis + Celery |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS |
| State | TanStack Query + Zustand |
| Maps | Leaflet + react-leaflet |
| Notifications | Sonner toasts |
| Containers | Docker + Docker Compose |
| Proxy | Nginx |
| CI/CD | GitHub Actions |

---

## API

All endpoints are prefixed with `/api/v1/`.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register/` | Register new user |
| POST | `/api/v1/auth/login/` | Login |
| POST | `/api/v1/auth/logout/` | Logout (blacklists refresh token) |
| POST | `/api/v1/auth/refresh/` | Refresh access token |
| GET | `/api/v1/auth/me/` | Get current user |

### Public endpoints

| Endpoint | Description |
|---|---|
| `GET /api/v1/health/` | System healthcheck |
| `GET /api/v1/events/` | List published events (supports `?page`, `?category`, `?date_from`, `?free`) |
| `GET /api/v1/places/` | List active places (supports `?page`, `?lat`, `?lon`, `?radius_km`, `?open_now`) |
| `GET /api/v1/activities/` | List activities (supports `?page`, `?type`, `?indoor`, `?free`) |
| `GET /api/v1/promotions/` | List active promotions |
| `GET /api/v1/search/?q=` | Global search across places, activities and events |
| `GET /api/v1/trending/` | Trending places, activities and events (5-min cache) |
| `GET /api/v1/plans/trending/` | Trending public plans ranked by views + shares |
| `GET /api/v1/plans/public/<slug>/` | Public plan by slug |

### Response format

```json
{ "success": true, "data": {} }
```

```json
{ "success": false, "error": { "code": "...", "message": "..." } }
```

---

## Project Structure

```
Planify/
├── backend/           Django API
│   ├── apps/
│   │   ├── users/     Auth, profiles, preferences
│   │   ├── events/    Events + workflow
│   │   ├── places/    Places + OSM enrichment
│   │   ├── activities/Activities (manual + GCBA + OpenTripMap)
│   │   ├── favorites/ User favorites
│   │   ├── promotions/Business promotions
│   │   ├── notifications/ Notifications + reminders
│   │   ├── recommendations/ Recommendation engine V3
│   │   ├── reviews/   Reviews & ratings (entity_type generic)
│   │   ├── planner/   Smart Planner: generate, itinerary, clone, surprise
│   │   ├── dashboard/ Business, organizer, and user-activity dashboards
│   │   ├── integrations/ OpenWeather, OSM/Overpass, Nominatim, GCBA, OpenTripMap
│   │   ├── audit/     Audit logging
│   │   └── core/      Shared utilities + search + trending
│   └── config/        Django settings + URL router
├── frontend/          React application
│   └── src/
│       ├── components/ Reusable UI components
│       ├── features/  Feature modules
│       ├── hooks/     Custom hooks
│       ├── services/  API service layer
│       ├── store/     Zustand stores
│       └── types/     TypeScript types
├── docker/            Nginx config + scripts
├── .github/workflows/ CI/CD pipeline
├── docker-compose.yml
└── .env.example
```

---

## Sprint Status

| Sprint | Status | Description |
|---|---|---|
| Sprint 0 | ✅ `DONE` | Architecture, JWT auth, base structure, Docker |
| Sprint 1 | ✅ `DONE` | Events, places, activities, favorites, recommendations v1 |
| Sprint 2 | ✅ `DONE` | Recommendation Engine v1, UserPreferences, Reminders, RBAC |
| Sprint 3 | ✅ `DONE` | Full experience: promotions, advanced recs, detail pages, geo |
| Sprint 4 | ✅ `DONE` | Quality, testing (90+ Vitest, 5 Playwright), production Docker |
| Sprint 5 | ✅ `DONE` | External integrations: OpenWeather, OSM/Overpass, Rec Engine v2 |
| Sprint 6 | ✅ `DONE` | Reviews & Ratings, Global Search, Advanced Filters, Trending |
| Sprint 7 | ✅ `DONE` | Smart Planner: generate_plan, itinerary view, plan CRUD |
| Sprint 8 | ✅ `DONE` | Ownership, Business/Organizer Dashboards, Rec Engine v3, Plan Feedback |
| Sprint 9 | ✅ `DONE` | Discovery: trending plans, clone plan, Sorprendeme, calendar export |
| Sprint 10 | ✅ `DONE` | Rich places data (opening_hours, cuisine, fee, wifi), weather forecast |
| Sprint 11 | ✅ `DONE` | GCBA Open Data, OpenTripMap enrichment, smart Sorprendeme (3-phase) |
| Sprint 12 | ✅ `DONE` | UI polish: spinners, date formatting, card hover, EmptyState, Navbar |
| Sprint 13–15 | ✅ `DONE` | UX audit: score badges, search page, address in cards, PREF_TYPE_MAP, activity distance |
| Sprint 16 | ✅ `DONE` | Neon Glowmorph aesthetic: dark glass UI, neon shadows, glassmorphism |
| A11y audit | ✅ `DONE` | aria-hidden, focus-visible, role=alert, optimistic favorites, sonner toasts |
| Paginación + Mapa | ✅ `DONE` | Server-side pagination (30/page), BoundsWatcher en MapPage, code splitting |
| UX polish | ✅ `DONE` | Errores en español, aria-label dinámico, Escape en dropdowns, caps de input |

---

## Documentation

All project documentation lives in `docs/`:

- `ARCHITECTURE.md` — System architecture
- `DATA_MODEL.md` — Database entities
- `API_GUIDELINES.md` — API design standards
- `RBAC.md` — Roles and permissions
- `RULES.md` — Project constitution
- `WORKFLOW.md` — State machines and flows
- `adr/` — Architecture Decision Records (ADR-001 through ADR-020)
