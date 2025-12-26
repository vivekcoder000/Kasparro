# AWS Deployment Guide

Since the AWS CLI is not installed in this environment, I have generated scripts to help you deploy manually.

## 1. Prerequisites
- [Install AWS CLI](https://aws.amazon.com/cli/)
- Run `aws configure` and enter your credentials.

## 2. Push to ECR (Registry)
Run the helper script on your local machine:
```powershell
.\deployment\deploy_ecr.ps1
```
This will:
1.  Create an ECR repository named `antigravity-backend-etl`.
2.  Build your docker image.
3.  Push it to AWS.

## 3. Launch EC2 (Automated)
Run the automated launch script:
```powershell
.\deployment\launch_ec2.ps1
```
This script will:
1.  Create a Key Pair (`kasparro-key.pem`) -> **SAVE THIS FILE**.
2.  Create a Security Group (`kasparro-sg`) allowing ports 22 & 8000.
3.  Launch a t2.micro instance.
4.  Auto-install Docker and start your app.

## 4. Manual Launch (Alternative)
SSH into your instance:
```bash
ssh -i key.pem ec2-user@<PUBLIC_IP>
```

Run the setup commands (or copy `deployment/setup_ec2.sh`):
```bash
# Install Docker
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
exit
# Log back in
```

Run the app:
```bash
# Login
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com

# Run
docker run -d -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e API_KEY="your_api_key" \
  <YOUR_ECR_URI>:latest
```

## 5. Scheduled ETL
Add a cron job on EC2 to run the ETL hourly:
```bash
crontab -e
# Add:
0 * * * * docker exec $(docker ps -q) python run_etl.py
```
