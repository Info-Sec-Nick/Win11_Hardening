

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
        return "PASS: Windows Defender is running"
    } else {
        return "FAIL: Windows Defender is not running"
    }
}

function Main {
    Write-Output "Starting ISM Windows Hardening Checks...`n"

    $results = @()
    $results += Check-WindowsDefender

    $results | ForEach-Object { Write-Output $_ }

    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $results | Out-File -FilePath ".\hardening_report_$timestamp.txt"

    Write-Output "`nResults saved to: hardening_report_$tiimestamp.txt"

}
Main