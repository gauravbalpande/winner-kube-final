# ============================================================
# Backend main.py — FastAPI with OpenTelemetry Instrumentation
# ============================================================
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, bets, payment
from core.config import settings

# ============================================================
# OpenTelemetry Setup
# Must be initialised BEFORE importing application code
# ============================================================
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Configure OTel resource (service name shows up in Jaeger/Grafana)
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger-collector:4317")
SERVICE_NAME  = os.getenv("OTEL_SERVICE_NAME", "betmasterx-backend")

resource = Resource.create({"service.name": SERVICE_NAME})

tracer_provider = TracerProvider(resource=resource)

# Export spans via gRPC to Jaeger / OTel Collector
otlp_exporter = OTLPSpanExporter(endpoint=OTEL_ENDPOINT, insecure=True)
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(tracer_provider)

# Auto-instrument logging so trace IDs appear in log lines
LoggingInstrumentor().instrument(set_logging_format=True)

# Auto-instrument outgoing httpx calls (Supabase client uses httpx)
HTTPXClientInstrumentor().instrument()

# ============================================================
# Configure structured logging
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ============================================================
# FastAPI Application
# ============================================================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
API_PREFIX  = "/api"

app = FastAPI(
    title="BetMasterX API",
    description="Production-grade betting platform API",
    version="1.0.0",
)

# ============================================================
# CORS Middleware — MUST be registered before routes
# ============================================================
ALLOWED_ORIGINS = settings.ALLOWED_ORIGINS if ENVIRONMENT == "production" else [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# ============================================================
# Include Routers
# ============================================================
app.include_router(auth.router,    prefix=f"{API_PREFIX}/auth",    tags=["Authentication"])
app.include_router(users.router,   prefix=f"{API_PREFIX}/user",    tags=["Users"])
app.include_router(bets.router,    prefix=f"{API_PREFIX}/bets",    tags=["Betting"])
app.include_router(payment.router, prefix=f"{API_PREFIX}/payment", tags=["Payment"])

# ============================================================
# Auto-instrument FastAPI AFTER routes are registered
# ============================================================
FastAPIInstrumentor.instrument_app(app)


@app.get("/")
async def root():
    return {
        "message":    "Welcome to BetMasterX API",
        "version":    "1.0.0",
        "status":     "operational",
        "environment": ENVIRONMENT,
        "api_prefix": API_PREFIX,
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": ENVIRONMENT}


# OPTIONS pre-flight handlers
@app.options(f"{API_PREFIX}/auth/register")
@app.options(f"{API_PREFIX}/auth/login")
async def options_handler():
    return {"status": "ok"}