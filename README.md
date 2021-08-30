# Serverless PyPI with Cognito

[![terraform](https://img.shields.io/github/v/tag/amancevice/terraform-aws-serverless-pypi-cognito?color=62f&label=version&logo=terraform&style=flat-square)](https://registry.terraform.io/modules/amancevice/serverless-pypi/aws)
[![py.test](https://img.shields.io/github/workflow/status/amancevice/terraform-aws-serverless-pypi-cognito/py.test?logo=github&style=flat-square)](https://github.com/amancevice/terraform-aws-serverless-pypi-cognito/actions)
[![coverage](https://img.shields.io/codeclimate/coverage/amancevice/terraform-aws-serverless-pypi-cognito?logo=code-climate&style=flat-square)](https://codeclimate.com/github/amancevice/terraform-aws-serverless-pypi-cognito/test_coverage)
[![maintainability](https://img.shields.io/codeclimate/maintainability/amancevice/terraform-aws-serverless-pypi-cognito?logo=code-climate&style=flat-square)](https://codeclimate.com/github/amancevice/terraform-aws-serverless-pypi-cognito/maintainability)

Secure a serverless PyPI deployed with the [serverless-pypi](https://github.com/amancevice/terraform-aws-serverless-pypi) Terraform module using AWS Cognito and Basic Authentication.

## Usage

Provide a single username and password to the module to create an API Gateway authorizer function for your serverless PyPI:

```terraform
resource "aws_apigatewayv2_api" "pypi" {
  name          = "pypi"
  protocol_type = "HTTP"
  # …
}

module serverless_pypi {
  source  = "amancevice/serverless-pypi-cognito/aws"
  version = "~> 4.1"

  api_authorization_type = "CUSTOM"
  api_authorizer_id      = module.serverless_pypi_cognito.authorizer.id
  # …
}

module serverless_pypi_cognito {
  source  = "amancevice/serverless-pypi-cognito/aws"
  version = "~> 3.0"

  api_id                 = aws_apigatewayv2_api.pypi.id
  cognito_user_pool_name = "serverless-pypi-cognito-pool"
  iam_role_name          = module.serverless_pypi.iam_role.name
  lambda_function_name   = "serverless-pypi-authorizer"
}
```
