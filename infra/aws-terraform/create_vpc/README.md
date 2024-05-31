# Create VPC using Terraform

### Requirements

- Check AWS_ACCESS_KEY_ID , AWS_SECRET_ACCESS_KEY

https://registry.terraform.io/providers/hashicorp/aws/latest/docs?product_intent=terraform#environment-variables

- Install terraform
    - brew
        
        ```bash
        # Add Hashicorp/tap repo	
        brew tap hashicorp/tap
        
        # Install terraform
        brew install hashicorp/tap/terraform
        ```
        

### Arch

*Region* : ap-northeast-1

*AZ* : ap-northeast-2a, ap-northeast-2b

*Private Subnet* :  10.0.2.0/28, 10.0.4.0/28

*Public Subnet* :  10.0.1.0/28, 10.0.3.0/28

*Nat Gateway* , *IGW*: True



### How to run

```bash
# Install module, provider
terraform init

# Check Terraform plan
terraform plan

# Apply
terraform apply

# destory
terraform destroy
```
