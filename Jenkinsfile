2026-05-01 16:37:39 [stdout]C:\Windows\System32>DEL /S /Q E:\tar-surge-Api-staging\environment\* 
2026-05-01 16:37:39 [stdout]Deleted file - E:\tar-surge-Api-staging\environment\deploy-environment.ps1
2026-05-01 16:37:39 [stdout]
2026-05-01 16:37:39 [stdout]C:\Windows\System32>DEL /S /Q E:\tar-surge-Api-staging\scripts\* 
2026-05-01 16:37:39 [stdout]Deleted file - E:\tar-surge-Api-staging\scripts\deploy-files.ps1
2026-05-01 16:37:39 [stdout]
2026-05-01 16:37:39 [stdout]C:\Windows\System32>exit 0 
2026-05-01 16:37:40 LifecycleEvent - AfterInstall
2026-05-01 16:37:40 Script - \after-install.bat
2026-05-01 16:37:41 [stdout]"ENVIRONMENT will be deployed"
2026-05-01 16:37:41 [stdout]WARNING: Restarting this script under 64-bit Windows PowerShell.
2026-05-01 16:37:42 [stdout]WARNING: Hello from C:\Windows\System32\WindowsPowerShell\v1.0
2026-05-01 16:37:42 [stdout]WARNING:   (\SysWOW64\ = 32-bit mode, \System32\ = 64-bit mode)
2026-05-01 16:37:42 [stdout]WARNING: Original arguments (if any): 
2026-05-01 16:37:42 [stdout]Environment  : SANDBOX
2026-05-01 16:37:42 [stdout]IIS Site     : Apiservices-SBX
2026-05-01 16:37:42 [stdout]App Pool     : Apiservices-SBX
2026-05-01 16:37:42 [stdout]Vault Addr   : https://np.secrets.cammis.medi-cal.ca.gov/v1/
2026-05-01 16:37:42 [stdout]RPM Root     : E:/inetpub/ApiServices/RPM/dhcs_dev/rpm_root
2026-05-01 16:37:42 [stdout]WebAdministration module loaded
2026-05-01 16:37:42 [stdout]appcmd.exe found at: C:\WINDOWS\system32\inetsrv\appcmd.exe
2026-05-01 16:37:42 [stdout]--- Stopping IIS site and app pool ---
2026-05-01 16:37:42 [stdout]Shutting down the  Apiservices-SBX
2026-05-01 16:37:42 [stdout]    Apiservices-SBX status:  Started
2026-05-01 16:37:42 [stdout]    Apiservices-SBX status:  Stopped
2026-05-01 16:37:43 [stdout]Apiservices-SBX  stopped successfully
2026-05-01 16:37:43 [stdout]Sleeping 5 seconds after site stop
2026-05-01 16:37:48 [stdout]Shutting down the  Apiservices-SBX
2026-05-01 16:37:48 [stdout]    Apiservices-SBX status:  Started
2026-05-01 16:37:48 [stdout]    Apiservices-SBX status:  Stopping
2026-05-01 16:37:49 [stdout]    Apiservices-SBX status:  Stopping
2026-05-01 16:37:50 [stdout]    Apiservices-SBX status:  Stopping
2026-05-01 16:37:51 [stdout]Apiservices-SBX  stopped successfully
2026-05-01 16:37:51 [stdout]Sleeping 5 seconds after app pool stop
2026-05-01 16:37:56 [stdout]App pool state after stop:
2026-05-01 16:37:56 [stdout]
2026-05-01 16:37:56 [stdout]--- Checking for lingering w3wp.exe worker processes ---
2026-05-01 16:37:56 [stdout]Killing w3wp.exe PID: 11164
2026-05-01 16:37:56 [stdout]Sleeping 3 seconds after killing worker processes
2026-05-01 16:37:59 [stdout]Worker processes cleared
2026-05-01 16:37:59 [stdout]--- Applying environment variables via appcmd.exe ---
2026-05-01 16:37:59 [stdout]Clearing existing environment variables...
2026-05-01 16:37:59 [stdout]ERROR ( message:Unknown attribute "environmentVariables".  Replace with -? for help. )
2026-05-01 16:37:59 [stdout]Existing environment variables cleared
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: SURGE_ENVNAME = SANDBOX
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: VAULT_ADDRESS = https://np.secrets.cammis.medi-cal.ca.gov/v1/
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: VAULT_SECRET_PATH_IMGVWR = kv-dev/data/us-west/dev-tar/tar-image-viewer-service-secrets
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: SURGE_RPM_ROOT = E:/inetpub/ApiServices/RPM/dhcs_dev/rpm_root
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: VAULT_SECRET_PATH_LTAR = kv-dev/data/us-west/dev-tar/tar-ltar-service-secrets
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: DD_LOGS_ENABLED = true
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: VAULT_APPROLE_SECRET_ID = ****
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: VAULT_SECRET_PATH = kv-dev/data/us-west/dev-tar/tar-surgenet-service-secrets
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: VAULT_APPROLE_ROLE_ID = ****
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: VAULT_APPROLE_AUTH_PATH = auth/approle/login
2026-05-01 16:38:00 [stdout]Applied configuration changes to section "system.applicationHost/applicationPools" for "MACHINE/WEBROOT/APPHOST" at configuration commit path "MACHINE/WEBROOT/APPHOST"
2026-05-01 16:38:00 [stdout]    Set: SURGE_RPM_ONLINE_KEY = /online
2026-05-01 16:38:00 [stdout]All environment variables applied via appcmd.exe
2026-05-01 16:38:00 [stdout]--- Verifying environment variables ---
2026-05-01 16:38:00 [stdout]Name              State
2026-05-01 16:38:00 [stdout]----              -----
2026-05-01 16:38:00 [stdout]Apiservices-SBX Stopped
2026-05-01 16:38:00 [stdout]                       
2026-05-01 16:38:00 [stdout]                       
2026-05-01 16:38:00 [stdout]                       
2026-05-01 16:38:00 [stdout]                       
2026-05-01 16:38:00 [stdout]                       
2026-05-01 16:38:00 [stdout]                       
2026-05-01 16:38:00 [stdout]                       
2026-05-01 16:38:00 [stdout]--- Starting IIS app pool and site ---
2026-05-01 16:38:00 [stdout]Starting up  Apiservices-SBX
2026-05-01 16:38:00 [stdout]    Apiservices-SBX status:  Stopped
2026-05-01 16:38:00 [stdout]    Apiservices-SBX status:  Started
2026-05-01 16:38:01 [stdout]Apiservices-SBX  started successfully
2026-05-01 16:38:01 [stdout]Sleeping 5 seconds after app pool start
2026-05-01 16:38:06 [stdout]App pool state after start:
2026-05-01 16:38:06 [stdout]Apiservices-SBX Started
2026-05-01 16:38:06 [stdout]Starting up  Apiservices-SBX
2026-05-01 16:38:06 [stdout]    Apiservices-SBX status:  Stopped
2026-05-01 16:38:06 [stdout]    Apiservices-SBX status:  Started
2026-05-01 16:38:07 [stdout]Apiservices-SBX  started successfully
2026-05-01 16:38:07 [stdout]Sleeping 5 seconds after site start
2026-05-01 16:38:12 [stdout]Site state after start:
2026-05-01 16:38:12 [stdout]state                  
2026-05-01 16:38:12 [stdout]--- Final status check ---
2026-05-01 16:38:12 [stdout]App pool 'Apiservices-SBX' : Started
2026-05-01 16:38:12 [stdout]Site     'Apiservices-SBX'    : Started
2026-05-01 16:38:12 [stdout]Environment Deploy Complete
