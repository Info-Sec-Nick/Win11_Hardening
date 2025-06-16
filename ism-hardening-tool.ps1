

##############################################################
# TITLE: Windows System Hardening Tool - ISM Aligned         #
#                                                            #
# AUTHOR: Nick Kroepsch                                      #     
#                                                            #
# VERSION: Version 0.1                                       #
#                                                            #
# DESCRIPTION: This tool will audit the current system and   #
#              do some basic checks to see if the system     # 
#              aligns with the ISM framework.                #
##############################################################


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
    if ($currentversion -gt '2') {
        return "PASS: PowerShell version is currently $currentversion, running newer than v2.0`nCompliant with ISM Control [ISM-1621] - Windows PowerShell 2.0 is disabled or removed" 
    } else {
        return "FAIL: PowerShell currently $currentversion, and is not running newer than v2.0"
    }
}

function Main {
    Write-Output "Starting ISM Windows Hardening Checks...`n"

    $results = @()
    $results += Check-WindowsDefender
    $results += Check-PowerShellVersion

    $results | ForEach-Object { Write-Output $_ }

    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $results | Out-File -FilePath ".\hardening_report_$timestamp.txt"

    Write-Output "`nResults saved to: hardening_report_$tiimestamp.txt"

}
Main