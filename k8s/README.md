# Kubernetes Deployment Guide

This directory contains Kubernetes manifests for deploying BetMasterX on a Kubernetes cluster (EKS, GKE, AKS, or local).

## Prerequisites

1. **Kubernetes Cluster** (EKS, GKE, AKS, or local like minikube/kind)
2. **kubectl** configured to access your cluster
3. **AWS ECR Access** (if using ECR images)
4. **ALB Ingress Controller** (for AWS EKS) or **NGINX Ingress Controller** (for other clusters)

## Quick Start

### 1. Create Namespace

```bash
kubectl apply -f namespace.yaml
```

### 2. Create ECR Secret (for AWS EKS)

If using ECR images, create the registry secret:

```bash
kubectl create secret docker-registry ecr-registry-secret \
  --namespace=betmasterx \
  --docker-server=262164343217.dkr.ecr.us-east-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region us-east-1)
```

### 3. Create Application Secrets

Copy the template and fill in your values:

```bash
cp secrets.yaml.template secrets.yaml
# Edit secrets.yaml with your actual values
kubectl apply -f secrets.yaml
```

**Important**: Never commit `secrets.yaml` to git!

### 4. Deploy Application

Deploy all resources:

```bash
kubectl apply -f .
```

Or using kustomize:

```bash
kubectl apply -k .
```

### 5. Verify Deployment

```bash
# Check pods
kubectl get pods -n betmasterx

# Check services
kubectl get svc -n betmasterx

# Check ingress
kubectl get ingress -n betmasterx

# View logs
kubectl logs -f deployment/backend -n betmasterx
kubectl logs -f deployment/frontend -n betmasterx
```

## Architecture

```
Internet
   │
   ▼
Ingress (ALB/Nginx)
   │
   ├─ /api/* ────────► Backend Service (ClusterIP)
   │                      └─ Backend Pods (port 8000)
   │
   └─ /* ────────────► Frontend Service (ClusterIP)
                          └─ Frontend Pods (port 80)
```

## Configuration

### Image Configuration

Update image tags in deployment files:
- `backend-deployment.yaml`: Update `image` field
- `frontend-deployment.yaml`: Update `image` field

### Resource Limits

Adjust CPU/memory requests and limits in:
- `backend-deployment.yaml`
- `frontend-deployment.yaml`

### Replicas

Change replica count in deployment files:
- `backend-deployment.yaml`: `spec.replicas`
- `frontend-deployment.yaml`: `spec.replicas`

## Ingress Configuration

### AWS EKS (ALB Ingress Controller)

The `ingress.yaml` is configured for AWS ALB Ingress Controller. Ensure you have:

1. ALB Ingress Controller installed in your cluster
2. IAM permissions for the controller to create ALBs

To install ALB Ingress Controller:
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.7/docs/install/v2_4_7_full.yaml
```

### Other Clusters (NGINX Ingress)

For non-AWS clusters, update `ingress.yaml`:

```yaml
annotations:
  kubernetes.io/ingress.class: nginx
  # Remove ALB-specific annotations
```

## Health Checks

- **Backend**: `/api/health` on port 8000
- **Frontend**: `/health` on port 80

Both deployments include liveness and readiness probes.

## Scaling

### Manual Scaling

```bash
kubectl scale deployment backend -n betmasterx --replicas=3
kubectl scale deployment frontend -n betmasterx --replicas=3
```

### Horizontal Pod Autoscaler (HPA)

Create `hpa.yaml`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: betmasterx
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Updating Deployments

### Rolling Update

```bash
# Update image
kubectl set image deployment/backend backend=NEW_IMAGE_TAG -n betmasterx
kubectl set image deployment/frontend frontend=NEW_IMAGE_TAG -n betmasterx

# Check rollout status
kubectl rollout status deployment/backend -n betmasterx
kubectl rollout status deployment/frontend -n betmasterx

# Rollback if needed
kubectl rollout undo deployment/backend -n betmasterx
```

## Monitoring (Future: Prometheus & Grafana)

The manifests are structured to support Prometheus scraping:

1. **ServiceMonitor** (for Prometheus Operator):
   - Add labels to services: `prometheus.io/scrape: "true"`
   - Add annotations: `prometheus.io/port: "8000"`

2. **Grafana Dashboards**:
   - Will be added in future updates
   - Use service discovery to find pods

## ArgoCD Integration (Future)

The `kustomization.yaml` file is ready for ArgoCD:

1. Create ArgoCD Application:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: betmasterx
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/yourusername/winner.git
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: betmasterx
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

2. ArgoCD will automatically sync changes from the repository.

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n betmasterx

# Check events
kubectl get events -n betmasterx --sort-by='.lastTimestamp'
```

### Image pull errors

```bash
# Verify ECR secret exists
kubectl get secret ecr-registry-secret -n betmasterx

# Recreate if needed
kubectl create secret docker-registry ecr-registry-secret \
  --namespace=betmasterx \
  --docker-server=262164343217.dkr.ecr.us-east-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region us-east-1) \
  --dry-run=client -o yaml | kubectl apply -f -
```

### Ingress not working

```bash
# Check ingress status
kubectl describe ingress betmasterx-ingress -n betmasterx

# For ALB: Check AWS console for ALB creation
# For Nginx: Check ingress controller logs
```

## Cleanup

To remove all resources:

```bash
kubectl delete namespace betmasterx
```

Or delete individual resources:

```bash
kubectl delete -f .
```

## Next Steps

1. ✅ Kubernetes manifests (current)
2. ⏳ ArgoCD integration
3. ⏳ Prometheus monitoring
4. ⏳ Grafana dashboards
5. ⏳ CI/CD pipeline integration


