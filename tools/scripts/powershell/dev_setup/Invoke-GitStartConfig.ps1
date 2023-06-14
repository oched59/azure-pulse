<#
.SYNOPSIS
Setup basic Git configuration.

.DESCRIPTION
Setup basic Git configuration.

.PARAMETER FullName
The FullName of the user.

.PARAMETER Email
The email of the user.

.EXAMPLE
Invoke-GitStartConfig -FullName "Matthias Pfeiffer" Email "matthias.pfeiffer@accenture.com"
Describe one example

.NOTES
Author: Matthias Pfeiffer
Date:   2023-05-12
Version: 1.0

.LINK
https://github.com/AMBGASG/DATA.AI-Azure-OpenAI-Microsoft-Advisor-Bot/wiki

.COMPONENT
Requires PowerShell Core 7.0 or above
#>
#Requires -PSEdition Core
#Requires -Version 7.0

[CmdletBinding()]
param (
    [Parameter(
        Mandatory = $true,
        ValueFromPipeline = $true,
        ValueFromPipelineByPropertyName = $true,
        Position = 0
    )]
    [String]
    $FullName,
    [Parameter(
        Mandatory = $true,
        ValueFromPipeline = $true,
        ValueFromPipelineByPropertyName = $true,
        Position = 1
    )]
    [String]
    $Email
)

<# ---------------- Begin main script ---------------- #>

BEGIN {
    try {
        # Check if git is installed
        if (-not (Get-Command -Name git -ErrorAction SilentlyContinue)) {
            throw "Git is not installed. Please install Git and try again."
        }
    }
    catch {
        $PSCmdlet.ThrowTerminatingError($PSItem)
    }
}

PROCESS {
    try {
        git config --global user.name $FullName
        git config --global user.email $Email
        git config --global credential.https://dev.azure.com.useHttpPath true
        git config --global credential.azreposCredentialType oauth
        
        if ($IsLinux -or $IsMacOS) {
            # Find the "git-credential-manager.exe" within the windows git installation and set the path to it
            $gitCredentialManager = Get-ChildItem -Path $env:ProgramFiles -Recurse -Filter "git-credential-manager.exe" | Select-Object -First 1
            git config --global credential.helper '$gitCredentialManager'
        }
        else {
            git config --global credential.helper manager
        }
        Write-Host "Git configuration:" -ForegroundColor Green
        git config --global --list
    }
    catch {
        $PSCmdlet.ThrowTerminatingError($PSItem)
    }
}

END {
    try {
        #region Cleanup
        #endregion Cleanup
    }
    catch {
        $PSCmdlet.ThrowTerminatingError($PSItem)
    }
}