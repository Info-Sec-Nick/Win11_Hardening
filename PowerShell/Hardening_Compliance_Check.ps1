

##############################################################
# TITLE: ISM Compliance System Checker                       #
#                                                            #
# AUTHOR: Nick Kroepsch                                      #     
#                                                            #
# VERSION: Version 0.1                                       #
#                                                            #
# DESCRIPTION: This tool will audit the current system and   #
#              do some basic checks to see if the system     # 
#              aligns with the ISM framework.                #
##############################################################




## LIST OF AUDIT CHECKS AGAINST THE SYSTEM ##
function Check-WindowsDefender {
    $service = Get-Service -Name WinDefend
    if ($service.Status -eq 'Running') {
        return "PASS: Windows Defender is running`nCompliant with ISM Control [ISM-1341] - A HIPS or EDR solution is implemented on Workstations. "
    } else {
        return "FAIL: Windows Defender is not running"
    }
}

function Check-PowerShellVersion {
    $currentversion = $PSVersionTable.PSVersion.Major
    if ($currentversion -gt 2) {
        return "PASS: PowerShell version is currently $currentversion, running newer than v2.0`nCompliant with ISM Control [ISM-1621] - Windows PowerShell 2.0 is disabled or removed" 
    } else {
        return "FAIL: PowerShell currently $currentversion, and is not running newer than v2.0"
    }
}

function Check-OperatingVersion {
    $os = Get-CimInstance -ClassName Win32_OperatingSystem
    $version = $os.Version
    $caption = $os.Caption

    if ([version]$version -ge [version]"10.0.19045") {
        return "PASS: Windows Operating System is running $caption (Version $version), this is the newest up-to-date version.`nCompliant with ISM Control [ISM-1407] - The latest release or previous release of operating systems are used."
    } else {
        return "FAIL: Windows Operating System is running $caption (Version $version). Please update your system or contact your system administrator."
    }
}

function Check-PowershellLanguage {
    $langmode = $ExecutionContext.SessionState.LanguageMode

    if ($langmode -eq "ConstrainedLanguage") {
        return "PASS: Windows is running PowerShell in Constrained Language Mode`nCompliant with ISM Control [ISM-1622] - PowerShell is configured to use Constrained Language Mode"
    } else {
        return "FAIL: Windows is running PowerShell incorrectly configured to comply with [ISM-1622]"
    }
}
## MAIN FUCNTION TO RUN CHECKS ##
function Main {
    Write-Host "Starting ISM Windows Hardening Checks...`n" -ForegroundColor DarkCyan

    $results = @()
    $results += Check-WindowsDefender
    $results += Check-PowerShellVersion
    $results += Check-OperatingVersion
    $results += Check-PowershellLanguage

    $results | ForEach-Object { 
        if ($_ -like "PASS*") {
            Write-Host $_ -ForegroundColor Green
        } elseif ($_ -like "FAIL*") {
            Write-Host $_ -ForegroundColor Red
        } else {
            Write-Host $_
        }
        Write-Host "" # Blank line
        
    }

    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $results | Out-File -FilePath ".\hardening_report_$timestamp.txt"

    Write-Output "`nResults saved to: hardening_report_$timestamp.txt"

    Read-Host "`nPress ENTER to exit...."
}
Main
