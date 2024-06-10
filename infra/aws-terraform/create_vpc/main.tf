provider "aws" {
  region = var.region
}

locals {
  cluster_name = "tf-eks-cluster"
}


module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "tf-vpc"
  cidr = "10.0.0.0/20"

  azs             = var.azs
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_vpn_gateway = false

  tags = {
    Terraform = "true"
    Environment = "dev"
  }

}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.5"

  cluster_name  = local.cluster_name
  cluster_version = "1.30"
  
  cluster_endpoint_public_access  = true

  # VPC Config
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_group_defaults = {
    ami_type = "AL2_x86_64"
  }

  eks_managed_node_groups = {
    one = {
      desired_capacity = 1
      max_capacity     = 2
      min_capacity     = 1

      instance_type = ["t3.small"]
    }
  }
}