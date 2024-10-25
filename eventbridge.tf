resource "aws_cloudwatch_event_rule" "main" {
  name        = "daily-spotify-wrakkd-trigger"
  description = "Triggers spotify-wrakkd every day at midnight"
  
  schedule_expression = "cron(0 0 * * ? *)"
}

resource "aws_cloudwatch_event_target" "main" {
  rule      = aws_cloudwatch_event_rule.main.name
  target_id = aws_lambda_function.main.id
  arn       = aws_lambda_function.main.arn
}
