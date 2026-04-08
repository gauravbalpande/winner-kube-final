#!/usr/bin/env bash
# ============================================================
# argocd/install/install.sh
# One-command ArgoCD installation on EKS
#
# Prerequisites:
#   - kubectl configured for target EKS cluster
#   - helm >= 3.14
#   - argocd CLI (optional, for initial login)
# ============================================================

set -euo pipefail

ARGOCD_NS="argocd"
ARGOCD_VERSION="6.7.0"   # Helm chart version (maps to app v2.10.0)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log()  { echo -e "\033[1;32m[INFO]\033[0m  $*"; }
warn() { echo -e "\033[1;33m[WARN]\033[0m  $*"; }
err()  { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; exit 1; }

# ============================================================
# Step 1: Create namespace
# ============================================================
log "Creating namespace: ${ARGOCD_NS}"
kubectl create namespace "${ARGOCD_NS}" --dry-run=client -o yaml | kubectl apply -f -

# ============================================================
# Step 2: Add Argo Helm repo
# ============================================================
log "Adding Argo Helm repository..."
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
log "Helm repos updated"

# ============================================================
# Step 3: Install ArgoCD via Helm
# ============================================================
log "Installing ArgoCD v2.10 (chart ${ARGOCD_VERSION})..."
helm upgrade --install argocd argo/argo-cd \
  --version "${ARGOCD_VERSION}" \
  --namespace "${ARGOCD_NS}" \
  --values "${SCRIPT_DIR}/argocd-values.yaml" \
  --set configs.secret.argocdServerAdminPassword="${ARGOCD_ADMIN_PASSWORD_HASH:-\$2a\$10\$PLACEHOLDER}" \
  --wait \
  --timeout 10m
log "ArgoCD installed"

# ============================================================
# Step 4: Wait for all pods to be ready
# ============================================================
log "Waiting for ArgoCD pods..."
kubectl rollout status deployment/argocd-server          -n "${ARGOCD_NS}" --timeout=120s
kubectl rollout status deployment/argocd-repo-server     -n "${ARGOCD_NS}" --timeout=120s
kubectl rollout status deployment/argocd-applicationset-controller -n "${ARGOCD_NS}" --timeout=120s

# ============================================================
# Step 5: Apply the Root App-of-Apps
# ============================================================
log "Bootstrapping Root App-of-Apps..."
kubectl apply -f "${SCRIPT_DIR}/root-app.yaml" -n "${ARGOCD_NS}"
log "Root app applied — ArgoCD will now auto-sync all child Applications"

# ============================================================
# Step 6: Print access info
# ============================================================
log "=========================================================="
log "ArgoCD Installed & Bootstrapped!"
log ""
log "Port-forward to UI:"
log "  kubectl port-forward svc/argocd-server 8080:443 -n ${ARGOCD_NS}"
log "  Open: https://localhost:8080"
log "  Username: admin"
log "  Password: kubectl get secret argocd-initial-admin-secret -n ${ARGOCD_NS} -o jsonpath='{.data.password}' | base64 -d"
log ""
log "ArgoCD CLI login:"
log "  argocd login localhost:8080 --insecure"
log "  argocd app list"
log "=========================================================="
