# 🚀 Quick Setup Guide for BetMasterX

## Prerequisites Checklist
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Docker & Docker Compose installed
- [ ] Supabase account created
- [ ] Git installed

## Step-by-Step Setup (5 minutes)

### 1️⃣ Supabase Setup (2 minutes)

1. Go to https://supabase.com and sign up
2. Click "New Project"
3. Fill in:
   - Name: `betmasterx`
   - Database Password: (save this!)
   - Region: Choose closest to you
4. Wait for project to initialize
5. Go to Settings → API
6. Copy these values:
   - Project URL
   - `anon` public key
   - `service_role` secret key

### 2️⃣ Database Setup (1 minute)

1. In Supabase Dashboard, go to SQL Editor
2. Click "New Query"
3. Copy entire content from `db/migrations/001_initial_schema.sql`
4. Click "Run"
5. Verify tables created: Go to Table Editor

### 3️⃣ Backend Configuration (1 minute)

```bash
cd backend
cp .env.example .env
nano .env  # or use any text editor
```

Update these lines:
```env
SUPABASE_URL=your-project-url-here
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here
SECRET_KEY=your-generated-secret-key  # Generate with: openssl rand -hex 32
```

### 4️⃣ Install Dependencies (1 minute)

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 5️⃣ Run the Application

**Option A: Docker (Easiest)**
```bash
docker-compose up
```

**Option B: Manual**
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 6️⃣ Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### 7️⃣ Test Login

Use demo account:
- Username: `demo_user`
- Password: `testpass123`

Or create a new account!

## 🎉 You're Done!

The application should now be running. If you encounter any issues, check the troubleshooting section in README.md.

## Common Issues

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Supabase Connection Error
- Verify your `.env` file has correct credentials
- Check if Supabase project is active
- Ensure you have internet connection

### Database Migration Failed
- Check SQL syntax in migration file
- Ensure you're using PostgreSQL 15+
- Verify Supabase project permissions

## Next Steps

1. ✅ Explore the Horse Race betting feature
2. ✅ Check out API documentation
3. ✅ Review the code structure
4. ✅ Customize the application
5. ✅ Deploy to production

Happy Betting! 🎰