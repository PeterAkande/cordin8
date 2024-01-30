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

