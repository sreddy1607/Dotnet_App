2026-08-14 18:38:18 LifecycleEvent - BeforeInstall
2026-08-14 18:38:18 Script - \before-install.bat
2026-08-14 18:38:18 [stdout]
2026-08-14 18:38:18 [stdout]C:\Windows\System32>REM Install Internet Information Server (IIS).  
2026-08-14 18:38:18 [stdout]
2026-08-14 18:38:18 [stdout]C:\Windows\System32>c:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command Import-Module -Name ServerManager 
2026-08-14 18:38:18 [stdout]
2026-08-14 18:38:18 [stdout]C:\Windows\System32>c:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command Install-WindowsFeature Web-Server 
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]Success Restart Needed Exit Code      Feature Result                               
2026-08-14 18:38:19 [stdout]------- -------------- ---------      --------------                               
2026-08-14 18:38:19 [stdout]True    No             NoChangeNeeded {}                                           
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]C:\Windows\System32>REM Backup existing configuration for IIS 
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]C:\Windows\System32>C:\Windows\System32\inetsrv\appcmd.exe add backup 
2026-08-14 18:38:19 [stdout]BACKUP object "20260814T183819" added
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]C:\Windows\System32>REM Ensure that api directory is empty before deploying files 
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]C:\Windows\System32>DEL /S /Q E:\tar-surge-Api-staging\Apiservices\* 
2026-08-14 18:38:19 [stderr]The system cannot find the path specified.
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]C:\Windows\System32>DEL /S /Q E:\tar-surge-Api-staging\serverconfig\* 
2026-08-14 18:38:19 [stderr]The system cannot find the path specified.
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]C:\Windows\System32>DEL /S /Q E:\tar-surge-Api-staging\environment\* 
2026-08-14 18:38:19 [stderr]The system cannot find the path specified.
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]C:\Windows\System32>DEL /S /Q E:\tar-surge-Api-staging\scripts\* 
2026-08-14 18:38:19 [stderr]The system cannot find the path specified.
2026-08-14 18:38:19 [stdout]
2026-08-14 18:38:19 [stdout]C:\Windows\System32>exit 0 
2026-08-14 18:38:21 LifecycleEvent - AfterInstall
2026-08-14 18:38:21 Script - \after-install.bat
2026-08-14 18:38:21 [stdout]"ENVIRONMENT will be deployed"
2026-08-14 18:38:22 [stdout]WARNING: Restarting this script under 64-bit Windows PowerShell.
2026-08-14 18:38:22 [stdout]WARNING: Hello from C:\Windows\System32\WindowsPowerShell\v1.0
2026-08-14 18:38:22 [stdout]WARNING:   (\SysWOW64\ = 32-bit mode, \System32\ = 64-bit mode)
2026-08-14 18:38:22 [stdout]WARNING: Original arguments (if any): 
2026-08-14 18:38:22 [stdout]Environment  : SANDBOX
2026-08-14 18:38:22 [stdout]IIS Site     : Apiservices-SBX
2026-08-14 18:38:22 [stdout]App Pool     : Apiservices-SBX
2026-08-14 18:38:22 [stdout]Vault Addr   : https://np.secrets.cammis.medi-cal.ca.gov/v1/
2026-08-14 18:38:22 [stdout]RPM Root     : E:/inetpub/ApiServices/RPM/dhcs_sbx/rpm_root
2026-08-14 18:38:22 [stdout]WebAdministration module loaded
2026-08-14 18:38:22 [stdout]appcmd.exe found at: C:\WINDOWS\system32\inetsrv\appcmd.exe
2026-08-14 18:38:22 [stdout]--- Stopping IIS site and app pool ---
2026-08-14 18:38:22 [stdout]Shutting down the  Apiservices-SBX
2026-08-14 18:38:22 [stdout]    Apiservices-SBX status:  Started
2026-08-14 18:38:22 [stdout]    Apiservices-SBX status:  Stopped
2026-08-14 18:38:23 [stdout]Apiservices-SBX  stopped successfully
2026-08-14 18:38:23 [stdout]Sleeping 5 seconds after site stop
2026-08-14 18:38:28 [stdout]Shutting down the  Apiservices-SBX
2026-08-14 18:38:28 [stdout]    Apiservices-SBX status:  Started
2026-08-14 18:38:28 [stdout]    Apiservices-SBX status:  Stopping
2026-08-14 18:38:29 [stdout]    Apiservices-SBX status:  Stopping
2026-08-14 18:38:30 [stdout]Apiservices-SBX  stopped successfully
2026-08-14 18:38:30 [stdout]Sleeping 5 seconds after app pool stop
2026-08-14 18:38:35 [stdout]App pool state after stop:
2026-08-14 18:38:35 [stdout]
2026-08-14 18:38:35 [stdout]--- Checking for lingering w3wp.exe worker processes ---
2026-08-14 18:38:35 [stdout]Killing w3wp.exe PID: 1428
2026-08-14 18:38:35 [stdout]Sleeping 3 seconds after killing worker processes
2026-08-14 18:38:38 [stdout]Worker processes cleared
2026-08-14 18:38:38 [stdout]--- Applying environment variables via appcmd.exe ---
2026-08-14 18:38:38 [stdout]Clearing existing environment variables...
2026-08-14 18:38:39 [stdout]ERROR ( message:Unknown attribute "environmentVariables".  Replace with -? for help. )
2026-08-14 18:38:39 [stdout]Existing environment variables cleared
2026-08-14 18:38:39 [stdout]ERROR ( message:New add object missing required attributes. Cannot add duplicate collection entry of type 'add' with unique key attribute 'name' set to 'SURGE_ENVNAME'
2026-08-14 18:38:39 [stdout]
2026-08-14 18:38:39 [stdout]. )
2026-08-14 18:38:39 [stdout]Name              State
2026-08-14 18:38:39 [stdout]----              -----
2026-08-14 18:38:39 [stdout]Apiservices-SBX Stopped
2026-08-14 18:38:39 [stderr]E:\tar-surge-Api-staging\environment\deploy-environment.ps1 : Failed to set environment variable: SURGE_ENVNAME (exit 
2026-08-14 18:38:39 [stderr]code 183)
2026-08-14 18:38:39 [stderr]    + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
2026-08-14 18:38:39 [stderr]    + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException,deploy-environment.ps1
2026-08-14 18:38:39 [stderr] 
