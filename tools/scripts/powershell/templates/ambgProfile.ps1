#Requires -Version 7

$global:profile_initialized = $false

function prompt {

    function Initialize-Profile {
        # ---------------------------------------  Display welcome message ---------------------------------------
        $ME = whoami.exe
        Write-Host "Hello $ME! Welcome to the AMBG PowerShell profile" -ForegroundColor Green
        Write-Host "Initializing profile..." -ForegroundColor Yellow
        # Display an asci logo with the letters A M B G
        Write-Host "        _   _   _   _  " -ForegroundColor DarkBlue
        Write-Host "       / \ / \ / \ / \ " -ForegroundColor DarkBlue
        Write-Host "      ( A | M | B | G )" -ForegroundColor DarkBlue
        Write-Host "       \_/ \_/ \_/ \_/ " -ForegroundColor DarkBlue
        Write-Host "                       " -ForegroundColor DarkBlue
        
        # ---------------------------------------  Install modules ---------------------------------------
        
        $profilePathFolder = $profile.CurrentUserAllHosts -split '\\profile.ps1' | Select-Object -First 1
        $modulesConfigPath = "$profilePathFolder\ambgProfileConfig.json"
        $lastUpdateCheckPath = "$profilePathFolder\ambgProfileLastUpdateCheck.check"
        $userInput = $null

        if (-not (Test-Path -Path $lastUpdateCheckPath)) {
            New-Item -Path $lastUpdateCheckPath -ItemType File -Force
            $userInput = "A"
        }
        else {
            $lastUpdate = (Get-Item -Path $modulesConfigPath).LastWriteTime
            if ($lastUpdate -lt (Get-Date).AddDays(-7)) {
                Write-Host "Modules were last updated on '$lastUpdate'. Do you want to update them?", "The modules will be updated and you can choose for each module if it should be updated."
                $userInput = Read-Host -Prompt "Modules were last updated on '$lastUpdate'. Do you want to update them?", "The modules will be updated and you can choose for each module if it should be updated.? [Y]es/[N]o"
            }
        }

        if ($userInput -eq "A" -or $userInput -eq "Y") {
            Write-Host "Updating modules..." -ForegroundColor Yellow
            $modulesConfig = Get-Content -Path $modulesConfigPath -Raw | ConvertFrom-Json
            $modulesToInstall = $modulesConfig.ModulesToInstall
            if (-not $modulesToInstall) {
                Write-Warning "No modules were found in '$modulesConfigPath'."
            }
            else {
                foreach ($moduleToInstall in $modulesToInstall) {
                    $module = Get-Module -Name $moduleToInstall -ListAvailable | Sort-Object -Property Version -Descending | Select-Object -First 1
                    if (-not $module) {
                        if ($PSCmdlet.ShouldContinue("Module '$($moduleToInstall)' is not installed. Do you want to install it?", "The module will be installed")) {
                            Install-Module -Name $moduleToInstall -Force
                        }
                    }
                    else {
                        $availableModule = Find-Module -Name $moduleToInstall
                        $availableModuleVersion = $availableModule.Version
                        $installedModuleVersion = $module.Version.ToString()
                        if ($installedModuleVersion -lt $availableModuleVersion) {
                            if ($userInput -eq "A") {
                                Write-Host "Updating module '$moduleToInstall' from version '$installedModuleVersion' to version '$availableModuleVersion"
                                Install-Module -Name $moduleToInstall -Force
                            }
                            else {
                                $userInput = Read-Host -Prompt "Update module '$moduleToInstall' from version '$installedModuleVersion' to version '$availableModuleVersion'? [Y]es/[N]o/[A]ll"
                                if ($userInput -eq "Y" -or $userInput -eq "A") {
                                    Install-Module -Name $moduleToInstall -Force
                                }
                            }
                        }
                    }
                }
                Write-Host "`nAll modules were updated successfully" -ForegroundColor Green
            }
            New-Item -Path $lastUpdateCheckPath -ItemType File -Force
        }

        # ---------------------------------------  Configure session ---------------------------------------

        try {
            Set-PSReadLineOption -PredictionSource HistoryAndPlugin -ErrorAction Stop
        }
        catch {
            Set-PSReadLineOption -PredictionSource History
        }
        Set-PSReadLineOption -PredictionViewStyle ListView
        Enable-AzPredictor

        # --------------------------------------- Start transcript logging ---------------------------------------
        $logFolder = "$env:USERPROFILE\PowerShellSessionLogs"
        if (-not (Test-Path -Path $logFolder)) {
            New-Item -Path $logFolder -ItemType Directory
        }
        $oldLogs = Get-ChildItem -Path $logFolder -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) }
        if ($oldLogs) {
            foreach ($oldLog in $oldLogs) {
                Remove-Item -Path $oldLog.FullName -Force
            }
        }
        #$logPath = "$logFolder\$(Get-Date -Format 'yyyy-MM-dd-HH-mm-ss').log"
        # The logPath includes the date and time of the session as well as the name of the user and the powershell host
        $logPath = "$logFolder\$($host.Name)_$(Get-Date -Format 'yyyy-MM-dd-HH-mm-ss').log"
        if (Test-Path -Path $logPath) {
            Remove-Item -Path $logPath -Force
        }
        Start-Transcript -Path $logPath
        Write-Host "Transcript log is located at '$logPath'" -ForegroundColor DarkGreen
        
        # --------------------------------------- Finish initialization ---------------------------------------
        Write-Host "Profile initialized" -ForegroundColor Green
        return "Press enter to get started..."
    }

    # Check if session is already initialized

    if ($global:profile_initialized -ne $true) {
        $global:profile_initialized = $true
        Initialize-Profile
    }
    # If profile is initialized run normal prompt
    else {
        $global:profile_initialized = $true
        if ((Get-History).Count -ge 1) {
            [double] $executionTime = ((Get-History)[-1].EndExecutionTime - (Get-History)[0].StartExecutionTime).TotalSeconds
            $time = [math]::Round($executionTime, 2)
            if ($time / 1000 -gt 1) {
                Write-Host "[$([math]::Round(($time/1000), 2)) s]" -NoNewline -ForegroundColor DarkYellow
            }
            else {
                Write-Host "[$time ms]" -NoNewline -ForegroundColor DarkYellow
            }
        }
        else {
            Write-Host "[0 ms]" -NoNewline -ForegroundColor DarkYellow
        }
        Write-Host " $((Get-Location).Path)" -NoNewline -ForegroundColor DarkBlue
        return " "
    }
}