# ============================================================
# Backend Dockerfile — Multi-Stage, Non-Root, Production Ready
# ============================================================

# Stage 1: Builder — installs deps, compiles extensions
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build tools (only in builder stage)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install Python deps into a clean prefix (easier to copy)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================================
# Stage 2: Runtime — minimal image, no build tools
# ============================================================
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install only runtime system deps (curl for health check)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    # Create non-root user for security
    && groupadd -r appuser --gid 1001 \
    && useradd -r -g appuser --uid 1001 --no-create-home appuser

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Healthcheck — used by Docker Compose and Kubernetes probes
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command — no --reload flag
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]