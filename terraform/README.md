# Terraform Infrastructure for BetMasterX on AWS ECS Fargate

This Terraform configuration deploys the BetMasterX application on AWS ECS Fargate with an Application Load Balancer.

## Architecture

- **Frontend**: React/Vite app served by nginx on port 80
- **Backend**: FastAPI app running on port 8000
- **Load Balancer**: ALB with path-based routing:
  - `/api/*` → Backend service
  - All other paths → Frontend service

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. Docker images pushed to ECR
3. Terraform >= 1.0 installed

## Setup

1. **Build and push Docker images to ECR**:
   ```bash
   # Set your AWS account ID and region
   export AWS_ACCOUNT_ID=123456789012
   export AWS_REGION=us-east-1
   
   # Create ECR repositories (if not exists)
   aws ecr create-repository --repository-name betmasterx-frontend --region $AWS_REGION
   aws ecr create-repository --repository-name betmasterx-backend --region $AWS_REGION
   
   # Login to ECR
   aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
   
   # Build and push frontend
   cd frontend
   docker build -t betmasterx-frontend:latest .
   docker tag betmasterx-frontend:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-frontend:latest
   docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-frontend:latest
   
   # Build and push backend
   cd ../backend
   docker build -t betmasterx-backend:latest .
   docker tag betmasterx-backend:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-backend:latest
   docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/betmasterx-backend:latest
   ```

2. **Create terraform.tfvars**:
   ```bash
   cd terraform
   cp variables.tf.example terraform.tfvars
   # Edit terraform.tfvars with your actual ECR image URIs and region
   ```

3. **Initialize and apply Terraform**:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **Get the ALB DNS name**:
   ```bash
   terraform output alb_dns_name
   ```

   Access your application at: `http://<alb-dns-name>`

## Variables

- `frontend_image`: ECR image URI for frontend (required)
- `backend_image`: ECR image URI for backend (required)
- `aws_region`: AWS region (default: us-east-1)
- `app_name`: Application name (default: betmasterx)
- `environment`: Environment name (default: production)

## Important Notes

1. **Environment Variables**: Backend containers need environment variables for Supabase connection. Add these to the task definition or use AWS Secrets Manager/Parameter Store.

2. **CORS Configuration**: Ensure your backend CORS settings allow requests from your ALB domain in production.

3. **Security Groups**: The current setup allows HTTP traffic on port 80. For production, consider:
   - Using HTTPS with ACM certificate
   - Restricting security group rules
   - Enabling WAF on the ALB

4. **Scaling**: Services are configured with `desired_count = 2`. Adjust based on your needs.

5. **Logs**: CloudWatch logs are retained for 7 days. Adjust retention as needed.

## Cleanup

To destroy all resources:
```bash
terraform destroy
```

