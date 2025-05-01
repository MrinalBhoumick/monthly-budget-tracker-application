variable "region" {
  description = "AWS region where resources will be created"
  type        = string
}

variable "account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "ecr_repo_name" {
  description = "ECR Repository name"
  type        = string
}

variable "ecs_cluster" {
  description = "ECS Cluster name"
  type        = string
}

variable "ecs_task_def" {
  description = "ECS Task Definition name"
  type        = string
}

variable "ecs_service" {
  description = "ECS Service name"
  type        = string
}

variable "load_balancer_name" {
  description = "ALB Name"
  type        = string
}

variable "target_group_name" {
  description = "ALB Target Group Name"
  type        = string
}

variable "subnets" {
  description = "Subnets where ECS and ALB will be deployed"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID where ECS and ALB will be deployed"
  type        = string
}

variable "cpu" {
  description = "The number of CPU units to reserve for the container"
  type        = number
  default     = 1024
}

variable "memory" {
  description = "The amount of memory (in MiB) to allocate to the container"
  type        = number
  default     = 3072
}

variable "ecs_min_capacity" {
  description = "Minimum ECS Service task count"
  type        = number
  default     = 1
}

variable "ecs_max_capacity" {
  description = "Maximum ECS Service task count"
  type        = number
  default     = 5
}

variable "cpu_target_value" {
  description = "Target CPU utilization percentage for scaling"
  type        = number
  default     = 75
}

variable "memory_target_value" {
  description = "Target memory utilization percentage for scaling"
  type        = number
  default     = 75
}

variable "scale_in_cooldown" {
  description = "Cooldown period after scale-in (in seconds)"
  type        = number
  default     = 300
}

variable "scale_out_cooldown" {
  description = "Cooldown period after scale-out (in seconds)"
  type        = number
  default     = 300
}