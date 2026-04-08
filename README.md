<div align="center">

# 🏇 BetMasterX — Cloud-Native Betting Platform

[![CI/CD](https://github.com/your-org/winner-kube/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/your-org/winner-kube/actions/workflows/ci-cd.yml)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.29-326CE5?logo=kubernetes)](https://kubernetes.io)
[![Terraform](https://img.shields.io/badge/Terraform-1.6+-7B42BC?logo=terraform)](https://terraform.io)
[![Helm](https://img.shields.io/badge/Helm-3.14-0F1689?logo=helm)](https://helm.sh)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

**A production-grade, cloud-native horse-betting platform demonstrating modern DevOps practices on AWS EKS.**

</div>

---

## 📐 Architecture

```
                          ┌─────────────────────────────────────────────┐
                          │              AWS us-east-1                   │
                          │                                              │
  Users ──► Route 53 ──► │  ┌─────────────────────────────────────────┐ │
  (HTTPS)                 │  │       Application Load Balancer (ALB)  │ │
                          │  │   Port 443 → HTTPS (ACM Certificate)   │ │
                          │  └──────────────┬──────────────────────────┘ │
                          │                 │                            │
                          │    ┌────────────┼────────────┐              │
                          │    ▼            │            ▼              │
                          │  ┌──────────┐  │  ┌──────────────────────┐  │
                          │  │ Frontend │  │  │  Backend (FastAPI)   │  │
                          │  │ (Nginx)  │  │  │  /api/* routes       │  │
                          │  │ React SPA│  │  │  OTel instrumented   │  │
                          │  │ 2-6 pods │  │  │  2-8 pods (HPA)      │  │
                          │  └──────────┘  │  └──────────┬───────────┘  │
                          │                │             │               │
                          │  ┌─────────────────────────────────────┐    │
                          │  │         EKS Cluster (betmasterx ns) │    │
                          │  │   Private Subnets  ·  AL2023 Nodes  │    │
                          │  └─────────────────────────────────────┘    │
                          │                             │               │
                          │            ┌────────────────┘               │
                          │            ▼                                 │
                          │  ┌─────────────────────────────────────┐    │
                          │  │         monitoring namespace         │    │
                          │  │  Prometheus · Grafana · Loki · Jaeger│   │
                          │  └─────────────────────────────────────┘    │
                          │                                              │
                          └──────────────────────────────────────────────┘
                                         │ HTTPS
                                         ▼
                          ┌──────────────────────────┐
                          │  Supabase (PostgreSQL)   │
                          │  External SaaS · No EC2  │
                          └──────────────────────────┘
```

### Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + Tailwind CSS + Nginx |
| Backend | FastAPI (Python 3.11) + Uvicorn |
| Database | Supabase PostgreSQL (SaaS) |
| Container Registry | Amazon ECR |
| Orchestration | AWS EKS (Kubernetes 1.29) |
| Infrastructure as Code | Terraform 1.6+ |
| Package Manager | Helm 3.14 |
| Observability | Prometheus · Grafana · Loki · Jaeger (OTel) |
| CI/CD | GitHub Actions |
| Security | IRSA · Trivy · Network Policies · Non-root containers |

---

## 📁 Repository Structure

```
winner-kube/
├── backend/                    # FastAPI application
│   ├── Dockerfile              # Multi-stage, non-root user
│   ├── main.py                 # OTel-instrumented FastAPI app
│   ├── requirements.txt        # Includes OTel packages
│   ├── routers/                # auth, users, bets, payment
│   ├── services/               # Business logic
│   └── core/                   # Config + security
├── frontend/                   # React + Vite
│   ├── Dockerfile              # Multi-stage → nginx:1.27-alpine
│   ├── nginx.conf              # SPA routing + /api proxy
│   └── src/                    # React components
├── terraform/
│   ├── VPC-manifest/           # VPC, subnets, NAT GW (with EKS tags)
│   ├── EKS-cluster/            # EKS control plane + node group
│   └── ECR/                    # ECR repos + IRSA + ALB controller IAM
├── kubernetes/                 # Raw manifests (reference)
│   ├── namespace.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml.example
│   ├── serviceaccount.yaml
│   ├── hpa.yaml
│   └── network-policy.yaml
├── helm/betmasterx/            # Helm chart (deploy this)
│   ├── Chart.yaml
│   ├── values.yaml             # Base / dev defaults
│   ├── values-staging.yaml
│   ├── values-production.yaml
│   └── templates/
├── monitoring/                 # Observability stack
│   ├── install.sh              # One-command install
│   ├── prometheus-values.yaml
│   ├── grafana-values.yaml
│   ├── loki-values.yaml
│   └── jaeger.yaml
├── .github/workflows/
│   └── ci-cd.yml               # GitHub Actions pipeline
└── docker-compose.yml          # Local development
```

---

## 🚀 Quick Start — Local Development

```bash
# 1. Clone
git clone https://github.com/your-org/winner-kube.git
cd winner-kube

# 2. Copy and fill environment variables
cp .env.example .env.local
# Edit .env.local with your Supabase credentials

# 3. Start with Docker Compose
docker compose up --build

# Frontend: http://localhost:80
# Backend:  http://localhost:8000/docs (Swagger UI)
```

---

## 🏗️ Infrastructure Provisioning

### Prerequisites

```bash
brew install terraform awscli kubectl helm
# Configure AWS credentials
aws configure
```

### Step 1 — Create S3 Backend for Terraform State

```bash
# Create S3 bucket + DynamoDB table for state locking
aws s3 mb s3://aws-remote-tfstate --region us-east-1
aws dynamodb create-table \
    --table-name terraform-state-lock \
    --attribute-definitions AttributeName=LockID,AttributeType=S \
    --key-schema AttributeName=LockID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

### Step 2 — Provision VPC

```bash
cd terraform/VPC-manifest
terraform init
terraform plan
terraform apply -auto-approve
```

This creates: VPC, 3 public + 3 private subnets across AZs, Internet Gateway, NAT Gateway, route tables, and EKS subnet tags for ALB discovery.

### Step 3 — Provision ECR Repositories + IRSA

```bash
cd terraform/ECR
# Set your EKS cluster name and AWS account ID
terraform init
terraform plan \
  -var="aws_account_id=$(aws sts get-caller-identity --query Account --output text)"
terraform apply -auto-approve

# Note the outputs:
terraform output backend_repository_url
terraform output backend_irsa_role_arn
terraform output alb_controller_role_arn
```

### Step 4 — Provision EKS Cluster

```bash
cd terraform/EKS-cluster
terraform init
terraform plan
terraform apply -auto-approve   # ~15 minutes

# Configure kubectl
aws eks update-kubeconfig \
    --name retail-dev-eksdemo \
    --region us-east-1
kubectl get nodes
```

### Step 5 — Install AWS Load Balancer Controller

```bash
# Add EKS chart repo
helm repo add eks https://aws.github.io/eks-charts
helm repo update

# Install ALB controller (uses IRSA role from Step 3)
ALB_ROLE=$(cd terraform/ECR && terraform output -raw alb_controller_role_arn)

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=retail-dev-eksdemo \
  --set serviceAccount.create=true \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=${ALB_ROLE}
```

---

## 📦 Kubernetes Deployment (Raw Manifests)

```bash
ECR_BACKEND=$(cd terraform/ECR && terraform output -raw backend_repository_url)
ECR_FRONTEND=$(cd terraform/ECR && terraform output -raw frontend_repository_url)

# Push images to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin $ECR_BACKEND

docker build -t $ECR_BACKEND:latest ./backend && docker push $ECR_BACKEND:latest
docker build -t $ECR_FRONTEND:latest --target production ./frontend && docker push $ECR_FRONTEND:latest

# Update manifest image references
sed -i "s|ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/betmasterx-backend|$ECR_BACKEND|g" kubernetes/*.yaml
sed -i "s|ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/betmasterx-frontend|$ECR_FRONTEND|g" kubernetes/*.yaml

# Deploy
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/serviceaccount.yaml
kubectl apply -f kubernetes/configmap.yaml

# Create secret with real credentials (never commit to Git!)
kubectl create secret generic betmasterx-secrets \
  --namespace=betmasterx \
  --from-literal=SUPABASE_URL="your-url" \
  --from-literal=SUPABASE_KEY="your-key" \
  --from-literal=SUPABASE_SERVICE_KEY="your-service-key" \
  --from-literal=SECRET_KEY="your-jwt-secret"

kubectl apply -f kubernetes/

# Check status
kubectl get pods -n betmasterx
kubectl get ingress -n betmasterx
```

---

## ⛵ Helm Deployment (Recommended)

```bash
# Update image references in values.yaml or use --set

# Dev deployment
helm upgrade --install betmasterx ./helm/betmasterx \
  -f ./helm/betmasterx/values.yaml \
  --set backend.image.repository="$ECR_BACKEND" \
  --set frontend.image.repository="$ECR_FRONTEND" \
  --set secrets.supabaseUrl="$SUPABASE_URL" \
  --set secrets.supabaseKey="$SUPABASE_KEY" \
  --set secrets.supabaseServiceKey="$SUPABASE_SERVICE_KEY" \
  --set secrets.secretKey="$JWT_SECRET"

# Production deployment
helm upgrade --install betmasterx ./helm/betmasterx \
  -f ./helm/betmasterx/values.yaml \
  -f ./helm/betmasterx/values-production.yaml \
  --set backend.image.tag="v1.0.0" \
  --set frontend.image.tag="v1.0.0" \
  --set secrets.supabaseUrl="$SUPABASE_URL" \
  --set secrets.supabaseKey="$SUPABASE_KEY" \
  --set secrets.supabaseServiceKey="$SUPABASE_SERVICE_KEY" \
  --set secrets.secretKey="$JWT_SECRET" \
  --atomic --wait

# Check release
helm list -n betmasterx
```

---

## 📊 Observability Setup

```bash
# Install full monitoring stack (Prometheus + Grafana + Loki + Jaeger)
chmod +x monitoring/install.sh
GRAFANA_ADMIN_PASSWORD="your-password" ./monitoring/install.sh

# Port-forward to access UIs locally:
kubectl port-forward svc/grafana 3000:3000 -n monitoring &
kubectl port-forward svc/prometheus-operated 9090:9090 -n monitoring &
kubectl port-forward svc/jaeger-query 16686:16686 -n monitoring &
```

| Tool | Local URL | Purpose |
|---|---|---|
| Grafana | http://localhost:3000 | Dashboards (K8s, FastAPI, Nodes) |
| Prometheus | http://localhost:9090 | Metrics query + alerts |
| Jaeger | http://localhost:16686 | Distributed traces |
| Loki (via Grafana) | Grafana → Explore | Centralized logs |

### OpenTelemetry Flow

```
FastAPI request
     ↓
OTel FastAPIInstrumentor (auto-trace)
     ↓
TracerProvider → BatchSpanProcessor
     ↓
OTLPSpanExporter (gRPC:4317)
     ↓
Jaeger all-in-one (monitoring ns)
     ↓
Grafana (Jaeger datasource)
```

---

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline (`.github/workflows/ci-cd.yml`) runs on every push to `main`:

```
Push to main
    │
    ▼
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌─────────────────┐
│ lint-test   │───►│  security-scan   │───►│  build-push  │───►│     deploy      │
│             │    │                  │    │              │    │                 │
│ flake8      │    │ Trivy: images    │    │ ECR backend  │    │ Helm upgrade    │
│ ESLint      │    │ Trivy: IaC       │    │ ECR frontend │    │ --atomic        │
│ helm lint   │    │ CRITICAL→fail    │    │ SHA tag      │    │ EKS cluster     │
└─────────────┘    └──────────────────┘    └──────────────┘    └─────────────────┘
```

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user with ECR push + EKS access |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret |
| `AWS_ACCOUNT_ID` | 12-digit AWS account ID |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_KEY` | Supabase anon key |
| `SUPABASE_SERVICE_KEY` | Supabase service role key |
| `JWT_SECRET` | Strong random JWT signing secret |

---

## 🔐 Security

| Practice | Implementation |
|---|---|
| Non-root containers | Backend UID 1001, Frontend nginx:101 |
| IRSA | Backend SA annotated with IAM role ARN |
| Least-privilege IAM | ECR read-only + explicit S3/OTel only |
| Network policies | Default-deny + whitelist approach |
| Zero secret in Git | Secrets injected by CI/CD via `--set` |
| Image scanning | Trivy on every CI run (blocks CRITICAL/HIGH) |
| HTTPS only | ALB forces HTTP→HTTPS redirect (ACM cert) |
| Capabilities drop | `drop: ALL` + only required caps added |
| Pod security context | `runAsNonRoot: true`, `allowPrivilegeEscalation: false` |

---

## 🔧 Development Commands

```bash
# Validate Helm chart
helm lint ./helm/betmasterx -f ./helm/betmasterx/values.yaml

# Dry-run render all templates
helm template betmasterx ./helm/betmasterx | kubectl apply --dry-run=client -f -

# Terraform validate + format check
cd terraform/ECR && terraform fmt -check && terraform validate

# Build images locally
docker build -t betmasterx-backend:dev ./backend
docker build -t betmasterx-frontend:dev --target production ./frontend

# Run backend tests
cd backend && pip install pytest pytest-asyncio && pytest

# Check pod logs
kubectl logs -l app=betmasterx-backend -n betmasterx --tail=100 -f
kubectl logs -l app=betmasterx-frontend -n betmasterx --tail=50

# HPA status
kubectl get hpa -n betmasterx
```

---

## 📖 Troubleshooting

| Issue | Fix |
|---|---|
| Pods stuck in `Pending` | `kubectl describe pod <pod> -n betmasterx` — check node capacity |
| ALB not provisioned | Verify subnet tags `kubernetes.io/role/elb=1` and ALB controller is running |
| OTel traces not appearing | Check `OTEL_EXPORTER_OTLP_ENDPOINT` in configmap, verify Jaeger pod is running |
| ECR pull failure | Verify IRSA role ARN in serviceaccount annotation, check node IAM role |
| Helm deploy fails | `helm history betmasterx -n betmasterx` — `--atomic` auto-rolls back |

---

## 📄 License

MIT — see [LICENSE](./LICENSE)
ok

---

<div align="center">
Built with ❤️ as a production DevOps portfolio project · Terraform · Kubernetes · Helm · OpenTelemetry · GitHub Actions
</div>