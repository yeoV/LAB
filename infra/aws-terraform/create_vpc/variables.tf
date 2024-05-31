variable "region" {
  description = "Aws Region name"
  type = string
  default = "ap-northeast-2"
}

variable "azs" {
  description = "Availability zones"
  type = list(string)
  default = ["ap-northeast-2a", "ap-northeast-2b"]
}

variable "public_subnet_cidrs" {
  type = list(string)
  description = "Public Subnet CIDR values"
  default = [ "10.0.1.0/28", "10.0.3.0/28"]
}

variable "private_subnet_cidrs" {
  type = list(string)
  description = "Public Subnet CIDR values"
  default = [ "10.0.2.0/28", "10.0.4.0/28"]
}