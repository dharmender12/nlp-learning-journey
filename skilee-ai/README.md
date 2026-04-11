# Skilee-AI

AI-Powered Platform for Skilled Trainers and Contractors.

## What You Get
- Full-stack SaaS app (FastAPI + React)
- JWT auth with role-based access (`contractor`, `trainer`, `admin`)
- Contract posting and trainer applications with CV upload/reupload
- AI-based CV relevance scoring and premium shortlist logic
- Subscription tiers (`free`, `standard`, `premium`)
- Admin analytics dashboard with charts
- Alembic migrations + seed script
- Dockerized backend/frontend
- GitHub Actions CI + deploy workflow templates

## Architecture
1. Browser -> React (Vite, Tailwind)
2. React -> FastAPI API
3. FastAPI -> Supabase Postgres
4. FastAPI -> Supabase Storage (`trainer-cvs` bucket)

## Repository Layout
- `backend/` FastAPI service
- `frontend/` React app
- `docker-compose.yml` local container orchestration
- `.github/workflows/` CI/CD templates

## Backend Setup (Local)
1. `cd backend`
2. `python3 -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.example .env` and fill values
5. Run migration: `alembic upgrade head`
6. Optional seed data: `python3 scripts/seed.py`
7. Start API: `uvicorn app.main:app --reload --host 0.0.0.0 --port 10000`

## Frontend Setup (Local)
1. `cd frontend`
2. `npm install`
3. `cp .env.example .env`
4. Set `VITE_API_URL=http://localhost:10000`
5. `npm run dev`

## Docker Run
1. Create `backend/.env` from `backend/.env.example`
2. Run: `docker compose up --build`
3. Frontend: `http://localhost:4173`
4. Backend: `http://localhost:10000`

## Required Environment Variables
### Backend (`backend/.env`)
- `DATABASE_URL`
- `JWT_SECRET`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY` (or `SUPABASE_KEY`)
- `FRONTEND_URL`

### Frontend (`frontend/.env`)
- `VITE_API_URL`
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

## Supabase Configuration
1. Create a free Supabase project.
2. Use Postgres connection string in `DATABASE_URL`.
3. Create public bucket `trainer-cvs`.
4. Put service role key in `SUPABASE_SERVICE_KEY`.
5. Run `alembic upgrade head`.

## API Endpoints
### Auth
- `POST /auth/register`
- `POST /auth/login`

### Contracts
- `POST /contracts`
- `GET /contracts`
- `GET /contracts/{id}/applications`

### Applications
- `POST /contracts/{id}/apply`
- `PUT /applications/{id}/cv`
- `GET /applications/me`

### User/Admin
- `POST /users/subscription`
- `GET /users/me/subscription`
- `GET /users/admin/stats`
- `GET /users/me`

## Tier Visibility Logic
- `free`: only applicant count
- `standard` (₹199): all applicants
- `premium` (₹249): AI shortlist (`2 * required_trainers`)

## Deploy (Free)
### Backend on Render
- Service root: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 10000`
- Set env vars from `backend/.env.example`

### Frontend on Cloudflare Pages
- Project root: `frontend`
- Build command: `npm run build`
- Output: `dist`
- Set `VITE_API_URL` to Render backend URL
- Free domain: `https://<project>.pages.dev`

## GitHub Actions
- `backend-ci.yml`: Python compile + pytest
- `frontend-ci.yml`: frontend build
- `deploy-backend-render.yml`: triggers Render deploy hook
- `deploy-frontend-cloudflare.yml`: deploys build to Cloudflare Pages

Add these GitHub secrets:
- `RENDER_DEPLOY_HOOK_URL`
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_PROJECT_NAME`
- `VITE_API_URL`

## Seed Accounts
After `python3 scripts/seed.py`:
- `admin@skilee.ai / password123`
- `contractor@skilee.ai / password123`
- `trainer@skilee.ai / password123`
