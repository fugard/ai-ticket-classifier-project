resource "aws_sns_topic" "ticket_notifications" {
  name = "${local.name_prefix}-ticket-notifications"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.ticket_notifications.arn
  protocol  = "email"
  endpoint  = var.notification_email
}
