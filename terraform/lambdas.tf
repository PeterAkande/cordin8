// This would contain all the lambdas


resource "aws_lambda_layer_version" "c8-lambda-layer" {
  filename   = "../build/python.zip"
  layer_name = "c8-python-lambda-layer"

  compatible_runtimes      = ["python3.8", "python3.7", "python3.9"]
  compatible_architectures = ["x86_64", "arm64"]
}
// Create the required roles first.
resource "aws_iam_role" "c8_lambda_exec_role" {
  name = "c8-lambda-exec-role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Sid       = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  managed_policy_arns = [
    aws_iam_policy.invoke-cognito-policy.arn, aws_iam_policy.aws_assumed_role.arn, aws_iam_policy.dynamo-db-policy.arn
  ]
}

#resource "aws_iam_role_policy_attachment" "lambda_policy" {
#  role       = aws_iam_role.c8_lambda_exec_role.name
#  // This makes things easy, using this predefined AWS Managed Role.
#  // We can actually create aws_iam_policy resource and attach it but ist not needed
#  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
#}


resource "aws_iam_policy" "invoke-cognito-policy" {
  name = "invoke-cognito-from-lambda"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "Stmt1706752366251",
        "Action" : "cognito-idp:*",
        "Effect" : "Allow",
        "Resource" : aws_cognito_user_pool.c8-user-pool.arn
      }
    ]
  })
}

resource "aws_iam_policy" "dynamo-db-policy" {
  name = "invoke-dynamodb-from-lambda"

  policy = jsonencode( {
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "Stmt1706777921387",
        "Action" : "dynamodb:*",
        "Effect" : "Allow",
        "Resource" : "*"
      }
    ]
  })
}


resource "aws_iam_policy" "aws_assumed_role" {
  // This is used because you cant use managed_policy_arns with aws_iam_role_policy_attachment
  name = "aws-assumed-role"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "*"
      }
    ]
  })
}


// Define the lambdas
resource "aws_lambda_function" "first_func" {
  function_name = "Cordin8-First"
  role          = aws_iam_role.c8_lambda_exec_role.arn

  s3_bucket = aws_s3_bucket.cordin8_lambda_bucket.id
  s3_key    = aws_s3_object.c8_lambda_code.key

  layers = [aws_lambda_layer_version.c8-lambda-layer.arn]

  runtime = "python3.8"
  handler = "main.lambda_handler"

  source_code_hash = data.archive_file.c8_lambda_code_zip.output_base64sha256

  memory_size = var.memory_size

}
