# Set environment variables for Vault access
Write-Host "Setting environment variables for Vault access"
[Environment]::SetEnvironmentVariable("VAULT_ADDRESS", "{VAULT_ADDR}", "Machine")
[Environment]::SetEnvironmentVariable("VAULT_APPROLE_ROLE_ID", "{APPROLE_ROLE_ID}", "Machine")
[Environment]::SetEnvironmentVariable("VAULT_APPROLE_SECRET_ID", "{APPROLE_SECRET_ID}", "Machine")
[Environment]::SetEnvironmentVariable("VAULT_SECRET_PATH", "{VAULT_SECRET_PATH}", "Machine")
[Environment]::SetEnvironmentVariable("VAULT_SECRET_PATH_LTAR", "{VAULT_SECRET_PATH_LTAR}", "Machine")
[Environment]::SetEnvironmentVariable("VAULT_SECRET_PATH_IMGVWR", "{VAULT_SECRET_PATH_IMGVWR}", "Machine")
[Environment]::SetEnvironmentVariable("VAULT_APPROLE_AUTH_PATH", "{VAULT_APPROLE_AUTH_PATH}", "Machine")

[Environment]::SetEnvironmentVariable("SURGE_ENVNAME", "{SURGE_ENVNAME}", "Machine")
[Environment]::SetEnvironmentVariable("SURGE_RPM_ROOT", "{SURGE_RPM_ROOT}", "Machine")
[Environment]::SetEnvironmentVariable("SURGE_RPM_ONLINE_KEY", "/online", "Machine")


Write-Host "Setting environment to enable Datadog file logging"
[Environment]::SetEnvironmentVariable("DD_LOGS_ENABLED", "true", "Machine")
