# fix_permissions.ps1
$path = ".\kasparro-key.pem"
$acl = Get-Acl $path
$acl.SetAccessRuleProtection($true, $false)
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($env:USERNAME,"Read","Allow")
$acl.AddAccessRule($rule)
Set-Acl $path $acl
Write-Host "Fixed permissions for $path"
