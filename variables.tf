variable api_id {
  description = "API Gateway REST API ID."
}

variable authorizer_name {
  description = "API Gateway authorizer name."
  default     = "COGNITO"
}

variable lambda_description {
  description = "REST API authorizer Lambda function description."
  default     = "PyPI REST API Authorizer"
}

variable lambda_function_name {
  description = "REST API authorizer Lambda function name."
}

variable log_group_retention_in_days {
  description = "CloudWatch log group retention period."
  default     = 30
}

variable policy_name {
  description = "IAM role inline policy name."
  default     = "pypi-authorizer-permissions"
}

variable role_description {
  description = "Lambda functions IAM role description."
  default     = "PyPI Lambda permissions"
}

variable role_name {
  description = "Authorizer Lambda function role name."
}

variable tags {
  description = "Resource tags."
  type        = map
  default     = {}
}

variable user_pool_name {
  description = "Cognito user pool name."
}
