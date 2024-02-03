module "auth" {
  source = "./modules/auth"

  rest_api_id                 = aws_api_gateway_rest_api.c8_rest_api_gateway.id
  rest_api_parent_resource_id = aws_api_gateway_resource.c8_rest_api_version.id
  lambda_exec_role_arn        = aws_iam_role.c8_lambda_exec_role.arn
  s3_bucket_id                = aws_s3_bucket.cordin8_lambda_bucket.id
  s3_bucket_key               = aws_s3_object.c8_lambda_code.key
  archive_file_base_64_sha256 = data.archive_file.c8_lambda_code_zip.output_base64sha256
  rest_api_execution_arn      = aws_api_gateway_rest_api.c8_rest_api_gateway.execution_arn
  lambda_layer_id             = aws_lambda_layer_version.c8-lambda-layer.arn
  python_runtime              = var.python_runtime
  memory_size                 = var.memory_size
}


// Define the AWS API Gateway. Primarily, only one is needed in an application
resource "aws_api_gateway_rest_api" "c8_rest_api_gateway" {
  name = "cordinate-rest-api-gateway"

}

// Define the Version Resource. Can always remove it 
resource "aws_api_gateway_resource" "c8_rest_api_version" {
  rest_api_id = aws_api_gateway_rest_api.c8_rest_api_gateway.id
  parent_id   = aws_api_gateway_rest_api.c8_rest_api_gateway.root_resource_id
  path_part   = var.api_version
}

// Define the Resource. Like a parent path.
resource "aws_api_gateway_resource" "c8_test_resource" {
  rest_api_id = aws_api_gateway_rest_api.c8_rest_api_gateway.id
  parent_id   = aws_api_gateway_resource.c8_rest_api_version.id
  path_part   = "test"
}

// The Individual Methods in a resurce
resource "aws_api_gateway_method" "c8_test_resource_get" {
  rest_api_id   = aws_api_gateway_rest_api.c8_rest_api_gateway.id
  resource_id   = aws_api_gateway_resource.c8_test_resource.id
  authorization = "NONE"
  http_method   = "GET"
}

// Define the Integrations needed For the GET function
// Each function would have am Integration
resource "aws_api_gateway_integration" "c8_test_resources_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.c8_rest_api_gateway.id
  resource_id             = aws_api_gateway_resource.c8_test_resource.id
  http_method             = aws_api_gateway_method.c8_test_resource_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.first_func.invoke_arn
}

// Define the permission to invole a function.
// All Resources needs this/
resource "aws_lambda_permission" "c8_first_func_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.first_func.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "${aws_api_gateway_rest_api.c8_rest_api_gateway.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "c8_rest_api_gateway_deployment" {
  rest_api_id = aws_api_gateway_rest_api.c8_rest_api_gateway.id

  #   depends_on = [aws_api_gateway_method.c8_test_resource_get, aws_api_gateway_integration.c8_test_resources_get_integration]

  triggers = {
    time = timestamp() // Trigger always. Todo: Make this trigger only when a change in resource happens
  }

  lifecycle {
    create_before_destroy = true
  }
}

// One per stage
resource "aws_api_gateway_stage" "c8_rest_api_gateway_stage" {
  deployment_id = aws_api_gateway_deployment.c8_rest_api_gateway_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.c8_rest_api_gateway.id
  stage_name    = "Dev"
}
