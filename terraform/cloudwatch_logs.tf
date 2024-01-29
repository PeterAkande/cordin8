resource "aws_cloudwatch_log_group" "first_func_lg" {
  name = "/aws/cordin8/${aws_lambda_function.first_func.function_name}"

  retention_in_days = 14 // Delete logs after 14 days
}