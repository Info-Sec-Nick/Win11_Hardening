# Import Modules 

import getpass                                                                  # This imports the getpass module to get Windows User
import platform                                                                 # This imports the platform module to get Windows version
#import pandas as pd                                                             # This imports the pandas module to allow the code to read excel spreadsheet
import winreg                                                                   # This imports the windows registery module to query programs
import subprocess                                                               # This imports the subprocess module to allow external progams to be called
import os                                                                       # This imports the os module to access system file structure

# Import for table functionality
from rich.console import Console
from rich.table import Table
from rich import box


def user():
    current_user = getpass.getuser()                                            # Get Windows user and store it in the current_user variable
    print("\nChecking Current User......")                                      # Print user message
    print(f"Current user logged in: {current_user}")                            # Print the current logged in user
user()                                                                          # This calls the fucntion defined with def user():

# Initilize Rich Console
console = Console()

# Function to Check Operating System
def check_os():
    os_name = platform.system()                                                 # Using the Platform module to get the OS and assign it to a variable
    os_release = platform.release()                                             # Using the Platform module to get the Release and assign it to a variable
    full_os = f"{os_name} {os_release}"
    ism = "ISM-1407"                                                            # Manually assigning the ISM control number to the check. Will automate this at a later stage
    if os_name == "Windows" and int(os_release) >= 10:                          # Rule to check compliance of Latest Windows Release or Previous Version
        status = "[green]PASS[/green]"
    else:
        status = "[red]FAIL[/red]"

    return ("Latest or Previous OS", ism, full_os, status)

# Function to check operating system architecture 
def check_arch():
    os_arch = platform.architecture()[0]                                        # Using the Platform module to get the architecture type, the [0] is used to only take the first number from 64bit
    ism = "ISM-1408"                                                            # Manually assigning the ISM control number to the check. Will automate this at a later stage
    if os_arch == "64bit":                                                      # Rule to check compliance of 64bit operating systems
        status = "[green]PASS[/green]"
    else:
        status = "[red]FAIL[/red]"
    
    return ("Architecture Build", ism, os_arch, status)

# Function to check IE11 Install status
def check_ie11():
    try:
        key_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Internet Explorer 11"         # RegEdit path to uninstalled software
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ) as key:                # Using winreg to read the key
            status = "[red]FAIL[/red]"
            result = "Internet Explorer 11 is installed on this machine"
    except FileNotFoundError:                                                                               # Checking to see if the folder / key is available. Error means not installed
        status = "[green]PASS[/green]"
        result = "Internet Explorer 11 is not installed on this machine"
    ism = "ISM-1654"                                                                                        # Manually assigning ISM control number to the check. Will automate this at a later stage
    return ("IE11 Status", ism, result, status)

# Function to check PowerShell Version and Constrained Language Mode
def check_ps():
    try:
        result = subprocess.run(                                                                            # Using the subprocess module to run the DISM command
            ["DISM", "/online", "/get-features", "/format:table"],                                          # Pulling the windows get features table
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        ism = "ISM-1621"
        for line in output.splitlines():
            if "MicrosoftWindowsPowerShellV2" in line:                                                      # Using the output to look if PowerShell is in the line
                if "Enabled" in line:                                                                       # If the output finds PowerShell and also finds the text Enabled it fails the check
                    return ("PowerShell v2", ism, "Installed", "[red]FAIL[/red]")
                elif "Disabled" in line:
                    return ("PowerShell v2", ism, "Not Installed", "[green]PASS[/green]")  
        return ("PowerShell v2", "Feature not found", "[green]PASS[/green]")
    except Exception as e:
        return ("PowerShell v2", ism, f"Error: {str(e)}", "[red]FAIL[/red]")

def check_constrained():
    try:
        result = subprocess.run(
            ["PowerShell", "-Command", "$ExecutionContext.SessionState.LanguageMode"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        mode = result.stdout.strip()
        ism = "ISM-1622"
        if mode == "ConstrainedLanguage":
            return ("PowerShell Language Mode", ism, mode, "[green]PASS[/green]")
        else:
            return ("PowerShell Language Mode", ism, mode, "[red]FAIL[/red]")
    except Exception as e:
        return ("PowerShell Language Mode", ism, f"Error: {str(e)}", "[red]FAIL[/red]")
    
def check_ssh():
    config_path = r"C:\\ProgramData\\ssh\\sshd_config"
    ism = "ISM-1506"
    if not os.path.exists(config_path):
        return ("SSH Protocol Version", ism, "sshd_config not found", "[yellow]WARNING[/yellow]")
    try:
        with open(config_path, "r") as f:
            content = f.read()

            if "Protocol 1" in content:
                return ("SSH Protocol Version", ism, "Protocol 1 Found", "[red]FAIL[/red]")
            elif "Protocol 2" in content:
                return ("SSH Protocol Version", ism, "Protocol 2 Found", "[green]PASS[/green]")
            else:
                return ("SSH Protocol Version", ism, "Protocol not explicitly set", "[yellow]WARNING[/yellow]")
    except Exception as e:
        return ("SSH Protocol Version", ism, f"Error: {str(e)}", "[red]FAIL[/red]")

# Display Results in Table
def display_results():
    table = Table(title="\nISM Compliance Check Results", box=box.DOUBLE)

    table.add_column("Check", style="bold blue")                                # Adds Check description column to the results table
    table.add_column("ISM Control", justify="center")                           # Adds ISM Control column to the results table
    table.add_column("Result", justify="center")                                # Adds Results column to the results table
    table.add_column("Status", justify="center")                                # Adds Status column to the results table

    os_check = check_os()                                                       # Assign variable to parse to the table
    table.add_row(*os_check)                                                    # Adds Check_OS row to the results table
    arch_check = check_arch()                                                   # Assigns variable to parse to the table
    table.add_row(*arch_check)                                                  # Adds Check_arch row to the results table
    ie11_check = check_ie11()                                                   # Assigns variable to parse to the table
    table.add_row(*ie11_check)                                                  # Adds Check_ie11 row to the results table
    ps_check = check_ps()                                                       # Assigns variable to parse to the table
    table.add_row(*ps_check)                                                    # Adds Check_PS row to the results table
    constrained_check = check_constrained()                                     # Assigns a variable to parse to the table
    table.add_row(*constrained_check)                                           # Adds Check_Constrained row to the results table
    ssh_check = check_ssh()
    table.add_row(*ssh_check)

    console.print(table)

display_results()