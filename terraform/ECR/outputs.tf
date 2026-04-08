# ============================================================
# ECR + IRSA Outputs
# ============================================================

output "backend_repository_url" {
  description = "ECR repository URL for the backend image"
  value       = aws_ecr_repository.backend.repository_url
}

output "frontend_repository_url" {
  description = "ECR repository URL for the frontend image"
  value       = aws_ecr_repository.frontend.repository_url
}

output "backend_repository_arn" {
  description = "ECR repository ARN for the backend"
  value       = aws_ecr_repository.backend.arn
}

output "frontend_repository_arn" {
  description = "ECR repository ARN for the frontend"
  value       = aws_ecr_repository.frontend.arn
}

output "backend_irsa_role_arn" {
  description = "IAM role ARN for backend IRSA (annotate SA with this)"
  value       = aws_iam_role.backend_irsa.arn
}

output "alb_controller_role_arn" {
  description = "IAM role ARN for AWS Load Balancer Controller IRSA"
  value       = aws_iam_role.alb_controller.arn
}
