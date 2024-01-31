// Define the lambda to handle all requests to /users
resource "aws_lambda_function" "c8-auth-func" {
  function_name = "C8-DEV-AUTH"
  role          = var.lambda_exec_role_arn

  s3_bucket = var.s3_bucket_id
  s3_key    = var.s3_bucket_key

  layers = [var.lambda_layer_id]

  runtime = "python3.8"
  handler = var.handler

  source_code_hash = var.archive_file_base_64_sha256

}

// Define the permission to invoKe a function.
resource "aws_lambda_permission" "c8-auth-func" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c8-auth-func.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "${var.rest_api_execution_arn}/*/*"
}

// User Sign up Lambda
resource "aws_lambda_function" "c8-user-signup" {
  function_name = "C8-DEV-AUTH-SIGNUP"
  role          = var.lambda_exec_role_arn

  s3_bucket = var.s3_bucket_id
  s3_key    = var.s3_bucket_key

  layers = [var.lambda_layer_id]


  runtime = "python3.8"
  handler = var.user_sign_up_handler

  source_code_hash = var.archive_file_base_64_sha256

}

// Define the permission to invoKe user sign up function
resource "aws_lambda_permission" "c8-user-signup-func" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c8-user-signup.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "${var.rest_api_execution_arn}/*/*"
}


// User Sign In Lambda
resource "aws_lambda_function" "c8-user-signin" {
  function_name = "C8-DEV-AUTH-SIGNIN"
  role          = var.lambda_exec_role_arn

  s3_bucket = var.s3_bucket_id
  s3_key    = var.s3_bucket_key

  layers = [var.lambda_layer_id]


  runtime = "python3.8"
  handler = var.user_sign_in_handler

  source_code_hash = var.archive_file_base_64_sha256

}

// Define the permission to invoKe user sign In function
resource "aws_lambda_permission" "c8-user-signin-func_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c8-user-signin.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "${var.rest_api_execution_arn}/*/*"
}