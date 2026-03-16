output "api_invoke_url" {
  description = "Invoke URL for the HTTP API."
  value       = aws_apigatewayv2_stage.default.invoke_url
}

output "lambda_function_name" {
  description = "Lambda function name."
  value       = aws_lambda_function.ticket_processor.function_name
}

output "dynamodb_table_name" {
  description = "DynamoDB table name."
  value       = aws_dynamodb_table.tickets.name
}

output "sns_topic_arn" {
  description = "SNS topic ARN."
  value       = aws_sns_topic.ticket_notifications.arn
}
