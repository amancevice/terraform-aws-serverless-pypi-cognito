terraform {
  required_version = "~> 0.13"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

locals {
  cognito = {
    user_pool_name = var.cognito_user_pool_name
    tags           = var.cognito_tags
  }

  http_api = {
    id              = var.api_id
    authorizer_name = var.api_authorizer_name
    execution_arn   = var.api_execution_arn
  }

  iam_role = {
    name        = var.iam_role_name
    policy_name = var.iam_role_policy_name
  }

  lambda = {
    alias_name             = var.lambda_alias_name
    alias_function_version = var.lambda_alias_function_version
    description            = var.lambda_description
    filename               = "${path.module}/package.zip"
    function_name          = var.lambda_function_name
    publish                = var.lambda_publish
    source_code_hash       = filebase64sha256("${path.module}/package.zip")
    tags                   = var.lambda_tags
  }

  logs = {
    retention_in_days = var.log_group_retention_in_days
    tags              = var.log_group_tags
  }
}

# IAM

data "aws_iam_role" "role" {
  name = local.iam_role.name
}

data "aws_iam_policy_document" "policy" {
  statement {
    sid       = "InvokeAuthorizer"
    actions   = ["lambda:InvokeFunction"]
    resources = [aws_lambda_function.lambda.arn]
  }

  statement {
    sid       = "WriteLambdaLogs"
    resources = ["*"]

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
  }

  statement {
    sid       = "InitiateAuth"
    actions   = ["cognito-idp:InitiateAuth"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "policy" {
  name   = local.iam_role.policy_name
  role   = data.aws_iam_role.role.id
  policy = data.aws_iam_policy_document.policy.json
}

# COGNITO

resource "aws_cognito_user_pool" "pool" {
  name = local.cognito.user_pool_name
  tags = local.cognito.tags
}

resource "aws_cognito_user_pool_client" "client" {
  name         = local.cognito.user_pool_name
  user_pool_id = aws_cognito_user_pool.pool.id

  explicit_auth_flows = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
  ]
}

# LAMBDA :: AUTHORIZER

resource "aws_cloudwatch_log_group" "logs" {
  name              = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
  retention_in_days = local.logs.retention_in_days
  tags              = local.logs.tags
}

resource "aws_lambda_function" "lambda" {
  description      = local.lambda.description
  filename         = local.lambda.filename
  function_name    = local.lambda.function_name
  handler          = "index.handler"
  publish          = local.lambda.publish
  role             = data.aws_iam_role.role.arn
  runtime          = "python3.8"
  source_code_hash = local.lambda.source_code_hash
  tags             = local.lambda.tags

  environment {
    variables = {
      COGNITO_CLIENT_ID = aws_cognito_user_pool_client.client.id
    }
  }
}

resource "aws_lambda_permission" "invoke_api" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${local.http_api.execution_arn}/*/*/*"
  statement_id  = "InvokeAPI"
}



# REST API :: AUTHORIZER

resource "aws_apigatewayv2_authorizer" "authorizer" {
  api_id                            = local.http_api.id
  authorizer_payload_format_version = "2.0"
  authorizer_type                   = "REQUEST"
  authorizer_uri                    = aws_lambda_function.lambda.invoke_arn
  enable_simple_responses           = true
  identity_sources                  = ["$request.header.Authorization"]
  name                              = local.http_api.authorizer_name
}

/*
resource "aws_apigatewayv2_route_response" "unauthorized" {
  api_id        = local.http_api.id
  status_code   = "401"
  response_type = "UNAUTHORIZED"

  response_parameters = {
    "gatewayresponse.header.WWW-Authenticate" = "'Basic'"
  }

  response_templates = {
    "application/json" = "{\"message\":$context.error.messageString}"
  }
}
*/
