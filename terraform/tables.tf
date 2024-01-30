// The users table
resource "aws_dynamodb_table" "c8-users_table" {
  name           = "C8-USER-TABLE"
  hash_key       = "user_id"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  #  range_key = "" no need

  attribute {
    name = "user_id"
    type = "S"
  }
  #
  #  attribute {
  #    name = "name"
  #    type = "S"
  #  }
  #
  #  attribute {
  #    name = "email"
  #    type = "S"
  #  }
  #
  #  attribute {
  #    name = "phone"
  #    type = "S"
  #  }

#  ttl {
#    attribute_name = "TimeToExist"
#    enabled        = false
#  }

  tags = {
    Name        = "c8-user-table"
    Environment = "Dev"
  }
}

// The Organization table
resource "aws_dynamodb_table" "c8-org_table" {
  name           = "C8-ORG-TABLE"
  hash_key       = "org_id"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  #  range_key = "" no need

  attribute {
    name = "org_id"
    type = "S"
  }

  #  attribute {
  #    name = "name"
  #    type = "S"
  #  }
  #
  #  attribute {
  #    name = "email"
  #    type = "S"
  #  }


#  ttl {
#    attribute_name = "TimeToExist"
#    enabled        = false
#  }

  tags = {
    Name        = "c8-org-table"
    Environment = "Dev"
  }
}


// Departments Table
resource "aws_dynamodb_table" "c8-departments-table" {
  name           = "C8-DEPARTMENT-TABLE"
  hash_key       = "org_id"
  range_key      = "dept_id"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20


  attribute {
    name = "dept_id"
    type = "S"
  }
  attribute {
    name = "org_id" # The id of the organization
    type = "S"
  }

#  attribute {
#    name = "name"
#    type = "S"
#  }
#
#  attribute {
#    name = "team_lead" // This is the id of the team lead. The team lead would surely be a user
#    type = "S"
#  }
#
#
#  attribute {
#    name = "members"
#    type = "S"
#  }

#  ttl {
#    attribute_name = "TimeToExist"
#    enabled        = false
#  }

  tags = {
    Name        = "c8-dept-table"
    Environment = "Dev"
  }
}


// Tasks Table
resource "aws_dynamodb_table" "c8-tasks_table" {
  name           = "C8-TASKS-TABLE"
  hash_key       = "dept_id"
  range_key      = "task_id"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20

  attribute {
    name = "task_id"
    type = "S"
  }

  attribute {
    name = "dept_id"
    type = "S"
  }

#  attribute {
#    name = "title"
#    type = "S"
#  }
#
#  attribute {
#    name = "description"
#    type = "S"
#  }
#
#  attribute {
#    name = "team_lead"
#    type = "S"
#  }
#
#  attribute {
#    name = "date_assigned"
#    type = "S" // ISO8601 Formatted date
#  }
#
#  attribute {
#    name = "deadline"
#    type = "S"
#  }
#
#  attribute {
#    name = "assigned_to"
#    type = "S"
#  }
#
#  attribute {
#    name = "has_requested_completion"
#    type = "B"
#  }
#
#  attribute {
#    name = "verified_completion"
#    type = "B"
#  }
#
#  attribute {
#    name = "comments" // list of comments
#    type = "S"
#  }
#  ttl {
#    attribute_name = "TimeToExist"
#    enabled        = false
#  }

  tags = {
    Name        = "c8-tasks-table"
    Environment = "Dev"
  }
}