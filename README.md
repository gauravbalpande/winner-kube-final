A complete 3-tier web application showcasing DevOps, MCP (Model Context Protocol), backend architecture, and cloud deployment skills.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend Layer                     │
│            React + Tailwind CSS + Lucide Icons          │
│              Authentication & Game Interface            │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Backend Layer (API)                  │
│                    FastAPI + Python                     │
│        ┌──────────────────────────────────────┐         │
│        │  Routers (Auth, Users, Bets, Pay)    │         │
│        └──────────────────────────────────────┘         │
│        ┌──────────────────────────────────────┐         │
│        │  Services (Business Logic)           │         │
│        └──────────────────────────────────────┘         │
│        ┌──────────────────────────────────────┐         │
│        │  MCP Client (Protocol Layer)         │         │
│        └──────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Database Layer                       │
│              Supabase (PostgreSQL)                      │
│    Tables: users, wallets, bets                         │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Features

### ✅ Implemented
- **User Authentication**
  - Registration with email validation
  - Login with JWT tokens
  - Secure password hashing (bcrypt)
  - Protected API routes

- **Horse Race Betting**
  - 4 horses to bet on
  - Dynamic bet amounts
  - Real-time balance updates
  - Win/loss tracking
  - 2x payout multiplier

- **Wallet Management**
  - Initial balance: $1000
  - Real-time balance display
  - Transaction history

### 🚧 Coming Soon
- Cricket Betting
- Football Betting
- Payment Gateway Integration (Stripe/Razorpay)

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Supabase account (or local PostgreSQL)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/betmasterx.git
cd betmasterx
```

### 2. Set Up Supabase

#### Option A: Cloud Supabase (Recommended)

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Project Settings → API
4. Copy your:
   - Project URL
   - `anon` public key
   - `service_role` key (keep secret!)

#### Option B: Local Supabase

```bash
# Install Supabase CLI
npm install -g supabase

# Initialize Supabase
supabase init

# Start local instance
supabase start
```

### 3. Configure Environment Variables

```bash
# Backend configuration
cd backend
cp .env.example .env

# Edit .env with your Supabase credentials
nano .env
```

Update these values in `.env`:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
SECRET_KEY=generate-a-secure-random-key-here
```

### 4. Run Database Migrations

#### Using Supabase Dashboard:
1. Go to SQL Editor in Supabase Dashboard
2. Copy content from `db/migrations/001_initial_schema.sql`
3. Run the migration

#### Using psql:
```bash
psql -h your-db-host -U postgres -d betmasterx -f db/migrations/001_initial_schema.sql
```

### 5. Install Dependencies

#### Backend:
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend:
```bash
cd frontend
npm install
```

## 🚀 Running the Application

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Terminal 1 - Backend:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## 🧪 Testing

### Test User Credentials
```
Username: demo_user
Password: testpass123
```

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Register new user
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

## 📁 Project Structure

```
betmasterx/
├── backend/
│   ├── main.py                 # FastAPI application entry
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Backend container config
│   ├── core/
│   │   ├── config.py          # Application settings
│   │   └── security.py        # JWT & password utilities
│   ├── models/
│   │   ├── user.py            # User data models
│   │   └── bet.py             # Bet data models
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── users.py           # User management endpoints
│   │   ├── bets.py            # Betting endpoints
│   │   └── payment.py         # Payment endpoints (placeholder)
│   ├── services/
│   │   ├── auth_service.py    # Authentication business logic
│   │   ├── user_service.py    # User business logic
│   │   └── bet_service.py     # Betting business logic
│   ├── supabase/
│   │   └── supabase_client.py # Supabase connection
│   └── mcp/
│       └── mcp_client.py      # MCP protocol implementation
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
├── k8s/                       # Kubernetes manifests
│   ├── namespace.yaml         # Namespace definition
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── ingress.yaml           # Ingress configuration
│   ├── secrets.yaml.template  # Secrets template
│   ├── kustomization.yaml     # Kustomize config
│   ├── deploy.sh              # Deployment script
│   └── README.md              # K8s deployment guide
├── terraform/                 # Infrastructure as Code
│   ├── main.tf                # Terraform configuration
│   └── ...
├── db/
│   └── migrations/
│       └── 001_initial_schema.sql  # Database schema
├── docker-compose.yml         # Multi-container orchestration
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔒 Security Best Practices

1. **Never commit `.env` files** - Always use `.env.example`
2. **Strong SECRET_KEY** - Generate with: `openssl rand -hex 32`
3. **Supabase RLS** - Enable Row Level Security policies
4. **HTTPS in Production** - Use SSL/TLS certificates
5. **Rate Limiting** - Implement API rate limits
6. **Input Validation** - All inputs validated with Pydantic

## 🧩 MCP Integration

This application uses MCP (Model Context Protocol) as an abstraction layer between the backend and database. Benefits:

- **Separation of Concerns**: Business logic separated from data access
- **Flexibility**: Easy to swap database providers
- **Testability**: Mock MCP for unit tests
- **Scalability**: Distribute MCP servers separately

### MCP Operations:
- `authenticate_user()` - User authentication
- `get_user_balance()` - Fetch wallet balance
- `update_balance()` - Update wallet balance
- `create_bet_record()` - Store bet transactions

## 🚀 Deployment

### Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create betmasterx-api

# Set environment variables
heroku config:set SUPABASE_URL=your-url
heroku config:set SUPABASE_KEY=your-key
heroku config:set SECRET_KEY=your-secret

# Deploy
git push heroku main
```

### AWS/GCP/Azure Deployment

1. Build Docker image
2. Push to container registry
3. Deploy to ECS/Cloud Run/App Service
4. Configure environment variables
5. Set up load balancer & SSL

### Kubernetes Deployment

The project includes complete Kubernetes manifests for deployment on any Kubernetes cluster (EKS, GKE, AKS, or local).

**Quick Start:**

```bash
cd k8s

# Create secrets from template
cp secrets.yaml.template secrets.yaml
# Edit secrets.yaml with your values

# Deploy using the script
./deploy.sh

# Or deploy manually
kubectl apply -f .
```

**Features:**
- ✅ Complete Kubernetes manifests (Deployments, Services, Ingress)
- ✅ Health checks and resource limits configured
- ✅ Secrets management with templates
- ✅ ECR registry secret support
- ✅ ALB Ingress Controller support (AWS EKS)
- ✅ Kustomization file for ArgoCD integration
- ✅ Ready for Prometheus & Grafana monitoring

**For detailed Kubernetes deployment instructions, see [k8s/README.md](k8s/README.md)**

**Future Integrations:**
- ⏳ ArgoCD for GitOps deployments
- ⏳ Prometheus for metrics collection
- ⏳ Grafana for visualization dashboards

## 📊 Database Schema

### Users Table
```sql
- id (UUID, PK)
- username (VARCHAR, UNIQUE)
- email (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- created_at (TIMESTAMP)
```

### Wallets Table
```sql
- id (UUID, PK)
- user_id (UUID, FK → users)
- balance (DECIMAL)
- created_at (TIMESTAMP)
```

### Bets Table
```sql
- id (UUID, PK)
- user_id (UUID, FK → users)
- horse_choice (INTEGER)
- bet_amount (DECIMAL)
- winning_horse (INTEGER)
- result (VARCHAR)
- winnings (DECIMAL)
- created_at (TIMESTAMP)
```

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend connection issues
```bash
# Check API URL in frontend config
# Ensure CORS is properly configured in backend
```

### Database connection errors
```bash
# Verify Supabase credentials
# Check network connectivity
# Ensure database migrations ran successfully
```

## 📝 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [yourprofile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Supabase for database infrastructure
- React & Tailwind CSS for frontend
- Lucide for beautiful icons

---

**Note**: This is a demonstration project for portfolio purposes. For production use, implement additional security measures, proper payment gateway integration, and comprehensive testing.

 <!-- pydantic==2.5.0
pydantic-settings==2.1.0 -->