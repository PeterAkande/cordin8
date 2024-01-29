// This would handle archiving the file and depliying em

data "archive_file" "c8_lambda_code_zip" {
  type = "zip"

  source_dir  = "../src"
  output_path = "../build/build.zip"
}

resource "aws_s3_object" "c8_lambda_code" {
  key    = "build.zip"
  bucket = aws_s3_bucket.cordin8_lambda_bucket.id

  source = data.archive_file.c8_lambda_code_zip.output_path
  etag   = filemd5(data.archive_file.c8_lambda_code_zip.output_path)
}
