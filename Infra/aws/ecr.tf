variable "ecr_repositories" {
  type    = list(string)
  default = [
    "user-service",
    "product-service",
    "order-service",
    "payment-service"
  ]
}

resource "aws_ecr_repository" "repos" {
  for_each = toset(var.ecr_repositories)

  name                 = each.value
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}