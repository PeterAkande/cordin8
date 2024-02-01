output "first_func_name" {
  description = "Name of Lambda function is"
  value       = aws_lambda_function.first_func.function_name
}


output "base_url" {
  description = "Base URL for API Gateway stage."

  value = aws_api_gateway_stage.c8_rest_api_gateway_stage.invoke_url
}

output "exec_role_arn" {
  value = aws_iam_role.c8_lambda_exec_role.arn
}

output "userpool_id" {
  value = aws_cognito_user_pool.c8-user-pool.arn
}

output "userpool_client" {
  value = aws_cognito_user_pool_client.client.id
}