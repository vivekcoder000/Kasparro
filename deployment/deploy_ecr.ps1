# deploy_ecr.ps1
# Usage: .\deployment\deploy_ecr.ps1

$AWS_CMD = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"
$REGION = "ap-south-1"
$REPO_NAME = "antigravity-backend-etl"

Write-Host "Using AWS CLI at: $AWS_CMD"

# 1. Check Identity
Write-Host "Checking AWS Credentials..."
try {
    & $AWS_CMD sts get-caller-identity --region $REGION
    if ($LASTEXITCODE -ne 0) { throw "AWS Identity Check Failed" }
} catch {
    Write-Error "Could not authenticate with AWS. Please run 'aws configure' again and ensure keys are correct."
    exit 1
}

# 2. Login
Write-Host "Logging in to ECR ($REGION)..."
$Token = & $AWS_CMD ecr get-login-password --region $REGION
if (-not $Token) { exit 1 }

$ProxyEndpoint = & $AWS_CMD ecr get-authorization-token --region $REGION --query 'authorizationData[].proxyEndpoint' --output text
$Token | docker login --username AWS --password-stdin $ProxyEndpoint

# 3. Create Repo
Write-Host "Creating Repository '$REPO_NAME'..."
& $AWS_CMD ecr create-repository --repository-name $REPO_NAME --region $REGION --image-scanning-configuration scanOnPush=true
# Ignore error if already exists (stderr will show, but script continues)

# 4. Push
$ACCOUNT_ID = & $AWS_CMD sts get-caller-identity --query Account --output text --region $REGION
$ECR_URI = "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}"

Write-Host "Building Docker Image..."
docker build -t ${REPO_NAME}:latest .

Write-Host "Tagging Image ($ECR_URI)..."
docker tag ${REPO_NAME}:latest ${ECR_URI}:latest

Write-Host "Pushing to ECR..."
docker push ${ECR_URI}:latest

Write-Host "✅ Image Pushed Successfully: ${ECR_URI}:latest"
Write-Host "NEXT STEP: SSH into your EC2 instance and run:"
Write-Host "docker run -d -p 8000:8000 --env-file .env ${ECR_URI}:latest"
