# Functions needed to ensure the Website and AppPools are fully stopped before continuing
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

  & (Join-Path ($PSHOME -replace "SysWOW64", "SysNative") powershell.exe) -NoProfile -File `
    (Join-Path $PSScriptRoot $MyInvocation.MyCommand) @args

  # Exit 32-bit script.

  Exit $LastExitCode
}

# Was restart successful?
Write-Warning "Hello from $PSHOME"
Write-Warning "  (\SysWOW64\ = 32-bit mode, \System32\ = 64-bit mode)"
Write-Warning "Original arguments (if any): $args"

# Variables
$SiteName = "Apiservices"
$SiteFolder = 'D:\inetpub'
$StagingFolder = 'D:\tar-surge-Api-staging'

Import-Module -Name WebAdministration

# Stop Site and App Pools
Write-Host "Stopping $SiteName"
Stop-Web-Site("$SiteName")
Write-Host "Stop status: $?"

Write-Host "Stopping Application Pools"
Stop-Web-App-Pool("Apiservices")


Write-Host "Status of Application Pools"
Get-IISAppPool -Name Apiservices

# Remove Existing and Copy Deployed Files for Apiservices if app deployed
if (Test-Path $StagingFolder\Apiservices\*) {
  Write-Host "Removing existing Apiservices files from $SiteFolder\Apiservices"
  Remove-Item -Recurse $SiteFolder\Apiservices\*
  Write-Host "Removal status for Apiservices files: $?"
  Write-Host "Copying newly deployed Apiservices files to $SiteName\Apiservices"
  xcopy /s/y/e  $StagingFolder\Apiservices $SiteFolder\Apiservices
  Write-Host "Copy status for Apiservices files: $?"
}

# Start Site and App Pools
Write-Host "Starting Application Pools"
Start-WebAppPool -Name "Apiservices"

Write-Host "Status of Application Pools"
Get-IISAppPool -Name Apiservices

Write-Host "Starting $SiteName"
Start-Website -name "$SiteName"
Write-Host "Start status: $?"

Write-Host "Deploy Complete"
