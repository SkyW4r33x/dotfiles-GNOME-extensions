#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Author: Jordan aka SkyW4r33x
# Description: GNOME extensions installer
# Version: 1.2.0

import os
import subprocess
import shutil
import time
import sys
from pathlib import Path
import logging

# ------------------------------- Kali Style Class --------------------------- #

class KaliStyle:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BLUE = '\033[38;2;39;127;255m'  
    TURQUOISE = '\033[38;2;71;212;185m' 
    ORANGE = '\033[38;2;255;138;24m' 
    WHITE = '\033[37m'
    GREY = '\033[38;5;242m'
    RED = '\033[38;2;220;20;60m'  
    GREEN = '\033[38;2;71;212;185m' 
    YELLOW = '\033[0;33m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    SUDO_COLOR = '\033[38;2;94;189;171m' 
    APT_COLOR = '\033[38;2;73;174;230m' 
    SUCCESS = f"   {TURQUOISE}{BOLD}✔{RESET}"
    ERROR = f"   {RED}{BOLD}✘{RESET}"
    INFO = f"{BLUE}{BOLD}[i]{RESET}"
    WARNING = f"{YELLOW}{BOLD}[!]{RESET}"

# ------------------------------- Extensions Installer Class --------------------------- #

class ExtensionsInstaller:

    def __init__(self):
        if os.getuid() == 0:
            print(f"{KaliStyle.ERROR} Do not run this script with sudo or as root. Use a normal user like 'kali'.")
            sys.exit(1)
        
        original_user = os.environ.get('SUDO_USER', os.environ.get('USER') or Path.home().name)
        self.home_dir = os.path.expanduser(f'~{original_user}')
        self.current_user = original_user
        self.extensions_dir = os.path.join(self.home_dir, '.local/share/gnome-shell/extensions')
        self.temp_dir = '/tmp/gnome-extensions-install'
        self.config_dir = os.path.join(self.home_dir, '.config')
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.actions_taken = []  
        
        log_path = os.path.join(self.script_dir, 'install.log')
        if os.path.exists(log_path) and not os.access(log_path, os.W_OK):
            print(f"{KaliStyle.WARNING} Fixing permissions on {log_path}...")
            subprocess.run(['sudo', 'rm', '-f', log_path], check=True)
        logging.basicConfig(filename=log_path, level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def show_banner(self):
        print(f"""{KaliStyle.BLUE}{KaliStyle.BOLD}                                                       
             _____ _____ _____ _____ _____                               
            |   __|   | |     |     |   __|                              
            |  |  | | | |  |  | | | |   __|                              
            |_____|_|___|_____|_|_|_|_____|                                                                                     
 _____ __ __ _____ _____ _____ _____ _____ _____ _____ _____ 
|   __|  |  |_   _|   __|   | |   __|     |     |   | |   __|
|   __|-   -| | | |   __| | | |__   |-   -|  |  | | | |__   |
|_____|__|__| |_| |_____|_|___|_____|_____|_____|_|___|_____|{KaliStyle.RESET}                                  
        """)
        print(f"{KaliStyle.RED}{KaliStyle.BOLD}  D O T F I L E S   –   G N O M E   –   E X T E N S I O N S{KaliStyle.RESET}\n")
        print(f"{KaliStyle.WHITE}\t [ GNOME Extensions Installer - v.1.0.0 ]{KaliStyle.RESET}")
        print(f"{KaliStyle.GREY}\t\t [ Created by SkyW4r33x ]{KaliStyle.RESET}\n")

    def run_command(self, command, shell=False, sudo=False, quiet=True):
        try:
            if sudo and not shell:
                command = ['sudo'] + command
            result = subprocess.run(
                command,
                shell=shell,
                check=True,
                stdout=subprocess.PIPE if quiet else None,
                stderr=subprocess.PIPE if quiet else None,
                text=True
            )
            return True
        except subprocess.CalledProcessError as e:
            if not quiet:
                print(f"{KaliStyle.ERROR} Error executing command: {command}")
                print(f"Output: {e.stdout}")
                print(f"Error: {e.stderr}")
            logging.error(f"Error executing command: {command} - {e}\nOutput: {e.stdout}\nError: {e.stderr}")
            return False
        except PermissionError:
            print(f"{KaliStyle.ERROR} Insufficient permissions to execute: {command}")
            return False

    def check_command(self, command):
        try:
            subprocess.run([command, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def get_gnome_version(self):
        try:
            result = subprocess.run(['gnome-shell', '--version'], capture_output=True, text=True)
            version_str = result.stdout.strip().split()[-1]  
            major = int(version_str.split('.')[0])
            return major
        except Exception as e:
            logging.error(f"Error getting GNOME version: {str(e)}")
            return None

    def check_os(self):
        if not os.path.exists('/etc/debian_version'):
            print(f"{KaliStyle.ERROR} This script is designed for Debian/Kali based systems")
            return False
        return True

    def check_sudo_privileges(self):
        try:
            result = subprocess.run(['sudo', '-n', 'true'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                return True
            else:
                print(f"{KaliStyle.WARNING} This script needs to execute commands with sudo.")
                return True
        except Exception as e:
            print(f"{KaliStyle.ERROR} Could not verify sudo privileges: {str(e)}")
            return False

    def check_required_files(self):
        required_files = [
            "gnome-extensions"
        ]
        missing = [f for f in required_files if not os.path.exists(os.path.join(self.script_dir, f))]
        if missing:
            print(f"{KaliStyle.ERROR} Missing required files: {', '.join(missing)}")
            print(f"{KaliStyle.INFO} Make sure they are in {self.script_dir}")
            return False
        return True

    def install_custom_extensions(self):
        print(f"\n{KaliStyle.INFO} Installing custom extensions...")
        
        source_extensions_dir = os.path.join(self.script_dir, "gnome-extensions")
        if not os.path.exists(source_extensions_dir):
            print(f"{KaliStyle.ERROR} gnome-extensions folder not found in {source_extensions_dir}")
            return False
        
        custom_extensions = [
            "top-panel-ethernet@kali.org",
            "top-panel-vpnip@kali.org",
            "top-panel-target@kali.org"
        ]
        
        os.makedirs(self.extensions_dir, exist_ok=True)
        
        success_count = 0
        for extension in custom_extensions:
            source_path = os.path.join(source_extensions_dir, extension)
            dest_path = os.path.join(self.extensions_dir, extension)
            
            if not os.path.exists(source_path):
                print(f"{KaliStyle.ERROR} Extension {extension} not found in {source_path}")
                continue
                
            if os.path.exists(dest_path):
                print(f"{KaliStyle.WARNING} Extension {extension} already exists, skipping copy.")
                success_count += 1
                continue
            
            try:
                shutil.copytree(source_path, dest_path)
                self.actions_taken.append({'type': 'dir_copy', 'dest': dest_path})
                print(f"{KaliStyle.SUCCESS} Extension {extension} installed")
                success_count += 1
                
            except Exception as e:
                print(f"{KaliStyle.ERROR} Error copying {extension}: {str(e)}")
                logging.error(f"Error copying extension {extension}: {str(e)}")
        
        if success_count == len(custom_extensions):
            print(f"{KaliStyle.SUCCESS} All custom extensions installed correctly")
            return True
        elif success_count > 0:
            print(f"{KaliStyle.WARNING} {success_count}/{len(custom_extensions)} extensions installed")
            return True
        else:
            print(f"{KaliStyle.ERROR} Could not install any custom extension")
            return False

    def install_top_bar_organizer(self):
        print(f"\n{KaliStyle.INFO} Installing Top Bar Organizer from web...")
        uuid = "top-bar-organizer@julian.gse.jsts.xyz"
        gnome_version = self.get_gnome_version()
        if not gnome_version:
            print(f"{KaliStyle.ERROR} Could not determine GNOME version")
            return False
        url = f"https://extensions.gnome.org/download-extension/{uuid}.shell-extension.zip?shell_version={gnome_version}.0"
        temp_zip = os.path.join(self.temp_dir, f"{uuid}.zip")
        os.makedirs(self.temp_dir, exist_ok=True)
        if not self.run_command(['wget', '-q', url, '-O', temp_zip]):
            print(f"{KaliStyle.ERROR} Failed to download {uuid}")
            return False
        dest_dir = os.path.join(self.extensions_dir, uuid)
        if os.path.exists(dest_dir):
            print(f"{KaliStyle.WARNING} {uuid} already exists, removing...")
            shutil.rmtree(dest_dir)
        try:
            subprocess.run(['gnome-extensions', 'install', '--force', temp_zip], check=True)
            print(f"{KaliStyle.SUCCESS} {uuid} installed from web")
            self.actions_taken.append({'type': 'dir_copy', 'dest': dest_dir})
            return True
        except Exception as e:
            print(f"{KaliStyle.ERROR} Error installing {uuid}: {str(e)}")
            logging.error(f"Error installing top-bar-organizer: {str(e)}")
            return False

    def check_graphical_environment(self):
        if not os.environ.get('DISPLAY'):
            print(f"{KaliStyle.ERROR} No graphical environment detected.")
            return False
        return True

    def check_gnome_requirements(self):
        print(f"{KaliStyle.INFO} Checking requirements for GNOME extensions...")
        requirements = {
            'git': {'pkg': 'git', 'desc': 'Git'},
            'make': {'pkg': 'make', 'desc': 'Make'},
            'msgfmt': {'pkg': 'gettext', 'desc': 'Gettext'},
            'gnome-extensions': {'pkg': 'gnome-shell', 'desc': 'GNOME Extensions CLI'},
            'dconf': {'pkg': 'dconf-cli', 'desc': 'Dconf CLI'},
            'wget': {'pkg': 'wget', 'desc': 'Wget for downloading extensions'}
        }
        
        missing_pkgs = []
        for command, info in requirements.items():
            if not self.check_command(command):
                missing_pkgs.append(info['pkg'])
                print(f"{KaliStyle.ERROR} Missing {command} ({info['desc']})")
            else:
                print(f"{KaliStyle.SUCCESS} Found {command}")

        gnome_major = self.get_gnome_version()
        if gnome_major is None or gnome_major < 42 or gnome_major > 48:
            print(f"{KaliStyle.ERROR} Incompatible GNOME version or not detected (detected: {gnome_major}). Extensions may fail.")
            missing_pkgs.append('gnome-shell')  

        if missing_pkgs:
            print(f"\n{KaliStyle.INFO} Install manually:\n   {KaliStyle.BLUE}→{KaliStyle.RESET} {KaliStyle.SUDO_COLOR}sudo {KaliStyle.APT_COLOR}apt {KaliStyle.RESET}install {' '.join(missing_pkgs)}{KaliStyle.SUDO_COLOR} -y{KaliStyle.RESET}")
            return False
        print(f"{KaliStyle.SUCCESS} Requirements verified")
        return True

    def manage_extensions(self, quiet=False):
        if not quiet:
            print(f"\n{KaliStyle.INFO} Checking and disabling existing extensions")
        try:
            extensions_to_disable = [
                'system-monitor@gnome-shell-extensions.gcampax.github.com',
                'top-panel-vpnip@kali.org',
                'top-bar-organizer@julian.gse.jsts.xyz'
            ]
            for ext in extensions_to_disable:
                subprocess.run(['gnome-extensions', 'disable', ext], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if not quiet:
                    print(f"{KaliStyle.SUCCESS} Extension {ext} disabled (if it was active)")
            return True
        except Exception as e:
            if not quiet:
                print(f"{KaliStyle.WARNING} Could not manage all extensions")
            logging.error(f"Error in manage_extensions: {str(e)}")
            return False

    def enable_extensions(self):
        print(f"\n{KaliStyle.INFO} Enabling extensions...")
        
        extensions = [
            "top-panel-ethernet@kali.org",
            "top-panel-vpnip@kali.org",
            "top-bar-organizer@julian.gse.jsts.xyz",
            "top-panel-target@kali.org"
        ]
        
        enabled_count = 0
        for ext in extensions:
            try:
                subprocess.run(['gnome-extensions', 'enable', ext], check=True, stdout=subprocess.DEVNULL)
                print(f"{KaliStyle.SUCCESS} {ext} enabled")
                enabled_count += 1
            except subprocess.CalledProcessError as e:
                print(f"{KaliStyle.ERROR} Error enabling {ext}: {str(e)}")
                logging.error(f"Error enabling extension {ext}: {str(e)}")
            except Exception as e:
                print(f"{KaliStyle.ERROR} Unexpected error enabling {ext}: {str(e)}")
                logging.error(f"Error in enable_extensions: {str(e)}")
        
        try:
            dconf_path = '/org/gnome/shell/extensions/top-bar-organizer/'
            subprocess.run(['dconf', 'reset', '-f', dconf_path], check=True)
            order = [
                'top-panel-ethernet@kali.org',
                'top-panel-vpnip@kali.org',
                'top-bar-organizer@julian.gse.jsts.xyz',
                'top-panel-target@kali.org'
            ]
            dconf_value = f"['{','.join(order)}']"
            subprocess.run(['dconf', 'write', f'{dconf_path}top-bar-items-order', dconf_value], check=True)
            print(f"{KaliStyle.SUCCESS} Top Bar Organizer order configured: target at the end")
        except Exception as e:
            print(f"{KaliStyle.ERROR} Error configuring Top Bar Organizer order: {str(e)}")
            logging.error(f"Error configuring Top Bar Organizer order: {str(e)}")
        
        if enabled_count > 0:
            print(f"{KaliStyle.SUCCESS} {enabled_count}/{len(extensions)} extensions enabled")
            return True
        else:
            print(f"{KaliStyle.ERROR} Could not enable any extension")
            return False

    def verify_installation(self):
        print(f"\n{KaliStyle.INFO} Verifying installation...")
        
        extensions_to_check = [
            "top-panel-ethernet@kali.org",
            "top-panel-vpnip@kali.org",
            "top-bar-organizer@julian.gse.jsts.xyz",
            "top-panel-target@kali.org"
        ]
        
        installed_count = 0
        for ext in extensions_to_check:
            ext_path = os.path.join(self.extensions_dir, ext)
            system_path = f"/usr/share/gnome-shell/extensions/{ext}"
            if os.path.exists(ext_path) or os.path.exists(system_path):
                print(f"{KaliStyle.SUCCESS} {ext} found")
                installed_count += 1
            else:
                print(f"{KaliStyle.ERROR} {ext} not found")
        
        if installed_count > 0:
            print(f"\n{KaliStyle.WARNING} Restart GNOME Shell {KaliStyle.GREY}(Alt + F2, 'r'){KaliStyle.RED}")
            input(f"\n{KaliStyle.SUDO_COLOR}[*]{KaliStyle.RESET} Press Enter after restarting GNOME Shell...")
            self.enable_extensions()
            return True
        return False

    def setup_aliases(self):
        print(f"\n{KaliStyle.INFO} Setting up aliases...")
        zshrc_path = f"{self.home_dir}/.zshrc"
        
        target_dir = os.path.join(self.config_dir, "bin", "target")
        os.makedirs(target_dir, exist_ok=True)
        self.actions_taken.append({'type': 'dir_copy', 'dest': target_dir})
        print(f"{KaliStyle.SUCCESS} Directory {target_dir} created or verified")
        
        target_file = os.path.join(target_dir, "target.txt")
        try:
            with open(target_file, 'a') as f:
                pass
            self.actions_taken.append({'type': 'file_copy', 'dest': target_file})
            print(f"{KaliStyle.SUCCESS} File {target_file} created")
        except Exception as e:
            print(f"{KaliStyle.ERROR} Error creating {target_file}: {str(e)}")
            logging.error(f"Error creating {target_file}: {str(e)}")
            return False

        aliases_and_functions = [
            f"\n# Aliases\nalias {self.current_user}='su {self.current_user}'",
            "\nalias bat='batcat'",
            f"""\n# settarget function
    function settarget() {{

        local WHITE='\\033[1;37m'
        local GREEN='\\033[0;32m'
        local YELLOW='\\033[1;33m'
        local RED='\\033[0;31m'
        local BLUE='\\033[0;34m'
        local CYAN='\\033[1;36m'
        local PURPLE='\\033[1;35m'
        local GRAY='\\033[38;5;244m'
        local BOLD='\\033[1m'
        local ITALIC='\\033[3m'
        local COMAND='\\033[38;2;73;174;230m'
        local NC='\\033[0m' # No color
        
        local target_file="{target_file}"
        
        mkdir -p "$(dirname "$target_file")" 2>/dev/null
        
        if [ $# -eq 0 ]; then
            if [ -f "$target_file" ]; then
                rm -f "$target_file"
                echo -e "\\n${{CYAN}}[${{BOLD}}+${{NC}}${{CYAN}}]${{NC}} Target cleared successfully\\n"
            else
                echo -e "\\n${{YELLOW}}[${{BOLD}}!${{YELLOW}}]${{NC}} No target to clear\\n"
            fi
            return 0
        fi
        
        local ip_address="$1"
        local machine_name="$2"
        
        if [ -z "$ip_address" ] || [ -z "$machine_name" ]; then
            echo -e "\\n${{RED}}▋${{NC}} Error${{RED}}${{BOLD}}:${{NC}}${{ITALIC}} usage mode.${{NC}}"
            echo -e "${{GRAY}}—————————————————————${{NC}}"
            echo -e "  ${{CYAN}}• ${{NC}}${{COMAND}}settarget ${{NC}}192.168.1.100 Kali "
            echo -e "  ${{CYAN}}• ${{NC}}${{COMAND}}settarget ${{GRAY}}${{ITALIC}}(clear target)${{NC}}\\n"
            return 1
        fi
        
        if ! echo "$ip_address" | grep -qE '^[0-9]{{1,3}}\\.[0-9]{{1,3}}\\.[0-9]{{1,3}}\\.[0-9]{{1,3}}$'; then
            echo -e "\\n${{RED}}▋${{NC}} Error${{RED}}${{BOLD}}:${{NC}}"
            echo -e "${{GRAY}}————————${{NC}}"
            echo -e "${{RED}}[${{BOLD}}✘${{NC}}${{RED}}]${{NC}} Invalid IP format ${{YELLOW}}→${{NC}} ${{RED}}$ip_address${{NC}}"
            echo -e "${{BLUE}}${{BOLD}}[+] ${{NC}}Valid example:${{NC}} ${{GRAY}}192.168.1.100${{NC}}\\n"
            return 1
        fi
        
        if ! echo "$ip_address" | awk -F'.' '{{
            for(i=1; i<=4; i++) {{
                if($i < 0 || $i > 255) exit 1
                if(length($i) > 1 && substr($i,1,1) == "0") exit 1
            }}
        }}'; then
            echo -e "\\n${{RED}}[${{BOLD}}✘${{NC}}${{RED}}]${{NC}} Invalid IP ${{RED}}→${{NC}} ${{BOLD}}$ip_address${{NC}}"
            return 1
        fi
        
        echo "$ip_address $machine_name" > "$target_file"
        
        if [ $? -eq 0 ]; then
            echo -e "\\n${{YELLOW}}▌${{NC}}Target set successfully${{YELLOW}}${{BOLD}}:${{NC}}"
            echo -e "${{GRAY}}—————————————————————————————————${{NC}}"
            echo -e "${{CYAN}}→${{NC}} IP Address:${{GRAY}}...........${{NC}} ${{GREEN}}$ip_address${{NC}}"
            echo -e "${{CYAN}}→${{NC}} Machine Name:${{GRAY}}.........${{NC}} ${{GREEN}}$machine_name${{NC}}\\n"
        else
            echo -e "\\n${{RED}}[${{BOLD}}✘${{NC}}${{RED}}]${{NC}} Could not save the target\\n"
            return 1
        fi
        
        return 0
    }}"""
        ]
        try:
            with open(zshrc_path, 'a') as f:
                f.writelines(aliases_and_functions)
            print(f"{KaliStyle.SUCCESS} Aliases configured")
            return True
        except Exception as e:
            print(f"{KaliStyle.ERROR} Error setting aliases in {zshrc_path}: {str(e)}")
            logging.error(f"Error setting aliases: {str(e)}")
            return False

    def show_final_message(self):
        time.sleep(2)
        os.system('clear')
        print(f"\n\t\t[{KaliStyle.BLUE}{KaliStyle.BOLD}+{KaliStyle.RESET}] Installation Summary [{KaliStyle.BLUE}{KaliStyle.BOLD}+{KaliStyle.RESET}]\n\n")

        print(f"[{KaliStyle.BLUE}{KaliStyle.BOLD}+{KaliStyle.RESET}] GNOME Extensions")
        extensions = [
            ("Top Panel Ethernet", "Network interface monitoring"),
            ("Top Panel VPN IP", "VPN connection status"),
            ("Top Bar Organizer", "Panel element organization"),
            ("Top Panel Target", "Target machine information")
        ]
        
        for name, desc in extensions:
            print(f"   {KaliStyle.YELLOW}▸{KaliStyle.RESET} {KaliStyle.WHITE}{name:<18}{KaliStyle.RESET} {KaliStyle.GREY}→{KaliStyle.RESET} {desc}")
        
        print()

        print(f"\n{KaliStyle.WARNING}{KaliStyle.BOLD} Important Notes:{KaliStyle.RESET}")
        print(f"   • Click on IP addresses to copy them to clipboard")
        print(f"   • Use {KaliStyle.APT_COLOR}settarget{KaliStyle.RESET} <IP> <Name> to set target")
        print(f"   • Example: {KaliStyle.APT_COLOR}settarget{KaliStyle.RESET} 192.168.1.100 Kali")
        print(f"   • Use {KaliStyle.APT_COLOR}settarget{KaliStyle.RESET} (no args) to clear target")
        
        print(f"\n{KaliStyle.TURQUOISE}{'═' * 50}{KaliStyle.RESET}")
        print(f"\n{KaliStyle.WARNING}{KaliStyle.BOLD} Important:{KaliStyle.RESET} Restart GNOME Shell {KaliStyle.GREY}(Alt + F2, 'r'){KaliStyle.RESET} or reboot to apply all changes")
        print(f"\n\t\t\t{KaliStyle.RED}{KaliStyle.BOLD}  H4PPI H4CK1NG{KaliStyle.RESET}")

    def cleanup(self):
        # print(f"\n{KaliStyle.INFO} Cleaning temporary files...")
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            #print(f"{KaliStyle.SUCCESS} {KaliStyle.GREEN}Completed{KaliStyle.RESET}")
            return True
        return True

    def rollback(self):
        print(f"{KaliStyle.WARNING} Rolling back changes...")
        for action in reversed(self.actions_taken):
            if action['type'] == 'file_copy' and os.path.exists(action['dest']):
                self.run_command(['rm', action['dest']], sudo=True, quiet=True)
                print(f"{KaliStyle.SUCCESS} Deleted {action['dest']}")
            elif action['type'] == 'dir_copy' and os.path.exists(action['dest']):
                self.run_command(['rm', '-rf', action['dest']], sudo=True, quiet=True)
                print(f"{KaliStyle.SUCCESS} Deleted {action['dest']}")
        print(f"{KaliStyle.SUCCESS} Changes rolled back")

    def run(self):
        if not all([self.check_os(), self.check_sudo_privileges(), self.check_required_files(), self.check_graphical_environment()]):
            return False

        os.system('clear')
        self.show_banner()

        if not self.check_gnome_requirements():
            return False
        tasks = [
            (self.manage_extensions, "Managing existing extensions"),
            (self.install_custom_extensions, "Custom extensions installation"),
            (self.install_top_bar_organizer, "Top Bar Organizer installation from web"),
            (self.verify_installation, "Installation verification"),
            (self.setup_aliases, "Aliases setup")
        ]

        total_tasks = len(tasks)

        try:
            for i, (task, description) in enumerate(tasks, 1):
                print(f"\n{KaliStyle.GREY}{'─' * 40}{KaliStyle.RESET}")
                print(f"{KaliStyle.INFO} ({i}/{total_tasks}) Starting {description}...")
                if not task():
                    print(f"{KaliStyle.ERROR} Error in {description}")
                    self.rollback()
                    self.cleanup()
                    return False
                time.sleep(0.5)
            print()

            self.show_final_message()
            self.cleanup()
            logging.info("Installation completed successfully")
            return True

        except KeyboardInterrupt:
            print(f"\n{KaliStyle.WARNING} Installation interrupted")
            self.rollback()
            self.cleanup()
            return False
        except Exception as e:
            print(f"{KaliStyle.ERROR} Error: {str(e)}")
            logging.error(f"General error in run: {str(e)}")
            self.rollback()
            self.cleanup()
            return False

if __name__ == "__main__":
    installer = ExtensionsInstaller()
    installer.run()