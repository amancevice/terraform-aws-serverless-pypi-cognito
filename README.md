# Serverless PyPI Basic Auth

This is a very insecure proof-of-concept of how to secure a serverless PyPI instance deployed with the [serverless-pypi](https://github.com/amancevice/terraform-aws-serverless-pypi) Terraform module.

This module is provided as a proof-of-concept and **should not** be used in production.

## Usage

Provide a single username and password to the module to create an API Gateway authorizer function for your serverless PyPI:

```hcl
module serverless_pypi_basic_auth {
  source  = "amancevice/serverless-pypi-basic-auth/aws"
  version = "~> 0.1"

  api                  = "<rest-api-id>"
  basic_auth_username  = "<pypi-user>"
  basic_auth_password  = "<pypi-password>"
  lambda_function_name = "pypi-authorizer"
  role_name            = "pypi-authorizer-role"
}
```

You will also need to update your serverless PyPI module with the authorizer ID and authorization strategy:

```hcl
module serverless_pypi {
  source  = "amancevice/serverless-pypi/aws"
  version = "~> 0.2"

  # ...
  api_authorization = "CUSTOM"
  api_authorizer_id = module.serverless_pypi_basic_auth.authorizer.id
  # ...
}
```
