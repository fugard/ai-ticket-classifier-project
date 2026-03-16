data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../lambda/src"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "ticket_processor" {
  function_name    = "${local.name_prefix}-processor"
  role             = aws_iam_role.lambda_role.arn
  handler          = "app.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory_size

  environment {
    variables = {
      TICKETS_TABLE           = aws_dynamodb_table.tickets.name
      NOTIFICATIONS_TOPIC_ARN = aws_sns_topic.ticket_notifications.arn
      BEDROCK_MODEL_ID        = var.bedrock_model_id
      AWS_REGION              = var.aws_region
      LOG_LEVEL               = "INFO"
    }
  }
}
