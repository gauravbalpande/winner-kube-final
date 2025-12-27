# Troubleshooting Guide

## Common Issues and Solutions

### 1. "Name or service not known" Error

**Error:**
```
Authentication error: [Errno -2] Name or service not known
```

**Cause:** The backend cannot resolve the Supabase hostname. This usually means:
- The `SUPABASE_URL` in `.env` is incorrect or missing
- The `.env` file is not being loaded properly
- Network/DNS issue in Docker container

**Solution:**

1. **Verify `.env` file exists and has correct format:**
   ```bash
   cd backend
   cat .env
   ```

2. **Check the `.env` file format:**
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-key-here
   SUPABASE_SERVICE_KEY=your-service-role-key-here
   SECRET_KEY=your-secret-key-here
   ENVIRONMENT=development
   ```

3. **Important:** Make sure:
   - No quotes around values (unless they're part of the value)
   - No spaces around `=`
   - URL starts with `https://`
   - No trailing slashes in URL

4. **Test Supabase connection from container:**
   ```bash
   docker-compose exec backend python -c "
   from core.config import settings
   print('Supabase URL:', settings.SUPABASE_URL[:30] if settings.SUPABASE_URL else 'NOT SET')
   "
   ```

5. **Restart containers:**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### 2. Frontend Not Loading on localhost:5173

**Symptoms:**
- Browser shows connection refused
- Port 5173 not accessible

**Solution:**

1. **Check if port is in use:**
   ```bash
   lsof -i :5173
   # Kill process if needed
   kill -9 <PID>
   ```

2. **Verify docker-compose.yml uses development target:**
   ```yaml
   frontend:
     build:
       target: development  # NOT production
   ```

3. **Rebuild frontend:**
   ```bash
   docker-compose build --no-cache frontend
   docker-compose up frontend
   ```

4. **Check frontend logs:**
   ```bash
   docker-compose logs frontend
   ```

### 3. CORS Errors

**Symptoms:**
- Browser console shows CORS errors
- API calls fail with CORS policy

**Solution:**

1. **Verify backend CORS configuration** in `backend/main.py`:
   - Should include `http://localhost:5173`
   - Should allow credentials

2. **Check frontend is using proxy:**
   - Frontend should call `/api/...` (not `http://localhost:8000/...`)
   - Vite proxy should be configured in `vite.config.js`

3. **Verify environment variables:**
   ```bash
   docker-compose exec frontend env | grep VITE
   ```

### 4. Backend Not Starting

**Symptoms:**
- Backend container exits immediately
- Health check fails

**Solution:**

1. **Check backend logs:**
   ```bash
   docker-compose logs backend
   ```

2. **Verify .env file:**
   ```bash
   docker-compose exec backend env | grep SUPABASE
   ```

3. **Test backend health:**
   ```bash
   curl http://localhost:8000/health
   ```

4. **Check if Supabase credentials are correct:**
   - Go to Supabase Dashboard
   - Settings → API
   - Verify URL and keys match `.env` file

### 5. Database Connection Issues

**Symptoms:**
- "Connection refused" errors
- "Authentication failed" errors

**Solution:**

1. **Verify Supabase project is active:**
   - Check Supabase Dashboard
   - Ensure project is not paused

2. **Check network connectivity:**
   ```bash
   docker-compose exec backend curl -I https://your-project.supabase.co
   ```

3. **Verify database migrations:**
   - Run `db/migrations/001_initial_schema.sql` in Supabase SQL Editor

### 6. Environment Variables Not Loading

**Symptoms:**
- Settings show default values
- Supabase connection fails

**Solution:**

1. **Check .env file location:**
   - Should be in `backend/.env` (not root directory)

2. **Verify docker-compose.yml:**
   ```yaml
   backend:
     env_file:
       - ./backend/.env
   ```

3. **Test environment loading:**
   ```bash
   docker-compose exec backend python -c "
   from core.config import settings
   print('SUPABASE_URL set:', bool(settings.SUPABASE_URL))
   "
   ```

### 7. Hot Reload Not Working

**Symptoms:**
- Changes not reflected in browser
- Need to restart containers

**Solution:**

1. **Verify volumes are mounted:**
   ```yaml
   volumes:
     - ./backend:/app
     - ./frontend:/app
   ```

2. **Check file permissions:**
   ```bash
   ls -la backend/ frontend/
   ```

3. **Restart with rebuild:**
   ```bash
   docker-compose up --build
   ```

## Quick Diagnostic Commands

```bash
# Check all containers status
docker-compose ps

# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Test backend health
curl http://localhost:8000/health

# Test frontend
curl http://localhost:5173

# Check environment variables in container
docker-compose exec backend env | grep SUPABASE
docker-compose exec frontend env | grep VITE

# Restart everything
docker-compose down
docker-compose up --build
```

## Still Having Issues?

1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Verify network connectivity:**
   ```bash
   docker-compose exec backend ping -c 3 8.8.8.8
   ```

3. **Check Docker logs:**
   ```bash
   docker-compose logs --tail=100
   ```

4. **Rebuild from scratch:**
   ```bash
   docker-compose down -v
   docker-compose build --no-cache
   docker-compose up
   ```


