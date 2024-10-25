resource "aws_lambda_function" "main" {
  function_name = "spotify-wrakkd"
  handler       = "main.lambda_handler"
  runtime       = "python3.12"
  role          = aws_iam_role.main.arn
  architectures = ["arm64"]
  filename      = data.archive_file.grass.output_path

  timeout = 30
  environment {
    variables = {
      SPOTIFY_CLIENT_ID = var.SPOTIFY_CLIENT_ID
      SPOTIFY_CLIENT_SECRET = var.SPOTIFY_CLIENT_SECRET
      SPOTIFY_REDIRECT_URI = var.SPOTIFY_REDIRECT_URI

    }
  }
  source_code_hash = "${data.archive_file.grass.output_base64sha256}"
  layers = [aws_lambda_layer_version.lambda_layer.arn]
}

resource "aws_lambda_permission" "main" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.main.arn
}

data "archive_file" "grass" {
  type        = "zip"
  source_dir  = "lambda"
  output_path = "grass.zip"
}
