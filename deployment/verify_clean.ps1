# verify_clean.ps1
$ErrorActionPreference = "Stop"

$AWS_CMD = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"
$REGION = "ap-south-1"

Write-Host "Finding Kasparro Instance..."

try {
    $PublicIP = & $AWS_CMD ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].PublicIpAddress" --output text --region $REGION --no-cli-pager
    if ($null -eq $PublicIP) {
        throw "AWS CLI returned empty result (Instance might not be running yet)"
    }
    $PublicIP = $PublicIP.Trim()
} catch {
    Write-Host "FATAL ERROR: Could not get instances." -ForegroundColor Red
    Write-Host "Error Message: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

if (-not $PublicIP) {
    Write-Host "No running instances found! (Is it still booting?)"
    exit 1
}

Write-Host "Found Public IP: $PublicIP"
$BaseURL = "http://${PublicIP}:8000"

# 1. Health
Write-Host "TEST 1: /health"
try {
    $h = Invoke-RestMethod -Uri "${BaseURL}/health" -TimeoutSec 5
    Write-Host "Status: $($h.status)"
    Write-Host "DB: $($h.database)"
    Write-Host "ETL: $($h.etl_last_run)"
} catch {
    Write-Host "Failed to connect (Instance might be initializing... wait 60s)"
}

# 2. Stats
Write-Host "TEST 2: /stats"
try {
    $s = Invoke-RestMethod -Uri "${BaseURL}/stats" -TimeoutSec 5
    Write-Host "Total Runs: $($s.total_runs)"
    Write-Host "Last Status: $($s.last_run_status)"
} catch {
    Write-Host "Failed"
}

# 3. Data
Write-Host "TEST 3: /data"
try {
    $d = Invoke-RestMethod -Uri "${BaseURL}/data" -TimeoutSec 5
    Write-Host "Records Returned: $($d.metadata.total_records)"
} catch {
    Write-Host "Failed"
}

Write-Host "SMOKE TEST COMPLETE"
