# test_helper.py

import time
import socket
import re
import requests
import ctypes
import psutil
import os

# ---- 1. Recursive tag extraction ---- #
def extract_strings_recursive(test_str, tag):
    start_idx = test_str.find(f"<{tag}>")
    if start_idx == -1:
        return []
    end_idx = test_str.find(f"</{tag}>", start_idx)
    if end_idx == -1:
        return []  # prevent index error if tag is malformed
    content = test_str[start_idx+len(tag)+2:end_idx]
    return [content] + extract_strings_recursive(test_str[end_idx+len(tag)+3:], tag)

# ---- 2. Performance Timer ---- #
def timed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"[PERF] Function '{func.__name__}' took {time.time() - start:.5f}s")
        return result
    return wrapper

# ---- 3. Socket ingress/egress simulation ---- #
def start_ingress_server(port=5001):
    """Socket server to simulate ingress (data coming in)"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"[INGRESS] Server listening on port {port}...")
        conn, addr = s.accept()
        with conn:
            print(f"[INGRESS] Connected by {addr}")
            data = conn.recv(1024)
            print(f"[INGRESS] Received data: {data.decode()}")

def egress_to_server(data, port=5001):
    """Socket client to send data (egress)"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', port))
        s.sendall(data.encode())
        print("[EGRESS] Data sent.")

# ---- 4. Simulate ReadProcessMemory (limited) ---- #
def list_process_memory(pid=None):
    """Simulated ReadProcessMemory-like behavior using psutil"""
    pid = pid or os.getpid()
    try:
        proc = psutil.Process(pid)
        print(f"[MEMORY] Process name: {proc.name()}")
        print(f"[MEMORY] Memory info: {proc.memory_info()}")
    except Exception as e:
        print(f"[ERROR] Could not read memory info: {e}")

# ---- 5. String extraction using regex ---- #
def extract_item_names(html_str):
    """Extract <item>...</item> using regex"""
    return re.findall(r"<item>(.*?)</item>", html_str)

# ---- 6. Test endpoint to simulate request ---- #
def simulate_cart_request(url):
    try:
        r = requests.get(url)
        items = extract_item_names(r.text)
        return items
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        return []
