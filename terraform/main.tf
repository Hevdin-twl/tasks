   terraform {
     required_providers {
       aws = {
         source  = "hashicorp/aws"
         version = "~> 4.0"
       }
     }
   }

   provider "aws" {
   region = "us-east-1"
   }

   resource "aws_s3_bucket" "my_bucket" {
     bucket = "twl-test2-public"
   }
   # Создаём экземпляр EC2
resource "aws_instance" "twl_instance" {
  ami                    = "ami-0c4e709339fa8521a"  # Ubuntu Server (arm64)
  instance_type          = "t4g.medium"  # ЦПУ Graviton t4g.medium архитектура arm64
  key_name            = "twl"
  vpc_security_group_ids = ["sg-04dc7c6ac9ce020ec"]
  subnet_id             = "subnet-09429d636719d6f62" 

  tags = {
    Name = "twlUbuntuT4gInstance"
  }
}
