module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  name               = "e-commerce-cluster"
  kubernetes_version = "1.29"

  # Keep public endpoint for lab (avoids NAT complexity)
  endpoint_public_access = true

  addons = {
    coredns                = {}
    eks-pod-identity-agent = {
      before_compute = true
    }
    kube-proxy             = {}
    vpc-cni                = {
      before_compute = true
    }
  }
  
  # Enable cluster creator admin
  enable_cluster_creator_admin_permissions = true

  vpc_id     = aws_vpc.main.id
   subnet_ids = [
    aws_subnet.subnet1.id,
    aws_subnet.subnet2.id
  ]



  # Minimal managed node group
  eks_managed_node_groups = {
    small = {
      instance_types = ["t3.small"]  
      ami_type       = "AL2023_x86_64_STANDARD"

      min_size     = 1
      max_size     = 1
      desired_size = 1

      disk_size = 20
    }
  }
}

