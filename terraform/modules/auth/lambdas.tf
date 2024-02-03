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

  memory_size = var.memory_size


}

// Define the permission to invoKe user sign up function
resource "aws_lambda_permission" "c8-user-signup-func" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c8-user-signup.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "${var.rest_api_execution_arn}/*/*"
}

/// ------- ORG SIGNUP --------- //////

// Org Sign up Lambda
resource "aws_lambda_function" "c8-org-signup" {
  function_name = "C8-AUTH-ORG-SIGNUP"
  role          = var.lambda_exec_role_arn

  s3_bucket = var.s3_bucket_id
  s3_key    = var.s3_bucket_key

  layers = [var.lambda_layer_id]


  runtime = var.python_runtime
  handler = var.org_signup_handler

  source_code_hash = var.archive_file_base_64_sha256

  memory_size = var.memory_size


}

// Define the permission to invoKe user sign up function
resource "aws_lambda_permission" "c8-org-signup-func" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c8-org-signup.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "${var.rest_api_execution_arn}/*/*"
}

///// ----- USER SIGN IN ------ /////

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

  memory_size = var.memory_size


}

// Define the permission to invoKe user sign In function
resource "aws_lambda_permission" "c8-user-signin-func_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c8-user-signin.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "${var.rest_api_execution_arn}/*/*"
}



//// Verification Code ////////

// Handles v1/auth/verification-code
resource "aws_lambda_function" "c8-verification-code-lambda" {
  function_name = "C8-DEV-AUTH-VERIFICATION-CODE"
  role          = var.lambda_exec_role_arn

  s3_bucket = var.s3_bucket_id
  s3_key    = var.s3_bucket_key

  layers = [var.lambda_layer_id]


  runtime = var.python_runtime
  handler = var.verification_codes_handler

  source_code_hash = var.archive_file_base_64_sha256

  memory_size = var.memory_size


}

// Define the permission to invoke the function
resource "aws_lambda_permission" "c8-verification-code-lambda-permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c8-verification-code-lambda.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "${var.rest_api_execution_arn}/*/*"
}

//// Verification Code Confirm ////////

// Handles {version}/auth/verification-code/confirm
resource "aws_lambda_function" "c8-verification-code-confirm-lambda" {
  function_name = "C8-DEV-AUTH-VERIFICATION-CODE-CONFIRM"
  role          = var.lambda_exec_role_arn

  s3_bucket = var.s3_bucket_id
  s3_key    = var.s3_bucket_key

  layers = [var.lambda_layer_id]


  runtime = var.python_runtime
  handler = var.verification_codes_confirm_handler

  source_code_hash = var.archive_file_base_64_sha256
  memory_size      = var.memory_size

}

// Define the permission to invoke the function
resource "aws_lambda_permission" "c8-verification-code-confirm-lambda-permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.c8-verification-code-confirm-lambda.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "${var.rest_api_execution_arn}/*/*"
}

