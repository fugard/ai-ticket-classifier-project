variable "project_name" {
  description = "Base project name."
  type        = string
  default     = "ai-ticket-classifier"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region for deployment."
  type        = string
  default     = "eu-west-2"
}

variable "notification_email" {
  description = "Email subscriber for SNS notifications."
  type        = string
  default     = "change-me@example.com"
}

variable "bedrock_model_id" {
  description = "Optional AWS Bedrock model ID. Leave empty to use heuristic mode."
  type        = string
  default     = ""
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds."
  type        = number
  default     = 30
}

variable "lambda_memory_size" {
  description = "Lambda memory size in MB."
  type        = number
  default     = 512
}
