variable "handler" {
  default = "services.auth.main.lambda_handler"
}
variable "user_sign_up_handler" {
  default = "services.auth.signup.lambda_handler"
}

variable "user_sign_in_handler" {
  default = "services.auth.signin.lambda_handler"
}

variable "verification_codes_handler" {
  default = "services.auth.verification_codes.lambda_handler"
}

variable "verification_codes_confirm_handler" {
  default = "services.auth.verification_codes_confirm.lambda_handler"
}

variable "org_signup_handler" {
  default = "services.auth.org.signup.lambda_handler"
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

variable "lambda_layer_id" {
  default = ""
}

variable "python_runtime" {
  default = ""
}

variable "memory_size" {
  type    = number
  default = 128
}
