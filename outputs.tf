output authorizer {
  description = "PyPI REST API Authorizer"
  value       = aws_api_gateway_authorizer.authorizer
}

output lambda {
  description = "PyPI REST API Authorizer Lambda function"
  value       = aws_lambda_function.lambda
}

output user_pool {
  description = "Cognito user pool"
  value       = aws_cognito_user_pool.pool
}

output user_pool_client {
  description = "Cognito user pool"
  value       = aws_cognito_user_pool_client.client
}
