resource "aws_cognito_user_pool" "c8-user-pool" {
  name = "C8-USER-POOL"

  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_subject        = "Confirm your account with Cordin8"
    email_message        = "Your confirmation code is {####}"
  }

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true

  }

  // Lets define the schemas
  schema {
    attribute_data_type = "String"
    name                = "email"
    required            = true
    mutable             = false
    string_attribute_constraints {
      min_length = 1
      max_length = 2048
    }
  }
  schema {
    attribute_data_type = "String"
    name                = "name"
    required            = true
    mutable             = false
    string_attribute_constraints {
      min_length = 1
      max_length = 2048
    }
  }

  schema {
    attribute_data_type = "String"
    name                = "profile_type"
#    required            = true
    mutable             = false
    string_attribute_constraints {
      min_length = 1
      max_length = 2048
    }
  }
  tags = {
    Name = "C8"
  }

}

// Define the user pool client
resource "aws_cognito_user_pool_client" "client" {
  name = "C8-COGNITO-CLIENT"

  user_pool_id                  = aws_cognito_user_pool.c8-user-pool.id
  generate_secret               = true
  prevent_user_existence_errors = "ENABLED"

  token_validity_units {
    access_token  = "days"
    refresh_token = "days"
  }

  access_token_validity  = 1 # 1 DAY
  refresh_token_validity = 90 # 60 Days

  explicit_auth_flows = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]

}