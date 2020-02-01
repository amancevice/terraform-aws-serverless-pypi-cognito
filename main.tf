locals {
  api                         = var.api
  basic_auth_username         = var.basic_auth_username
  basic_auth_password         = var.basic_auth_password
  lambda_description          = var.lambda_description
  lambda_function_name        = var.lambda_function_name
  lambda_handler              = "index.handler"
  lambda_runtime              = "python3.8"
  log_group_retention_in_days = var.log_group_retention_in_days
  policy_name                 = var.policy_name
  role_description            = var.role_description
  role_name                   = var.role_name
  tags                        = var.tags
}

data archive_file package {
  source_file = "${path.module}/index.py"
  output_path = "${path.module}/package.zip"
  type        = "zip"
}

data aws_iam_policy_document assume_role {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = [
        "apigateway.amazonaws.com",
        "lambda.amazonaws.com",
      ]
    }
  }
}

data aws_iam_policy_document policy {
  statement {
    sid       = "InvokeAuthorizer"
    actions   = ["lambda:InvokeFunction"]
    resources = [aws_lambda_function.lambda.arn]
  }

  statement {
    sid = "WriteLambdaLogs"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["*"]
  }
}

resource aws_api_gateway_authorizer basic {
  authorizer_credentials = aws_iam_role.role.arn
  authorizer_uri         = aws_lambda_function.lambda.invoke_arn
  name                   = "BASIC"
  rest_api_id            = local.api.id
  type                   = "TOKEN"
}

resource aws_api_gateway_gateway_response unauthorized {
  rest_api_id   = local.api.id
  status_code   = "401"
  response_type = "UNAUTHORIZED"

  response_parameters = {
    "gatewayresponse.header.WWW-Authenticate" = "'Basic'"
  }

  response_templates = {
    "application/json" = "{\"message\":$context.error.messageString}"
  }
}

resource aws_cloudwatch_log_group logs {
  name              = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
  retention_in_days = local.log_group_retention_in_days
  tags              = local.tags
}

resource aws_iam_role role {
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  description        = local.role_description
  name               = local.role_name
  tags               = local.tags
}

resource aws_iam_role_policy policy {
  name   = local.policy_name
  role   = aws_iam_role.role.id
  policy = data.aws_iam_policy_document.policy.json
}

resource aws_lambda_function lambda {
  description      = local.lambda_description
  filename         = data.archive_file.package.output_path
  function_name    = local.lambda_function_name
  handler          = local.lambda_handler
  role             = aws_iam_role.role.arn
  runtime          = local.lambda_runtime
  source_code_hash = data.archive_file.package.output_base64sha256
  tags             = local.tags

  environment {
    variables = {
      BASIC_AUTH_USERNAME = local.basic_auth_username
      BASIC_AUTH_PASSWORD = local.basic_auth_password
    }
  }
}
