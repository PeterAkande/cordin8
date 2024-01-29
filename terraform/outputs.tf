output "first_func_name" {
  description = "Name of Lambda function is"
  value       = aws_lambda_function.first_func.function_name
}


output "base_url" {
  description = "Base URL for API Gateway stage."

  value = aws_api_gateway_stage.c8_rest_api_gateway_stage.invoke_url
}