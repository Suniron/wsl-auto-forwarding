# wsl-auto-forwarding

## Prerequisites

- [Python3](https://www.python.org/downloads/) installed on Windows host.
- net-tools installed on WSL (`sudo apt install net-tools`).

## Usage

1. Launch a terminal (_**bash** or **cmd**_) **as Administrator**.
2. Clone the script on your Windows machine.
3. Get the name of the WSL distribution (`wsl.exe -l`).
4. In python script, fill the `PORTS_TO_FORWARD` variable with all ports you want to forward.
5. Run the script: `python3 wsl-auto-forwarding.py "Name of you WSL machine"`.
