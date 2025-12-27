#!/bin/bash

# BetMasterX Kubernetes Deployment Script
# Usage: ./deploy.sh [namespace]

set -e

NAMESPACE=${1:-betmasterx}
AWS_REGION=${AWS_REGION:-us-east-1}
AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-262164343217}

echo "🚀 Deploying BetMasterX to Kubernetes namespace: $NAMESPACE"

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

echo "✅ Kubernetes cluster is accessible"

# Create namespace
echo "📦 Creating namespace..."
kubectl apply -f namespace.yaml

# Create ECR secret (if AWS credentials are available)
if command -v aws &> /dev/null; then
    echo "🔐 Creating ECR registry secret..."
    kubectl create secret docker-registry ecr-registry-secret \
        --namespace=$NAMESPACE \
        --docker-server=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com \
        --docker-username=AWS \
        --docker-password=$(aws ecr get-login-password --region ${AWS_REGION}) \
        --dry-run=client -o yaml | kubectl apply -f - || echo "⚠️  ECR secret may already exist"
else
    echo "⚠️  AWS CLI not found. Skipping ECR secret creation."
    echo "   Please create it manually if using ECR images."
fi

# Check if secrets.yaml exists
if [ ! -f "secrets.yaml" ]; then
    echo "⚠️  secrets.yaml not found!"
    echo "   Creating from template..."
    cp secrets.yaml.template secrets.yaml
    echo "   Please edit secrets.yaml with your actual values and run this script again."
    exit 1
fi

# Create application secrets
echo "🔒 Creating application secrets..."
kubectl apply -f secrets.yaml

# Deploy application
echo "🚀 Deploying application..."
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
kubectl apply -f ingress.yaml

# Wait for deployments
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/backend -n $NAMESPACE || true
kubectl wait --for=condition=available --timeout=300s deployment/frontend -n $NAMESPACE || true

# Show status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Deployment Status:"
kubectl get pods -n $NAMESPACE
echo ""
echo "🌐 Services:"
kubectl get svc -n $NAMESPACE
echo ""
echo "🔗 Ingress:"
kubectl get ingress -n $NAMESPACE
echo ""
echo "📝 To view logs:"
echo "   kubectl logs -f deployment/backend -n $NAMESPACE"
echo "   kubectl logs -f deployment/frontend -n $NAMESPACE"


