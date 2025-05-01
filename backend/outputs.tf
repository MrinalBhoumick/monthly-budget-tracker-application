output "ecr_repo_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.repo.repository_url
}

output "alb_url" {
  description = "URL of the Application Load Balancer"
  value       = aws_lb.alb.dns_name
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.cluster.name
}
