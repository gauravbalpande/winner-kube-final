# ============================================================
# Variables for ECR + IRSA Terraform Module
# ============================================================

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix for resource names (e.g. betmasterx)"
  type        = string
  default     = "betmasterx"
}

variable "eks_cluster_name" {
  description = "Name of the EKS cluster (used to retrieve OIDC provider)"
  type        = string
  default     = "retail-dev-eksdemo"
}

variable "tags" {
  description = "Tags applied to all resources"
  type        = map(string)
  default = {
    Project     = "betmasterx"
    ManagedBy   = "terraform"
    Environment = "dev"
  }
}
