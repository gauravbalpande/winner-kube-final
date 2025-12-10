# Deployment Guide: BetMasterX on AWS ECS Fargate

This guide walks you through deploying BetMasterX to AWS ECS Fargate using Terraform.

## Architecture Overview

```
Internet
   │
   ▼
Application Load Balancer (ALB)
   │
   ├─ /api/* ──────────────────► Backend Service (ECS Fargate)
   │                                 └─ FastAPI on port 8000
   │
   └─ /* (all other paths) ──────► Frontend Service (ECS Fargate)
                                        └─ nginx on port 80
```

## Prerequisites

1. AWS CLI installed and configured
2. Docker installed
3. Terraform >= 1.0 installed
4. AWS account with appropriate permissions
5. ECR repositories created (or use Terraform to create them)

## Step-by-Step Deployment

### 1. Create ECR Repositories

```bash
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create repositories
aws ecr create-repository --repository-name betmasterx-frontend --region $AWS_REGION
aws ecr create-repository --repository-name betmasterx-backend --region $AWS_REGION
```

### 2. Build and Push Docker Images

#### Frontend

```bash
cd frontend

# Create .env.production file (if not exists)
echo "VITE_API_URL=/api" > .env.production

# Build image
docker build -t betmasterx-frontend:latest .

# Tag for ECR
docker tag betmasterx-frontend:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-frontend:latest

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Push image
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-frontend:latest
```

#### Backend

```bash
cd ../backend

# Build image
docker build -t betmasterx-backend:latest .

# Tag for ECR
docker tag betmasterx-backend:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-backend:latest

# Push image
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-backend:latest
```

### 3. Configure Terraform Variables

```bash
cd ../terraform

# Create terraform.tfvars
cat > terraform.tfvars << EOF
frontend_image = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-frontend:latest"
backend_image  = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-backend:latest"
aws_region     = "$AWS_REGION"
EOF
```

### 4. Configure Backend Environment Variables

**Important**: The backend containers need Supabase credentials. You have two options:

#### Option A: Add to Task Definition (Quick but not secure)

Edit `terraform/main.tf` and add environment variables to the backend task definition:

```hcl
environment = [
  {
    name  = "SUPABASE_URL"
    value = "https://your-project.supabase.co"
  },
  {
    name  = "SUPABASE_KEY"
    value = "your-anon-key"
  },
  {
    name  = "SUPABASE_SERVICE_KEY"
    value = "your-service-role-key"
  },
  {
    name  = "SECRET_KEY"
    value = "your-secret-key"
  }
]
```

#### Option B: Use AWS Secrets Manager (Recommended for production)

1. Store secrets in AWS Secrets Manager
2. Reference them in the task definition using `secrets` instead of `environment`

### 5. Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply (this will create all resources)
terraform apply
```

### 6. Access Your Application

After deployment completes, get the ALB DNS name:

```bash
terraform output alb_dns_name
```

Access your application at: `http://<alb-dns-name>`

## Key Configuration Points

### Frontend

- **Port**: 80 (nginx)
- **API Base URL**: Uses `/api` (relative path) via `VITE_API_URL` environment variable
- **Build**: Multi-stage Docker build (node:18-alpine → nginx:alpine)
- **Static Assets**: Served by nginx with caching

### Backend

- **Port**: 8000 (uvicorn)
- **Health Check**: `/health` endpoint
- **CORS**: Currently allows all origins (`*`). For production, consider restricting.

### Load Balancer

- **Path Routing**:
  - `/api/*` → Backend target group
  - All other paths → Frontend target group
- **Health Checks**: Configured for both services

## Environment Variables

### Frontend (.env.production)

```env
VITE_API_URL=/api
```

This is automatically used by Vite during build.

### Backend (ECS Task Definition)

Add these environment variables to the backend task definition:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_KEY`
- `SECRET_KEY`

## Troubleshooting

### Frontend not loading

1. Check CloudWatch logs: `/ecs/betmasterx/frontend`
2. Verify ALB target group health
3. Check security group rules allow traffic from ALB

### Backend API errors

1. Check CloudWatch logs: `/ecs/betmasterx/backend`
2. Verify environment variables are set correctly
3. Check Supabase connection
4. Verify ALB routing rules for `/api/*`

### CORS errors

Since requests go through the same ALB domain, CORS should not be an issue. However, if you see CORS errors:
1. Check backend CORS configuration in `backend/main.py`
2. Verify ALB path routing is correct

## Scaling

Adjust the `desired_count` in the ECS service definitions:

```hcl
# In terraform/main.tf
resource "aws_ecs_service" "frontend" {
  desired_count = 3  # Increase as needed
}
```

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

**Note**: This will delete all resources created by Terraform, including the ECS services, ALB, and target groups.

## Production Recommendations

1. **HTTPS**: Add an ACM certificate and HTTPS listener to the ALB
2. **CORS**: Restrict CORS origins instead of using `*`
3. **Secrets**: Use AWS Secrets Manager for sensitive environment variables
4. **Monitoring**: Set up CloudWatch alarms and dashboards
5. **Auto Scaling**: Configure ECS auto-scaling based on CPU/memory
6. **WAF**: Enable AWS WAF on the ALB for additional security
7. **Log Retention**: Adjust CloudWatch log retention periods
8. **VPC**: Use custom VPC instead of default VPC for better isolation

## Cost Estimation

Approximate monthly costs (us-east-1):
- ALB: ~$16/month
- ECS Fargate (2 tasks each, 512MB frontend, 1GB backend): ~$30-40/month
- CloudWatch Logs: ~$0.50/GB ingested
- Data Transfer: Variable

Total: ~$50-60/month for baseline deployment

