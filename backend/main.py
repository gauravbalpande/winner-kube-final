# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from routers import auth, users, bets, payment
# from core.config import settings

# app = FastAPI(
#     title="BetMasterX API",
#     description="Production-grade betting platform API",
#     version="1.0.0"
# )

# # CORS Configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include Routers
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(users.router, prefix="/user", tags=["Users"])
# app.include_router(bets.router, prefix="/bets", tags=["Betting"])
# app.include_router(payment.router, prefix="/payment", tags=["Payment"])

# @app.get("/")
# async def root():
#     return {
#         "message": "Welcome to BetMasterX API",
#         "version": "1.0.0",
#         "status": "operational"
#     }

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}

# ===================================================================
# FILE: backend/main.py (FIXED CORS)
# ===================================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, bets, payment
from core.config import settings

# ALB forwards /api/* to this service; we expose routes under /api.
API_PREFIX = "/api"

app = FastAPI(
    title="BetMasterX API",
    description="Production-grade betting platform API",
    version="1.0.0"
)

# CORS Configuration - MUST BE BEFORE ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"  # Allow all origins for development (remove in production)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include Routers - AFTER CORS MIDDLEWARE
app.include_router(auth.router, prefix=f"{API_PREFIX}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{API_PREFIX}/user", tags=["Users"])
app.include_router(bets.router, prefix=f"{API_PREFIX}/bets", tags=["Betting"])
app.include_router(payment.router, prefix=f"{API_PREFIX}/payment", tags=["Payment"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to BetMasterX API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get(f"{API_PREFIX}/health")
async def health_check():
    return {"status": "healthy", "cors": "enabled"}

# Additional OPTIONS handlers for debugging
@app.options("/auth/register")
@app.options("/auth/login")
async def options_handler():
    return {"status": "ok"}