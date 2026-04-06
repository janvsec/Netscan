import ipaddress
import subprocess
import platform
import socket
import threading
import shutil
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)

OS = platform.system().lower()

COMMON_PORTS = {
    20: "FTP DATA",
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MYSQL",
    3389: "RDP",
    5432: "POSTGRES",
    5900: "VNC"
}

THREADS_HOST = 200
THREADS_PORT = 100
TIMEOUT = 0.8

def ping_cmd(ip):
    if OS == "windows":
        return ["ping", "-n", "1", "-w", "800", str(ip)]
    return ["ping", "-c", "1", "-W", "1", str(ip)]

def is_alive_ping(ip):
    try:
        result = subprocess.run(
            ping_cmd(ip),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False

def is_alive_tcp(ip):
    for port in (80, 443, 22):
        try:
            with socket.socket() as s:
                s.settimeout(TIMEOUT)
                if s.connect_ex((ip, port)) == 0:
                    return True
        except Exception:
            continue
    return False

def is_alive(ip):
    return is_alive_ping(ip) or is_alive_tcp(ip)

def scan_subnet(net):
    found = []
    with ThreadPoolExecutor(max_workers=THREADS_HOST) as executor:
        futures = {executor.submit(is_alive, str(ip)): str(ip) for ip in net.hosts()}
        for future in as_completed(futures):
            if future.result():
                found.append(futures[future])
    return found

def grab_banner(ip, port):
    try:
        with socket.socket() as s:
            s.settimeout(TIMEOUT)
            s.connect((ip, port))
            s.sendall(b"\r\n")
            banner = s.recv(1024).decode(errors="ignore").strip()
            return banner[:100]
    except Exception:
        return ""

def scan_ports(hosts):
    print(Style.BRIGHT + "\nStarting port scan...\n")
    results = {}
    lock = threading.Lock()

    def scan_host(ip):
        open_ports = []
        for port in COMMON_PORTS:
            try:
                with socket.socket() as s:
                    s.settimeout(TIMEOUT)
                    if s.connect_ex((ip, port)) == 0:
                        banner = grab_banner(ip, port)
                        open_ports.append((port, banner))
            except Exception:
                continue

        with lock:
            results[ip] = open_ports
            if open_ports:
                for p, b in open_ports:
                    extra = f" | {b}" if b else ""
                    print(Fore.GREEN + f"[+] {ip}:{p} ({COMMON_PORTS[p]}){extra}")
            else:
                print(Fore.RED + f"[-] {ip} (no common ports)")

    with ThreadPoolExecutor(max_workers=THREADS_PORT) as executor:
        futures = [executor.submit(scan_host, ip) for ip in hosts]
        for _ in as_completed(futures):
            pass

    return results

def run_nmap(hosts):
    if not shutil.which("nmap"):
        print(Fore.RED + "[!] Nmap not installed")
        return

    for ip in hosts:
        print(Style.BRIGHT + f"\n[NMAP] {ip}\n")
        try:
            subprocess.run(["nmap", "-sS", "-Pn", "-T4", ip])
        except Exception as e:
            print(Fore.RED + f"[!] Failed: {ip} ({e})")

def save_results(data):
    try:
        with open("scan_results.json", "w") as f:
            json.dump(data, f, indent=2)
        print(Fore.YELLOW + "[i] Saved to scan_results.json")
    except Exception as e:
        print(Fore.RED + f"[!] Save failed: {e}")

def get_base():
    while True:
        base = input("Enter base (first two octets, e.g. 192.168): ").strip()
        if not base:
            print(Fore.YELLOW + "[i] Using default base: 192.168")
            return "192.168"
        base = base.rstrip(".")
        parts = base.split(".")
        if len(parts) != 2:
            print(Fore.RED + "[!] Invalid format. Example: 192.168")
            continue
        try:
            a, b = int(parts[0]), int(parts[1])
            if 0 <= a <= 255 and 0 <= b <= 255:
                return f"{a}.{b}"
        except:
            pass
        print(Fore.RED + "[!] Invalid input")

def get_start():
    while True:
        val = input("Enter START of third octet (0-255): ").strip()
        if not val:
            print(Fore.YELLOW + "[i] Using default START: 0")
            return 0
        try:
            num = int(val)
            if 0 <= num <= 255:
                return num
        except:
            pass
        print(Fore.RED + "[!] Invalid START")

def get_end(start):
    while True:
        val = input("Enter END of third octet (0-255): ").strip()
        if not val:
            print(Fore.YELLOW + "[i] Using default END: 2")
            return 2
        try:
            num = int(val)
            if 0 <= num <= 255 and num >= start:
                return num
        except:
            pass
        print(Fore.RED + "[!] Invalid END")

def main():
    all_hosts = []

    while True:
        if not all_hosts:
            print("Example: 192.168.0.0 to 192.168.2.0\n")
            base = get_base()
            start = get_start()
            end = get_end(start)

            all_hosts = []

            for subnet in range(start, end + 1):
                net = ipaddress.ip_network(f"{base}.{subnet}.0/24", strict=False)
                print(Style.BRIGHT + f"\nScanning {net}...\n")
                found = scan_subnet(net)
                found = sorted(found, key=lambda x: tuple(map(int, x.split("."))))

                if found:
                    for ip in found:
                        print(Fore.GREEN + f"[+] {ip}")
                    all_hosts.extend(found)
                else:
                    print(Fore.RED + "[-] Nothing found in this subnet")

        print("\nOptions:")
        print("1 - Scan again")
        print("2 - Scan common ports")
        print("3 - Run Nmap scan")
        print("4 - Save results")
        print("5 - Exit")

        choice = input("Select: ").strip()
        if choice == "1":
            all_hosts = []
        elif choice == "2":
            if all_hosts:
                scan_ports(all_hosts)
            else:
                print(Fore.RED + "[!] No hosts to scan")
        elif choice == "3":
            if all_hosts:
                run_nmap(all_hosts)
            else:
                print(Fore.RED + "[!] No hosts to scan")
        elif choice == "4":
            if all_hosts:
                save_results({"hosts": all_hosts})
            else:
                print(Fore.RED + "[!] Nothing to save")
        elif choice == "5":
            break
        else:
            print(Fore.RED + "[!] Invalid option")

if __name__ == "__main__":
    main()
