output "api_authorizer" {
  description = "PyPI REST API Authorizer"
  value       = aws_apigatewayv2_authorizer.authorizer
}

output "cognito_user_pool" {
  description = "Cognito user pool"
  value       = aws_cognito_user_pool.pool
}

output "cognito_user_pool_client" {
  description = "Cognito user pool"
  value       = aws_cognito_user_pool_client.client
}

output "lambda" {
  description = "PyPI REST API Authorizer Lambda function"
  value       = aws_lambda_function.lambda
}
