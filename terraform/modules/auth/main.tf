// Define resource
// Would handle /{version}/auth
resource "aws_api_gateway_resource" "c8-auth-resource" {
  rest_api_id = var.rest_api_id
  parent_id   = var.rest_api_parent_resource_id
  path_part   = "auth"
}


////// --------- Sign In ----------///

// It would handle /{version}/auth/signin/
resource "aws_api_gateway_resource" "c8-auth-signin" {
  rest_api_id = var.rest_api_id
  parent_id   = aws_api_gateway_resource.c8-auth-resource.id
  path_part   = "signin"
}

// Define a method on Sign in
resource "aws_api_gateway_method" "c8-signin_post" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_resource.c8-auth-signin.id

  authorization = "NONE"
  http_method   = "POST"
}

// Define the Integration on that method
resource "aws_api_gateway_integration" "c8_signin_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_resource.c8-auth-signin.id
  http_method             = aws_api_gateway_method.c8-signin_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.c8-user-signin.invoke_arn
}


////// --------- Sign Up ----------///

// It would handle /{version}/auth/signin/
resource "aws_api_gateway_resource" "c8-auth-user-signup" {
  rest_api_id = var.rest_api_id
  parent_id   = aws_api_gateway_resource.c8-auth-resource.id
  path_part   = "signup"
}

// Define a method on Sign in
resource "aws_api_gateway_method" "c8-signup_post" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_resource.c8-auth-user-signup.id

  authorization = "NONE"
  http_method   = "POST"
}

// Define the Integration on that method
resource "aws_api_gateway_integration" "c8_signup_integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_resource.c8-auth-user-signup.id
  http_method             = aws_api_gateway_method.c8-signup_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.c8-user-signup.invoke_arn
}

///------- Verify Code ---------////

// This would handle /{version}/auth/verification-code
resource "aws_api_gateway_resource" "c8-send-verification-code" {
  parent_id   = aws_api_gateway_resource.c8-auth-resource.id
  rest_api_id = var.rest_api_id
  path_part   = "verification-code"
}

resource "aws_api_gateway_method" "c8-verification-code-post" {
  resource_id = aws_api_gateway_resource.c8-send-verification-code.id
  rest_api_id = var.rest_api_id

  authorization = "NONE"
  http_method   = "POST"
}

resource "aws_api_gateway_integration" "c8-verification-integration" {
  resource_id = aws_api_gateway_resource.c8-send-verification-code.id
  rest_api_id = var.rest_api_id
  http_method = aws_api_gateway_method.c8-verification-code-post.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"

  uri = aws_lambda_function.c8-verification-code-lambda.invoke_arn

}

///------- Verify Code Confirm ---------////

// This would handle /{version}/auth/verification-code/confirm
resource "aws_api_gateway_resource" "c8-verification-code-confirm" {
  parent_id   = aws_api_gateway_resource.c8-send-verification-code.id
  rest_api_id = var.rest_api_id
  path_part   = "confirm"
}

resource "aws_api_gateway_method" "c8-verification-code-confirm-post" {
  resource_id = aws_api_gateway_resource.c8-verification-code-confirm.id
  rest_api_id = var.rest_api_id

  authorization = "NONE"
  http_method   = "POST"
}

resource "aws_api_gateway_integration" "c8-verification-code-confirm-integration" {
  resource_id = aws_api_gateway_resource.c8-verification-code-confirm.id
  rest_api_id = var.rest_api_id
  http_method = aws_api_gateway_method.c8-verification-code-confirm-post.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"

  uri = aws_lambda_function.c8-verification-code-confirm-lambda.invoke_arn

}

/// ---- ORG SIGN UP ------ //// 

// It would handle /{version}/auth/org/
resource "aws_api_gateway_resource" "c8-org-auth-resource" {
  rest_api_id = var.rest_api_id
  parent_id   = aws_api_gateway_resource.c8-auth-resource.id
  path_part   = "org"
}

// It would handle /{version}/auth/org/signup/
resource "aws_api_gateway_resource" "c8-auth-org-signup" {
  rest_api_id = var.rest_api_id
  parent_id   = aws_api_gateway_resource.c8-org-auth-resource.id
  path_part   = "signup"
}

// Define a method on Sign in
resource "aws_api_gateway_method" "c8-org-signup-post" {
  rest_api_id = var.rest_api_id
  resource_id = aws_api_gateway_resource.c8-auth-org-signup.id

  authorization = "NONE"
  http_method   = "POST"
}

// Define the Integration on that method
resource "aws_api_gateway_integration" "c8-org-signup-integration" {
  rest_api_id             = var.rest_api_id
  resource_id             = aws_api_gateway_resource.c8-auth-org-signup.id
  http_method             = aws_api_gateway_method.c8-org-signup-post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.c8-org-signup.invoke_arn
}
