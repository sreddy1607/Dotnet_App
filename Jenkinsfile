function Stop-Web-App-Pool($AppPoolName) {
     if ((Get-WebAppPoolState -Name $AppPoolName).Value -eq "Stopped") {
         Write-Host "$AppPoolName already stopped"
     }
     else {
         Write-Host "Shutting down $AppPoolName"
         Stop-WebAppPool -Name $AppPoolName
     }
 
     do {
         Start-Sleep -Seconds 1
     } until ((Get-WebAppPoolState -Name $AppPoolName).Value -eq "Stopped")
 }
 
 function Stop-Web-Site($WebsiteName) {
     if ((Get-WebsiteState -Name $WebsiteName).Value -eq "Stopped") {
         Write-Host "$WebsiteName already stopped"
     }
     else {
         Write-Host "Shutting down $WebsiteName"
         Stop-Website -Name $WebsiteName
     }
 
     do {
         Start-Sleep -Seconds 1
     } until ((Get-WebsiteState -Name $WebsiteName).Value -eq "Stopped")
 }
 
 # Ensure script runs in 64-bit mode
 if ($PSHOME -like "*SysWOW64*") {
     Write-Warning "Restarting script in 64-bit Windows PowerShell..."
     & (Join-Path ($PSHOME -replace "SysWOW64", "SysNative") powershell.exe) -NoProfile -File `
         (Join-Path $PSScriptRoot $MyInvocation.MyCommand) @args
     Exit $LastExitCode
 }


     Write-Warning "Hello from $PSHOME"
     Write-Warning "  (\SysWOW64\ = 32-bit mode, \System32\ = 64-bit mode)"
     Write-Warning "Original arguments (if any): $args"
     
     # Create Paths if they do not already exist
     Write-Host "Creating directories if they do not already exist"
     if (-Not (Test-Path -Path "E:\inetpub\ETarWeb")) {
          New-Item -ItemType "directory" -Path "E:\inetpub\ETarWeb"
     }
     
     if (-Not (Test-Path -Path "E:\IISLogs")) {
          New-Item -ItemType "directory" -Path "E:\IISLogs"
     }
     
     if (-Not (Test-Path -Path "E:\apps\ErrorLogs")) {
          New-Item -ItemType "directory" -Path "E:\apps\ErrorLogs"
     }


 
 # Setup Paths & Variables
 Import-Module -Name WebAdministration
 $Hostname = ""
 $SiteName = "ETarWeb-SBX"
 $SiteFolder = 'E:\inetpub\ETarWeb'
 $LoggingDir = 'E:\IISLogs'
 $AppPoolName = 'ETarWeb-SBX'
 $StagingDir = "E:\tar-etar-web-staging"
 $IISRootDir = "E:\inetpub"
 
 # Ensure Required Directories Exist
 Write-Host "Ensuring required directories exist..."
 @("$SiteFolder", "$LoggingDir", "E:\apps\ErrorLogs") | ForEach-Object {
     if (-Not (Test-Path -Path $_)) {
         New-Item -ItemType "directory" -Path $_ | Out-Null
     }
 }
 
 # Stop Site & App Pool if they exist
 Write-Host "Stopping '$SiteName'"
 Stop-Web-Site("$SiteName")
 
 Write-Host "Stopping Application Pool '$AppPoolName'"
 Stop-Web-App-Pool("$AppPoolName")
 
 # Remove Existing Site & App Pool
 Write-Host "Removing '$SiteName' from IIS"
 Remove-Website -Name "$SiteName" -ErrorAction SilentlyContinue
 
 Write-Host "Removing Application Pool '$AppPoolName'"
 Remove-WebAppPool -Name "$AppPoolName" -ErrorAction SilentlyContinue
 
 # Create New Application Pool
 Write-Host "Creating Application Pool '$AppPoolName'"
 New-WebAppPool -Name $AppPoolName

 # ================================
 # SET IIS RECYCLE TIME (12:15 AM PST → 08:15 UTC)
 # ================================

 $RecycleTime = "08:15"

 Write-Host "Clearing existing recycle schedule for '$AppPoolName'..."

 # Clear all existing schedule entries (works on all IIS versions)
 Clear-WebConfiguration -Filter "system.applicationHost/applicationPools/add[@name='$AppPoolName']/recycling/periodicRestart/schedule"

 Write-Host "Adding new recycle time $RecycleTime..."

 # Add the new specific recycle time
 Add-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST' `
  -filter "system.applicationHost/applicationPools/add[@name='$AppPoolName']/recycling/periodicRestart/schedule" `
  -name "." -value @{value=$RecycleTime}

Write-Host "Recycle schedule updated successfully to $RecycleTime UTC (12:15 AM PST)"
 
 Write-Host "Disabling regular time interval recycling for $AppPoolName"
 Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name recycling.periodicRestart.time -Value ([TimeSpan]::Zero)

 # Set Application Pool to "No Managed Code"
 Write-Host "Setting $AppPoolName to No Managed Code"
 Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name managedRuntimeVersion -Value ""

 Write-Host "Setting 'Load User Profile' to True for $AppPoolName"
 Set-ItemProperty "IIS:\AppPools\$AppPoolName" -Name processModel.loadUserProfile -Value $true
 
 # Create IIS Site (No Nested App)
 Write-Host "Creating IIS site '$SiteName' and assigning to App Pool '$AppPoolName'"
 New-WebSite -Name "$SiteName" -PhysicalPath "$SiteFolder" -ApplicationPool "$AppPoolName" -Force
 
 # Configure Site Bindings (No IP Address)
 Write-Host "Configuring web bindings for '$SiteName'"
 New-WebBinding -Name "$SiteName" -Port 8081 -HostHeader "$Hostname" -Protocol "http"
 
 # Configure Logging Directory
 Write-Host "Setting logging directory for '$SiteName'"
 Set-WebConfigurationProperty "/system.applicationHost/sites/siteDefaults" -Name logfile.directory -Value $LoggingDir 
 
 # Push the index.html file
 Write-Host "Deploying index.html"
 Remove-Item "$IISRootDir\index.html" -ErrorAction SilentlyContinue
 Copy-Item "$StagingDir\serverconfig\index.html" -Destination "$IISRootDir"
 (Get-Content "$IISRootDir\index.html") -replace "{server-hostname}", "$Hostname" | Set-Content "$IISRootDir\index.html"
 
 Write-Host "Installing/Updating Datadog Configuration"
 xcopy /s/y/e $StagingDir\serverconfig\datadog\conf.d\* C:\ProgramData\Datadog\conf.d\

 Write-Host "`nAdding ddagentuser to C:\ProgramData\Amazon\CodeDeploy\deployment-logs so Datadog can read the CodeDeploy log file`n"
 $Folder = 'C:\ProgramData\Amazon\CodeDeploy\deployment-logs'
 $ACL = Get-Acl $Folder
 $ACL_Rule = new-object System.Security.AccessControl.FileSystemAccessRule (
    'ddagentuser',
    'ReadAndExecute',
    ([System.Security.AccessControl.InheritanceFlags]::ContainerInherit -bor [System.Security.AccessControl.InheritanceFlags]::Objectinherit),
    [System.Security.AccessControl.PropagationFlags]::None,
    [System.Security.AccessControl.AccessControlType]::Allow
 )
 $ACL.SetAccessRule($ACL_Rule)
 Set-Acl -Path $Folder -AclObject $ACL

 Write-Host "Restarting the Datadog agent service"
 & 'C:\Program Files\Datadog\Datadog Agent\bin\agent.exe' restart-service
 
 # Restart Datadog Service
 Write-Host "Restarting Datadog agent service"
 & 'C:\Program Files\Datadog\Datadog Agent\bin\agent.exe' restart-service
 
 Write-Host "IIS Configuration Deployment Complete"
