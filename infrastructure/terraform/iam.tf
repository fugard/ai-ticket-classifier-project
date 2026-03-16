data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "${local.name_prefix}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    sid     = "CloudWatchLogs"
    effect  = "Allow"
    actions = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:*:*:*"]
  }

  statement {
    sid     = "DynamoDBAccess"
    effect  = "Allow"
    actions = ["dynamodb:PutItem"]
    resources = [aws_dynamodb_table.tickets.arn]
  }

  statement {
    sid     = "SNSPublish"
    effect  = "Allow"
    actions = ["sns:Publish"]
    resources = [aws_sns_topic.ticket_notifications.arn]
  }
}

data "aws_iam_policy_document" "bedrock_policy" {
  statement {
    sid     = "BedrockInvoke"
    effect  = "Allow"
    actions = ["bedrock:InvokeModel"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "lambda_policy" {
  name   = "${local.name_prefix}-lambda-inline-policy"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.lambda_policy.json
}

resource "aws_iam_role_policy" "bedrock_policy" {
  count  = var.bedrock_model_id == "" ? 0 : 1
  name   = "${local.name_prefix}-bedrock-inline-policy"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.bedrock_policy.json
}