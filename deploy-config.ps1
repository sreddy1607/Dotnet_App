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

# Variables
$SiteName = "Apiservices-SBX"

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

Write-Host "Setting App Pool–level environment variables for Apiservices-SBX"

$envVars = @{
    VAULT_ADDRESS              = "https://np.secrets.cammis.medi-cal.ca.gov/v1/"
    VAULT_APPROLE_ROLE_ID      = "APPROLE_ROLE_ID"
    VAULT_APPROLE_SECRET_ID    = "APPROLE_SECRET_ID"
    VAULT_SECRET_PATH          = "kv-dev/data/us-west/dev-tar/tar-surgenet-service-secrets"
    VAULT_SECRET_PATH_LTAR     = "kv-dev/data/us-west/dev-tar/tar-ltar-service-secrets"
    VAULT_SECRET_PATH_IMGVWR   = "kv-dev/data/us-west/dev-tar/tar-image-viewer-service-secrets"
    VAULT_APPROLE_AUTH_PATH    = "auth/approle/login"

    SURGE_ENVNAME              = "SANDBOX"
    SURGE_RPM_ROOT             = "E:/inetpub/ApiServices/RPM/dhcs_dev/rpm_root"
    SURGE_RPM_ONLINE_KEY       = "/online"

    DD_LOGS_ENABLED            = "true"
}

Set-ItemProperty "IIS:\AppPools\Apiservices-SBX" `
  -Name processModel.environmentVariables `
  -Value $envVars

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
