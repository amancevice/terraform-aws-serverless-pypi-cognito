# Serverless PyPI with Cognito

Secure a serverless PyPI deployed with the [serverless-pypi](https://github.com/amancevice/terraform-aws-serverless-pypi) Terraform module using AWS Cognito and Basic Authentication.

## Usage

Provide a single username and password to the module to create an API Gateway authorizer function for your serverless PyPI:

```hcl
module serverless_pypi_cognito {
  source  = "amancevice/serverless-pypi-cognito/aws"
  version = "~> 0.2"

  api                  = "<rest-api-id>"
  lambda_function_name = "pypi-authorizer"
  role_name            = "pypi-authorizer-role"
  user_pool_name       = "serverless-pypi"
}
```

You will also need to update your serverless PyPI module with the authorizer ID and authorization strategy:

```hcl
module serverless_pypi {
  source  = "amancevice/serverless-pypi/aws"
  version = "~> 0.2"

  # ...
  api_authorization = "CUSTOM"
  api_authorizer_id = module.serverless_pypi_cognito.authorizer.id
  # ...
}
```
