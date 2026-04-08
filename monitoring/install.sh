#!/usr/bin/env bash
# ============================================================
# monitoring/install.sh — Install full observability stack
# Prerequisites: helm, kubectl configured against target cluster
# ============================================================

set -euo pipefail

MONITORING_NS="monitoring"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() { echo -e "\033[1;32m[INFO]\033[0m $*"; }
err() { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; exit 1; }

# ============================================================
# Step 1: Create monitoring namespace
# ============================================================
log "Creating namespace: ${MONITORING_NS}"
kubectl create namespace "${MONITORING_NS}" --dry-run=client -o yaml | kubectl apply -f -

# Label namespace for network policies
kubectl label namespace "${MONITORING_NS}" \
  kubernetes.io/metadata.name="${MONITORING_NS}" \
  --overwrite

# ============================================================
# Step 2: Add Helm repositories
# ============================================================
log "Adding Helm repositories..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana              https://grafana.github.io/helm-charts
helm repo update
log "Helm repos updated"

# ============================================================
# Step 3: Install Prometheus + Alertmanager (kube-prometheus-stack)
# ============================================================
log "Installing Prometheus (kube-prometheus-stack)..."
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace "${MONITORING_NS}" \
  --values "${SCRIPT_DIR}/prometheus-values.yaml" \
  --wait \
  --timeout 10m
log "Prometheus installed"

# ============================================================
# Step 4: Install Loki + Promtail (log aggregation)
# ============================================================
log "Installing Loki..."
helm upgrade --install loki grafana/loki \
  --namespace "${MONITORING_NS}" \
  --values "${SCRIPT_DIR}/loki-values.yaml" \
  --wait \
  --timeout 10m
log "Loki installed"

# ============================================================
# Step 5: Deploy Jaeger (distributed tracing)
# ============================================================
log "Deploying Jaeger all-in-one..."
kubectl apply -f "${SCRIPT_DIR}/jaeger.yaml"
kubectl rollout status deployment/jaeger -n "${MONITORING_NS}" --timeout=120s
log "Jaeger deployed"

# ============================================================
# Step 6: Install Grafana
# ============================================================
log "Installing Grafana..."
helm upgrade --install grafana grafana/grafana \
  --namespace "${MONITORING_NS}" \
  --values "${SCRIPT_DIR}/grafana-values.yaml" \
  --set adminPassword="${GRAFANA_ADMIN_PASSWORD:-admin}" \
  --wait \
  --timeout 5m
log "Grafana installed"

# ============================================================
# Step 7: Print access instructions
# ============================================================
log "=========================================="
log "Observability Stack Installed!"
log ""
log "Access Grafana (port-forward):"
log "  kubectl port-forward svc/grafana 3000:3000 -n ${MONITORING_NS}"
log "  Open: http://localhost:3000"
log "  User: admin / Password: set via GRAFANA_ADMIN_PASSWORD env var"
log ""
log "Access Prometheus:"
log "  kubectl port-forward svc/prometheus-operated 9090:9090 -n ${MONITORING_NS}"
log "  Open: http://localhost:9090"
log ""
log "Access Jaeger UI:"
log "  kubectl port-forward svc/jaeger-query 16686:16686 -n ${MONITORING_NS}"
log "  Open: http://localhost:16686"
log "=========================================="
