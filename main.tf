terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.69.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename   = data.archive_file.main.output_path
  layer_name = "spotipy"
  compatible_architectures = ["arm64"]
  compatible_runtimes = ["python3.12"]
}

resource "null_resource" "main" {
  provisioner "local-exec" {
    command = <<EOT
      rm -rf ./package/python/
      mkdir -p ./package/python/
      pip install -r requirements.txt -t ./package/python/
    EOT
    working_dir = "${path.module}/lambda_layer"
  }

  triggers = {
    always_run = "${timestamp()}"
  }
}

data "archive_file" "main" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_layer/package"
  output_path = "${path.module}/lambda_layer.zip"

  depends_on = [null_resource.main]
}

variable "SPOTIFY_CLIENT_ID" {}
variable "SPOTIFY_CLIENT_SECRET" {}
variable "SPOTIFY_REDIRECT_URI" {}
