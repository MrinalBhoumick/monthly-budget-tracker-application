provider "aws" {
  region = var.region
}

# Configure the AWS provider to assume an IAM role
provider "aws" {
  region = var.region
  alias  = "assumed"
  assume_role {
    role_arn     = "arn:aws:iam::${var.account_id}:role/github-actions-deploy-role"
    session_name = "GitHubActionsSession"
  }
}
