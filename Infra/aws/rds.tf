resource "aws_db_instance" "postgres" {
  identifier         = "ecommerce-db"
  engine             = "postgres"
  instance_class     = "db.t3.micro"
  allocated_storage  = 20
  username           = "postgres"
  password           = "password123"
  publicly_accessible = false
  vpc_security_group_ids = [module.vpc.default_security_group_id]
}