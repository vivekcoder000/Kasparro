# launch_ec2.ps1
# Usage: .\deployment\launch_ec2.ps1

$ErrorActionPreference = "Stop"
$AWS_CMD = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"
$REGION = "ap-south-1"
$AMI_ID = "ami-0f5ee92e2d63afc18" # Ubuntu 22.04 LTS (ap-south-1)
$INSTANCE_TYPE = "t2.micro"
$KEY_NAME = "kasparro-key"
$SG_NAME = "kasparro-sg"
$IMAGE_URI = "337964479379.dkr.ecr.ap-south-1.amazonaws.com/antigravity-backend-etl:latest"

Write-Host "🚀 Launching Kasparro Backend on AWS ($REGION)..."

# 1. Create Key Pair
Write-Host "Checking Key Pair '$KEY_NAME'..."
try {
    & $AWS_CMD ec2 describe-key-pairs --key-names $KEY_NAME --region $REGION --no-cli-pager | Out-Null
    Write-Host "✅ Key Pair exists."
} catch {
    Write-Host "Creating Key Pair..."
    $KeyMaterial = & $AWS_CMD ec2 create-key-pair --key-name $KEY_NAME --query "KeyMaterial" --output text --region $REGION --no-cli-pager
    $KeyMaterial | Out-File -Encoding ascii -FilePath "${KEY_NAME}.pem"
    Write-Host "✅ Created '${KEY_NAME}.pem'. KEEP THIS SAFE!"
}

# 2. Create Security Group
Write-Host "Checking Security Group '$SG_NAME'..."
try {
    $SG_ID = & $AWS_CMD ec2 describe-security-groups --group-names $SG_NAME --query "SecurityGroups[0].GroupId" --output text --region $REGION --no-cli-pager 2>$null
    Write-Host "✅ Security Group exists ($SG_ID)."
} catch {
    Write-Host "Creating Security Group..."
    $VPC_ID = & $AWS_CMD ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text --region $REGION --no-cli-pager
    $SG_ID = & $AWS_CMD ec2 create-security-group --group-name $SG_NAME --description "Kasparro SG" --vpc-id $VPC_ID --output text --region $REGION --no-cli-pager
    
    # Authorize Ports
    & $AWS_CMD ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0 --region $REGION --no-cli-pager
    & $AWS_CMD ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 8000 --cidr 0.0.0.0/0 --region $REGION --no-cli-pager
    Write-Host "✅ Created Security Group ($SG_ID) with ports 22, 8000 open."
}

# 3. Create IAM Role (for ECR Pull)
$ROLE_NAME = "KasparroECRRole"
$PROFILE_NAME = "KasparroECRProfile"

Write-Host "Configuring IAM Role '$ROLE_NAME'..."
& $AWS_CMD iam get-role --role-name $ROLE_NAME --no-cli-pager
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating IAM Role..."
    $TrustPolicy = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}]}' | Out-File -Encoding ascii -FilePath "trust_policy.json"
    & $AWS_CMD iam create-role --role-name $ROLE_NAME --assume-role-policy-document file://trust_policy.json --no-cli-pager | Out-Null
    & $AWS_CMD iam attach-role-policy --role-name $ROLE_NAME --policy-arn "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly" --no-cli-pager
    Remove-Item "trust_policy.json"
    Write-Host "✅ Created IAM Role."
} else {
    Write-Host "✅ IAM Role exists."
}

Write-Host "Configuring Instance Profile '$PROFILE_NAME'..."
& $AWS_CMD iam get-instance-profile --instance-profile-name $PROFILE_NAME --no-cli-pager
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating Instance Profile..."
    & $AWS_CMD iam create-instance-profile --instance-profile-name $PROFILE_NAME --no-cli-pager | Out-Null
    & $AWS_CMD iam add-role-to-instance-profile --instance-profile-name $PROFILE_NAME --role-name $ROLE_NAME --no-cli-pager
    Write-Host "✅ Created Instance Profile. Waiting for propagation..."
    Start-Sleep -Seconds 10
} else {
    Write-Host "✅ Instance Profile exists."
}

# 4. User Data Script (Auto-install & Run)
$UserData = @"
#!/bin/bash
apt-get update -y
apt-get install -y docker.io awscli
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

# Login to ECR (Using Instance Profile)
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin 337964479379.dkr.ecr.ap-south-1.amazonaws.com

# Create .env
echo "DATABASE_URL=postgresql://user:pass@db:5432/dbname" > .env
echo "API_KEY=testkey" >> .env

# Run Container
docker run -d -p 8000:8000 --env-file .env --restart always $IMAGE_URI
"@
$UserDataEncoded = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($UserData))

# 5. Launch Instance
Write-Host "Launching EC2 Instance..."
$InstanceID = & $AWS_CMD ec2 run-instances `
    --image-id $AMI_ID `
    --count 1 `
    --instance-type $INSTANCE_TYPE `
    --key-name $KEY_NAME `
    --security-group-ids $SG_ID `
    --user-data $UserDataEncoded `
    --query "Instances[0].InstanceId" `
    --output text `
    --region $REGION `
    --iam-instance-profile Name=$PROFILE_NAME `
    --no-cli-pager 

Write-Host "✅ Instance Launched: $InstanceID"
Write-Host "Waiting for Public IP..."
Start-Sleep -Seconds 10
$PublicIP = & $AWS_CMD ec2 describe-instances --instance-ids $InstanceID --query "Reservations[0].Instances[0].PublicIpAddress" --output text --region $REGION --no-cli-pager

Write-Host "`n🎉 DEPLOYMENT COMPLETE!"
Write-Host "Instance IP: $PublicIP"
Write-Host "API Health: http://${PublicIP}:8000/health"
Write-Host "SSH Command: ssh -i ${KEY_NAME}.pem ec2-user@${PublicIP}"
Write-Host "Note: It may take 2-3 minutes for the instance to initialize."
