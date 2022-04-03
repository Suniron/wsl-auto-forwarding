#!/usr/bin/env python3

import sys
import subprocess
import re
import os

PORTS_TO_FORWARD = [
    80,
    443,
    # ... add some extras ports here
]

wsl_distribution_name = sys.argv[1]

# Exit, if distribution name is invalid:
if not re.search(f"\s{wsl_distribution_name}\s", subprocess.Popen(
        'wsl --list', stdout=subprocess.PIPE).communicate()[0].decode('u16')):
    print(
        f'Error: invalid distribution name: "{wsl_distribution_name}". Please, check your distributions:')
    os.system('wsl --list')
    sys.exit(1)


wsl_ifconfig = subprocess.Popen(
    f'wsl -d {wsl_distribution_name} ifconfig', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

[wsl_ips_raw, ifconfigError] = wsl_ifconfig.communicate()

# Exit, if distribution doesn't have "net-tools" (ifconfig):
if ifconfigError:
    print(
        f'Error: "ifconfig" seem to be not available, please install it with "wsl -d {wsl_distribution_name} sudo apt install net-tools"')
    # TODO: ask user to install it (need sudo password)
    sys.exit(1)

# Get IP from WSL Linux distribution
wsl_ip_address = re.search(
    "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", wsl_ips_raw.decode()).group()

windows_ip_address = "0.0.0.0"
all_ports = ",".join(map(str, PORTS_TO_FORWARD))

# Remove firewall rule if it exists
[success, error] = subprocess.Popen(

    "powershell -command \"Remove-NetFireWallRule -DisplayName 'WSL 2 Firewall Unlock'\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

if success:
    print("Removed firewall rule with success!")

# Create firewall rules:
subprocess.Popen(
    "powershell -command \"New-NetFireWallRule -DisplayName 'WSL 2 Firewall Unlock' -Direction Outbound -LocalPort $ports_a -Action Allow -Protocol TCP\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
subprocess.Popen(
    "powershell -command \"New-NetFireWallRule -DisplayName 'WSL 2 Firewall Unlock' -Direction Inbound -LocalPort $ports_a -Action Allow -Protocol TCP\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

# For each port, create a local redirect rule:
for port in all_ports.split(","):
    subprocess.Popen(
        f"netsh interface portproxy delete v4tov4 listenport={port} listenaddress={windows_ip_address}", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    subprocess.Popen(
        f"netsh interface portproxy add v4tov4 listenport={port} listenaddress={windows_ip_address} connectport={port} connectaddress={wsl_ip_address}", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
