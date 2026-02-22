resource "aws_db_instance" "postgres" {
  identifier              = "ecommerce-db"
  engine                  = "postgres"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  username                = "postgres"
  password                = "password123"
  publicly_accessible     = false

  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]

  skip_final_snapshot = true
}

resource "aws_db_subnet_group" "default" {
  name = "main"

  subnet_ids = [
    aws_subnet.subnet1.id,
    aws_subnet.subnet2.id
  ]
}