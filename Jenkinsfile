REM Install Internet Information Server (IIS). 
c:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command Import-Module -Name ServerManager
c:\Windows\Sysnative\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command Install-WindowsFeature Web-Server

REM Backup existing configuration for IIS
C:\Windows\System32\inetsrv\appcmd.exe add backup

REM Ensure that api directory is empty before deploying files
DEL /S /Q D:\tar-surge-Api-staging\Apiservices\*

DEL /S /Q D:\tar-surge-Api-staging\serverconfig\*
DEL /S /Q D:\tar-surge-Api-staging\environment\*
DEL /S /Q D:\tar-surge-Api-staging\scripts\*

exit 0
