#!/usr/bin/env python3
"""
THREAD HANDLER MODULE
Thread management and coordination
"""

import threading
import queue
import time
from colorama import Fore, Style

class ThreadManager:
    def __init__(self, max_threads=10000):
        self.max_threads = min(max_threads, 10000)
        self.active_threads = 0
        self.thread_pool = []
        self.task_queue = queue.Queue()
        self.lock = threading.Lock()
        self.running = False
        
    def start_threads(self, target_func, num_threads, *args, **kwargs):
        """Start specified number of threads"""
        num_threads = min(num_threads, self.max_threads)
        
        print(f"{Fore.CYAN}[*] Starting {num_threads} threads...")
        
        self.running = True
        self.thread_pool = []
        
        # Create and start threads
        for i in range(num_threads):
            if not self.running:
                break
                
            t = threading.Thread(
                target=self._thread_wrapper,
                args=(target_func, i, *args),
                kwargs=kwargs,
                daemon=True
            )
            
            with self.lock:
                self.active_threads += 1
                self.thread_pool.append(t)
            
            t.start()
            
            # Stagger thread creation
            if i % 100 == 0 and i > 0:
                time.sleep(0.01)
        
        print(f"{Fore.GREEN}[✓] Started {len(self.thread_pool)} threads")
        return self.thread_pool
    
    def _thread_wrapper(self, target_func, thread_id, *args, **kwargs):
        """Wrapper for thread execution with error handling"""
        try:
            target_func(thread_id, *args, **kwargs)
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Thread {thread_id} error: {str(e)[:50]}")
        finally:
            with self.lock:
                self.active_threads -= 1
    
    def stop_threads(self):
        """Stop all threads"""
        print(f"{Fore.YELLOW}[*] Stopping threads...")
        self.running = False
        
        # Wait for threads to finish
        timeout = 5
        start_time = time.time()
        
        while self.active_threads > 0:
            if time.time() - start_time > timeout:
                print(f"{Fore.RED}[!] Timeout waiting for threads to stop")
                break
            time.sleep(0.1)
        
        print(f"{Fore.GREEN}[✓] Threads stopped. Active: {self.active_threads}")
    
    def get_thread_count(self):
        """Get current thread count"""
        with self.lock:
            return self.active_threads
    
    def add_task(self, task):
        """Add task to queue"""
        self.task_queue.put(task)
    
    def worker(self):
        """Worker thread for task processing"""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                if task:
                    task()
                self.task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Worker error: {str(e)[:50]}")
    
    def monitor_threads(self, interval=1):
        """Monitor thread status"""
        print(f"{Fore.CYAN}[*] Thread monitor started")
        
        while self.running:
            with self.lock:
                active = self.active_threads
                total = len(self.thread_pool)
            
            if total > 0:
                health = (active / total) * 100
                print(f'\r{Fore.MAGENTA}[+] Threads: {active}/{total} | Health: {health:.1f}%', end='', flush=True)
            
            time.sleep(interval)
        
        print(f"\n{Fore.GREEN}[✓] Thread monitor stopped")
