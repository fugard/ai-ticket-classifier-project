resource "aws_dynamodb_table" "tickets" {
  name         = "${local.name_prefix}-tickets"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ticket_id"

  attribute {
    name = "ticket_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
