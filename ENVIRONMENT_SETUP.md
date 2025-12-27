# Environment Setup Guide

BetMasterX supports both **Development** (Docker Compose) and **Production** (Terraform/ECS/K8s) deployments with automatic environment detection.

## How Environment Detection Works

### Backend (`backend/main.py`)

The backend automatically detects the environment using the `ENVIRONMENT` environment variable:

```python
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
API_PREFIX = "/api" if ENVIRONMENT == "production" else ""
```

**Development Mode** (`ENVIRONMENT=development`):
- Routes served at: `/auth/login`, `/user/balance`, etc.
- Health check: `/health`
- No API prefix needed

**Production Mode** (`ENVIRONMENT=production`):
- Routes served at: `/api/auth/login`, `/api/user/balance`, etc.
- Health check: `/api/health`
- Also available at `/health` for compatibility

### Frontend (`frontend/src/App.jsx`)

The frontend uses environment variables:

```javascript
const API_BASE = import.meta.env.VITE_API_URL || '/api';
```

**Development Mode**:
- `VITE_API_URL=/api` (set in docker-compose.yml)
- Vite proxy strips `/api` and forwards to `http://localhost:8000`
- Frontend calls: `/api/auth/login` → proxied to → `http://localhost:8000/auth/login`

**Production Mode**:
- `VITE_API_URL=/api` (set in .env.production)
- No proxy (static files served by nginx)
- Frontend calls: `/api/auth/login` → ALB routes to → backend at `/api/auth/login`

## Development Setup (Docker Compose)

### 1. Backend Configuration

Create `backend/.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
SECRET_KEY=your-secret-key
ENVIRONMENT=development
```

### 2. Start Services

```bash
docker-compose up
```

### 3. Access Points

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### How It Works

```
Browser → http://localhost:5173/api/auth/login
    ↓
Vite Dev Server (proxy in vite.config.js)
    ↓ (strips /api prefix)
http://localhost:8000/auth/login
    ↓
Backend FastAPI (no /api prefix in dev)
```

## Production Setup (Terraform/ECS)

### 1. Backend Configuration

In `terraform/main.tf`, backend task definition has:
```hcl
environment = [
  { name = "ENVIRONMENT", value = "production" },
  # ... other env vars
]
```

### 2. Frontend Configuration

Frontend uses `.env.production`:
```env
VITE_API_URL=/api
```

### 3. How It Works

```
Browser → https://your-alb.com/api/auth/login
    ↓
ALB (path-based routing)
    ↓ (/api/* → backend service)
Backend FastAPI (with /api prefix)
    ↓
/api/auth/login endpoint
```

## Key Differences

| Feature | Development | Production |
|---------|-------------|------------|
| **Backend API Prefix** | None | `/api` |
| **Frontend** | Vite dev server | Nginx static files |
| **Hot Reload** | ✅ Enabled | ❌ Disabled |
| **API Calls** | Proxied via Vite | Direct via ALB |
| **Health Check** | `/health` | `/api/health` (also `/health`) |
| **CORS** | Localhost origins | All origins (`*`) |

## Testing Both Environments

### Test Development

```bash
# Start development
docker-compose up

# Test backend directly
curl http://localhost:8000/health
curl http://localhost:8000/auth/login -X POST -d '{"username":"test","password":"test"}'

# Test via frontend proxy
curl http://localhost:5173/api/health
```

### Test Production

```bash
# Deploy with Terraform
cd terraform
terraform apply

# Get ALB URL
terraform output alb_dns_name

# Test
curl http://<alb-dns>/api/health
curl http://<alb-dns>/api/auth/login -X POST -d '{"username":"test","password":"test"}'
```

## Troubleshooting

### Development: Frontend can't reach backend

1. Check backend is running: `docker-compose ps`
2. Verify proxy in `vite.config.js`
3. Check browser console for CORS errors
4. Ensure `VITE_API_URL=/api` in docker-compose.yml

### Production: 404 errors on API calls

1. Verify `ENVIRONMENT=production` in backend task definition
2. Check ALB path routing: `/api/*` → backend
3. Verify backend routes have `/api` prefix
4. Check backend logs for route registration

### Both: CORS errors

Backend CORS allows:
- `http://localhost:5173` (development)
- `http://localhost:3000` (alternative dev port)
- `*` (all origins - for production ALB)

If you see CORS errors:
- Check backend CORS configuration in `main.py`
- Verify request origin matches allowed origins
- Check browser console for specific CORS error

## Migration Checklist

When moving from development to production:

- [ ] Set `ENVIRONMENT=production` in backend
- [ ] Verify backend routes use `/api` prefix
- [ ] Update frontend `.env.production` with `VITE_API_URL=/api`
- [ ] Rebuild frontend with production build
- [ ] Configure ALB path routing: `/api/*` → backend
- [ ] Update health checks to use `/api/health`
- [ ] Test all API endpoints through ALB

## Summary

The application automatically adapts to the environment:

- **Development**: Direct access, no prefixes, hot reload
- **Production**: ALB routing, `/api` prefix, optimized builds

Same codebase, different configurations! 🚀


