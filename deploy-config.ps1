function Stop-Web-App-Pool($AppPoolName) {
  if ( (Get-WebAppPoolState -Name $AppPoolName).Value -eq "Stopped" ) {
      Write-Host $AppPoolName " already stopped"
  }
  else {
      Write-Host "Shutting down the " $AppPoolName
      Write-Host "    $AppPoolName status: " (Get-WebAppPoolState $AppPoolName).Value
      Stop-WebAppPool -Name $AppPoolName 
  }

  do {
      Write-Host "    $AppPoolName status: " (Get-WebAppPoolState $AppPoolName).Value
      Start-Sleep -Seconds 1
  }
  until ( (Get-WebAppPoolState -Name $AppPoolName).Value -eq "Stopped" )
}

function Stop-Web-Site($WebsiteName) {
  if ( (Get-WebsiteState -Name $WebsiteName).Value -eq "Stopped" ) {
      Write-Host $WebsiteName " already stopped"
  }
  else {
      Write-Host "Shutting down the " $WebsiteName
      Write-Host "    $WebsiteName status: " (Get-WebsiteState $WebsiteName).Value
      Stop-Website -Name $WebsiteName 
  }

  do {
      Write-Host "    $WebsiteName status: " (Get-WebsiteState $WebsiteName).Value
      Start-Sleep -Seconds 1
  }
  until ( (Get-WebsiteState -Name $WebsiteName).Value -eq "Stopped" )
}

# This is needed because AWS CodeDeploy Agent runs in 32-bit mode,
# script below needs to run in 64-bit mode.

# Are you running in 32-bit mode?
#   (\SysWOW64\ = 32-bit mode)

if ($PSHOME -like "*SysWOW64*")
{
  Write-Warning "Restarting this script under 64-bit Windows PowerShell."

  # Restart this script under 64-bit Windows PowerShell.
  #   (\SysNative\ redirects to \System32\ for 64-bit mode)

  & (Join-Path ($PSHOME -replace "SysWOW64", "SysNative") powershell.exe) -File `
    (Join-Path $PSScriptRoot $MyInvocation.MyCommand) @args

  # Exit 32-bit script.

  Exit $LastExitCode
}

# Was restart successful?
Write-Warning "Hello from $PSHOME"
Write-Warning "  (\SysWOW64\ = 32-bit mode, \System32\ = 64-bit mode)"
Write-Warning "Original arguments (if any): $args"

Import-Module WebAdministration

# Variables
$SiteName = "Apiservices-SBX"
$AppPoolName = "Apiservices-SBX"

# Stop Site and App Pools
Write-Host "Stopping $SiteName"
Stop-Web-Site("$SiteName")
Write-Host "Stop status: $?"

Write-Host "Sleeping for 5 seconds for web site to stop"
Start-Sleep -Seconds 5

Write-Host "Stopping Application Pools"
Stop-Web-App-Pool("Apiservices-SBX")


Write-Host "Sleeping for 5 seconds for app pools to stop"
Start-Sleep -Seconds 5

Write-Host "Status of Application Pools"
Get-IISAppPool -Name Apiservices-SBX

Write-Host "Setting App Pool–level environment variables for $AppPoolName"

# Vault variables
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.VAULT_ADDRESS -Value "https://np.secrets.cammis.medi-cal.ca.gov/v1/"
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.VAULT_APPROLE_ROLE_ID -Value "APPROLE_ROLE_ID"
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.VAULT_APPROLE_SECRET_ID -Value "APPROLE_SECRET_ID"
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.VAULT_SECRET_PATH -Value "kv-dev/data/us-west/dev-tar/tar-surgenet-service-secrets"
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.VAULT_SECRET_PATH_LTAR -Value "kv-dev/data/us-west/dev-tar/tar-ltar-service-secrets"
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.VAULT_SECRET_PATH_IMGVWR -Value "kv-dev/data/us-west/dev-tar/tar-image-viewer-service-secrets"
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.VAULT_APPROLE_AUTH_PATH -Value "auth/approle/login"

# Surge variables
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.SURGE_ENVNAME -Value "SANDBOX"
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.SURGE_RPM_ROOT -Value "E:/inetpub/ApiServices/RPM/dhcs_dev/rpm_root"
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.SURGE_RPM_ONLINE_KEY -Value "/online"

# Datadog
Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.environmentVariables.DD_LOGS_ENABLED -Value "true"

Write-Host "App Pool environment variables applied successfully"

# Start Site and App Pools
Write-Host "Starting Application Pools"
Start-WebAppPool -Name "Apiservices-SBX"


Write-Host "Status of Application Pools"
Get-IISAppPool -Name Apiservices-SBX

Write-Host "Starting $SiteName"
Start-Website -name "$SiteName"
Write-Host "Start status: $?"

Write-Host "Environment Deploy Complete"
