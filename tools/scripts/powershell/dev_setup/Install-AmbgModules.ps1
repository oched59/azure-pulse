<#
.SYNOPSIS
Installs all current AMBG modules

.DESCRIPTION
Installs all current AMBG modules

.EXAMPLE
Install-AmbgModules
Just invoke this script to install all current AMBG modules

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

[CmdletBinding(
    SupportsShouldProcess,
    ConfirmImpact = 'High'
)]
param ()

<# ---------------- Begin main script ---------------- #>

BEGIN {
    try {
        #region Import Modules
        #endregion Import Modules

        #region Set Variables
        $ErrorActionPreference = 'Stop'
        
        if ($IsLinux -or $IsMacOS) {
            $standardModulePaths = $env:PSModulePath -split ':'
        }
        else {
            $standardModulePaths = $env:PSModulePath -split ';'
        }
        # Check if $standardModulePaths is empty or null
        if (-not $standardModulePaths) {
            Write-Error "No module paths found in environment variable PSModulePath."
        }
        $modulePathToInstallIn = $standardModulePaths[0]

        $pathOfModulesToInstall = "$PSScriptRoot\..\modules"

        #endregion Set Variables

        #region Set Functions
        #endregion Set Functions
    }
    catch {
        $PSCmdlet.ThrowTerminatingError($PSItem)
    }
}

PROCESS {
    try {
        #region Main Script               

        # Gets all folders in the modules folder
        $moduleFolders = Get-ChildItem -Path $pathOfModulesToInstall -Directory
        if (-not $moduleFolders) {
            Write-Warning "No modules found to install in '$pathOfModulesToInstall'."
        }
        else {
            Write-Host "`nAvailable modules are the following:" -ForegroundColor Blue
            $moduleFolders | ForEach-Object {
                Write-Host "  - $($PSItem.Name)" -ForegroundColor Green
            }
            Write-Host "`nModules will be installed in '$modulePathToInstallIn'"
    
            # For each module it checks if it is already installed and ask if it should be reinstalled. Then it copies the module to the module path.
            foreach ($moduleFolder in $moduleFolders) {
                $moduleName = $moduleFolder.Name
                $modulePath = "$pathOfModulesToInstall\$moduleName"
                $modulePathForInstallation = "$modulePathToInstallIn\$moduleName"
                if (Test-Path -Path $modulePathForInstallation) {
                    if ($PSCmdlet.ShouldContinue("Module '$moduleName' is already installed in '$modulePathForInstallation'.", "Remove it and install the newsest version?")) {
                        Remove-Item -Path $modulePathForInstallation -Recurse -Force
                        Copy-Item -Path $modulePath -Destination $modulePathForInstallation -Recurse -Force
                        Write-Host "Module '$moduleName' was removed and installed with newest version"
                    }
                    else {
                        Write-Warning "Module '$moduleName' is already installed in '$modulePathForInstallation' and will not be exchanged with newest version."
                    }
                }
                else {
                    Copy-Item -Path $modulePath -Destination $modulePathForInstallation -Recurse -Force
                    Write-Host "Module '$moduleName' was installed"
                }
            }
    
            Write-Host "`nAll modules were installed successfully" -ForegroundColor Green
        }

        # Asks if the user wants to replace its profile with the AMBG profile
        if ($PSCmdlet.ShouldContinue("Do you want to replace your PowerShell profile with the AMBG profile?", "This will overwrite your current profile.")) {
            $profilePath = $profile.CurrentUserAllHosts
            $profilePathFolder = $profilePath -split '\\profile.ps1' | Select-Object -First 1
            $profilePathBackup = "$profilePath.bak"
            if (Test-Path -Path $profilePath) {
                if (Test-Path -Path $profilePathBackup) {
                    Remove-Item -Path $profilePathBackup -Force
                }
                Rename-Item -Path $profilePath -NewName $profilePathBackup -Force
                Write-Host "Current profile was backed up to '$profilePathBackup'"
            }
            Copy-Item -Path "$PSScriptRoot\..\templates\ambgProfile.ps1" -Destination $profilePath -Force
            Copy-Item -Path "$PSScriptRoot\..\templates\ambgProfileConfig.json" -Destination "$profilePathFolder\ambgProfileConfig.json" -Force
            Write-Host "Profile was replaced with AMBG profile" -ForegroundColor Green
        }
        else {
            Write-Warning "Profile was not replaced with AMBG profile"
        }

        #endregion Main Script
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