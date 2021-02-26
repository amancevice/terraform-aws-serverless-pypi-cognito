variable "api_authorizer_name" {
  description = "API Gateway authorizer name"
  default     = "COGNITO"
}

variable "api_execution_arn" {
  description = "API Gateway execution ARN"
}

variable "api_id" {
  description = "API Gateway HTTP API ID"
}

variable "cognito_user_pool_name" {
  description = "Cognito user pool name"
}

variable "cognito_tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}

variable "iam_role_name" {
  description = "Serverless PyPI IAM role name"
}

variable "iam_role_policy_name" {
  description = "IAM role inline policy name"
  default     = "pypi-authorizer-permissions"
}

variable "lambda_alias_name" {
  description = "PyPI API Lambda alias name"
  default     = "prod"
}

variable "lambda_alias_function_version" {
  description = "PyPI API Lambda alias target function version"
  default     = "$LATEST"
}

variable "lambda_description" {
  description = "REST API authorizer Lambda function description"
  default     = "PyPI REST API Authorizer"
}

variable "lambda_function_name" {
  description = "REST API authorizer Lambda function name"
}

variable "lambda_publish" {
  description = "REST API authorizer Lambda publish trigger"
  type        = bool
  default     = false
}

variable "lambda_tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}

variable "log_group_retention_in_days" {
  description = "CloudWatch log group retention period"
  default     = 30
}

variable "log_group_tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
