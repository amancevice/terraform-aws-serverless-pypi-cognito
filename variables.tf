variable "cognito_user_pool_name" {
  description = "Cognito user pool name"
}

variable "iam_role_description" {
  description = "Lambda functions IAM role description"
  default     = "PyPI Lambda permissions"
}

variable "iam_role_name" {
  description = "Authorizer Lambda function role name"
}

variable "iam_role_policy_name" {
  description = "IAM role inline policy name"
  default     = "pypi-authorizer-permissions"
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

variable "lambda_qualifier" {
  description = "REST API authorizer Lambda function qualifier"
  default     = null
}

variable "log_group_retention_in_days" {
  description = "CloudWatch log group retention period"
  default     = 30
}

variable "rest_api_authorizer_name" {
  description = "API Gateway authorizer name"
  default     = "COGNITO"
}

variable "rest_api_id" {
  description = "API Gateway REST API ID"
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
