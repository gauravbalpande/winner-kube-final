# Development Guide

This guide explains how to run BetMasterX in development mode using Docker Compose.

## Prerequisites

- Docker and Docker Compose installed
- Supabase account (or local PostgreSQL)

## Quick Start

### 1. Set Up Backend Environment

```bash
cd backend
cp .env.example .env
# Edit .env with your Supabase credentials
```

Required environment variables:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_KEY`
- `SECRET_KEY`
- `ENVIRONMENT=development`

### 2. Start Services

```bash
# From project root
docker-compose up
```

Or in detached mode:
```bash
docker-compose up -d
```

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## How It Works

### Development Mode Configuration

**Backend:**
- Runs without `/api` prefix (direct access)
- Health check at: `http://localhost:8000/health`
- API endpoints: `http://localhost:8000/auth/login`, etc.

**Frontend:**
- Vite dev server with hot reload
- Proxy configuration: `/api/*` → `http://localhost:8000/*` (strips `/api`)
- Frontend calls: `/api/auth/login` → proxied to → `http://localhost:8000/auth/login`

### Network Flow

```
Browser → http://localhost:5173/api/auth/login
    ↓
Vite Dev Server (proxy)
    ↓
http://localhost:8000/auth/login
    ↓
Backend FastAPI
```

## Environment Variables

### Backend (.env)

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
SECRET_KEY=your-secret-key
ENVIRONMENT=development
```

### Frontend (docker-compose.yml)

- `VITE_API_URL=/api` - Frontend uses relative path `/api`
- `DOCKER_ENV=true` - Tells Vite to use Docker networking

## Differences from Production

| Aspect | Development | Production |
|--------|-------------|------------|
| Backend API Prefix | None (`/auth/login`) | `/api` (`/api/auth/login`) |
| Frontend | Vite dev server | Nginx static files |
| API URL | Relative `/api` (proxied) | Relative `/api` (ALB routed) |
| Hot Reload | ✅ Enabled | ❌ Disabled |
| Health Check | `/health` | `/api/health` |

## Troubleshooting

### Backend not starting

```bash
# Check logs
docker-compose logs backend

# Verify .env file exists
ls backend/.env

# Check Supabase connection
docker-compose exec backend curl http://localhost:8000/health
```

### Frontend not connecting to backend

1. Check backend is running: `docker-compose ps`
2. Verify proxy in browser dev tools (Network tab)
3. Check Vite proxy config in `vite.config.js`

### CORS errors

Backend CORS is configured to allow:
- `http://localhost:5173`
- `http://localhost:3000`
- All origins (`*`) in development

If you see CORS errors, check:
- Backend is running on port 8000
- Frontend is using the proxy (`/api` path)
- Browser console for specific error

## Stopping Services

```bash
# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Rebuilding After Changes

```bash
# Rebuild and restart
docker-compose up --build

# Rebuild specific service
docker-compose build backend
docker-compose up backend
```

## Database Setup

1. Run migrations in Supabase Dashboard
2. Or use psql to connect and run `db/migrations/001_initial_schema.sql`

## Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### Test Frontend

1. Open http://localhost:5173
2. Try registering a new user
3. Try logging in
4. Check browser console for errors

## Production vs Development

The application automatically detects the environment:

- **Development** (`ENVIRONMENT=development`):
  - Backend serves routes without `/api` prefix
  - Frontend uses Vite dev server with proxy
  - Hot reload enabled

- **Production** (`ENVIRONMENT=production`):
  - Backend serves routes with `/api` prefix
  - Frontend uses Nginx to serve static files
  - ALB routes `/api/*` to backend

This allows the same codebase to work in both environments!


