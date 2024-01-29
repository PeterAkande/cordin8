variable "handler" {
  default = "modules.auth.main.lambda_handler"
}

// This is the Id of the rest API resource
variable "rest_api_id" {
  default = ""
}

variable "rest_api_parent_resource_id" {
  default = ""
}

variable "lambda_exec_role_arn" {
  default = ""
}

variable "s3_bucket_id" {
  default = ""
}

variable "s3_bucket_key" {
  default = ""
}

variable "archive_file_base_64_sha256" {
  default = ""
}

variable "rest_api_execution_arn" {
  default = ""
}