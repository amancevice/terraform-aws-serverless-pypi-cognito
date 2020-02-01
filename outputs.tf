output authorizer {
  description = "PyPI REST API Authorizer."
  value       = aws_api_gateway_authorizer.basic
}

output lambda {
  description = "PyPI REST API Authorizer Lambda function."
  value       = aws_lambda_function.lambda
}
