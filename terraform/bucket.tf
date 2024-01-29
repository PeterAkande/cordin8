
// Random Name for the bucket
resource "random_pet" "cordin8_lambda_bucket_name" {
  prefix = "lambda-deploy"
  length = 2
}


resource "aws_s3_bucket" "cordin8_lambda_bucket" {
  bucket        = random_pet.cordin8_lambda_bucket_name.id // Name of the bucket
  force_destroy = true                                     // Destroy all objects of the bucket if the bucket is destroyed

  tags = {
    Name = "${var.tags_prefix}_bucket"
  }
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.cordin8_lambda_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
