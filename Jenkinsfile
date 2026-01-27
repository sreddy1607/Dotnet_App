version: 0.0
os: windows
files:
  - source: \scripts
    destination: D:\tar-surge-Api-staging\scripts
  - source: \serverconfig
    destination: D:\tar-surge-Api-staging\serverconfig
  - source: \environment
    destination: D:\tar-surge-Api-staging\environment
  - source: \surgeapi
    destination: D:\tar-surge-Api-staging\Apiservices  
file_exists_behavior: OVERWRITE    
hooks:
  BeforeInstall:
    - location: \before-install.bat
      timeout: 900
  AfterInstall:
    - location: \after-install.bat
      timeout: 900
