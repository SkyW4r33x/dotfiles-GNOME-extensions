![Banner](https://i.imgur.com/FMH528x.png) 

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Installer](#running-the-installer)
  - [Setting a Target](#setting-a-target)
- [Visuals](#visuals)
  - [Top Bar without Target Configured](#top-bar-without-target-configured)
  - [Top Bar with Target Configured](#top-bar-with-target-configured)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Introduction

This project provides an installer for custom GNOME Shell extensions designed for Debian or Kali Linux-based systems. It installs and configures extensions to enhance the top panel with useful indicators for network interfaces, VPN IP, and target machine information. The extensions include:

- **Top Panel Ethernet**: Displays network interface monitoring.
- **Top Panel VPN IP**: Shows VPN connection status.
- **Top Panel Target**: Displays target machine information (configured via the `settarget` alias).
- **Top Bar Organizer**: Organizes panel elements (installed from the official GNOME Extensions website for the latest version).
  
![extensions](https://i.imgur.com/iVpVTLF.png)

The script also sets up aliases, including `settarget`, to manage IPs and target machine names in the terminal.

This tool is designed for users seeking an optimized and customizable GNOME experience, especially in penetration testing or development environments.

## Requirements

- Debian or Kali Linux-based operating system.
- GNOME Shell version 42–48.
- Python 3.x.
- Required packages: `git`, `make`, `gettext`, `gnome-shell`, `dconf-cli`, `wget`.
- Run as a normal user (not root/sudo).
- Graphical environment (X11 or Wayland with DISPLAY configured).

Install missing packages:
```
sudo apt install git make gettext gnome-shell dconf-cli wget -y
```
> 💡 If any requirement is missing, the installer will indicate what is needed to proceed with the installation.

## Installation

1. Clone or download the repository:
   ```
   git clone https://github.com/your-repository/gnome-extensions-installer.git
   cd gnome-extensions-installer
   ```

2. Run the installer:
   ```
   python3 install.py
   ```

> 💡 Follow the on-screen instructions. Restart GNOME Shell when prompted (Alt + F2, type `r`, press Enter).

## Usage

### Running the Installer

Run the script as shown above. It will check requirements, disable conflicting extensions, install custom ones, configure the top bar, and set up aliases.

After installation:
- Restart GNOME Shell or the system.
- Verify that extensions are enabled with `gnome-extensions list`.

### Setting a Target

Use the `settarget` alias added to your `~/.zshrc` (refresh with `source ~/.zshrc` if needed).

- Set a target:
  ```
  settarget 192.168.1.1 Kali
  ```

- Clear target:
  ```
  settarget
  ```

This updates the Top Panel Target indicator in real-time.

![settarget](https://i.imgur.com/VqStQTn.png)

## Visuals

Below are visuals of the GNOME top bar with the installed extensions. These show the appearance when no target is configured (empty indicator) and when a target is configured (displays IP and machine name).

### Top Bar without Target Configured

When no target is set with `settarget`, the Target indicator is empty.

![Top Bar without Target](https://i.imgur.com/3M5BFqo.png)

*(Description: The top bar shows Ethernet status on the left, VPN IP in the middle, Top Bar Organizer elements, and an empty space for Target at the end.)*

### Top Bar with Target Configured

After running `settarget 192.168.1.1 Kali`, the Target indicator displays the IP and machine name at the end of the bar.

![Top Bar with Target](https://i.imgur.com/DzoNdQn.png)

*(Description: The top bar shows Ethernet status, VPN IP, Top Bar Organizer elements, and "Target: 192.168.1.1 (Kali)" at the end.)*

## Contributing

Contributions are welcome! Fork the repository, make changes, and submit a pull request. Ensure the code follows Python best practices and is tested on Kali Linux.

# H4PP1 H4CK1NG
