
# Netscan - Network Scanner

Lightweight multithreaded network scanner written in Python.  
Designed for fast subnet discovery and quick port scan with optional Nmap usage.

## Features

- Subnet scanning across multiple /24 ranges
- Host discovery using:
  - ICMP (ping)
  - TCP fallback (ports 80, 443, 22)
- Multithreaded scanning
- Common port scanning with service labeling
- Basic banner grabbing
- Optional Nmap integration
- JSON export of discovered hosts
- Cross-platform (Windows/Linux)

---

## Installation

```bash
git clone https://github.com/janvsec/Netscan
cd Netscan
pip install colorama
````

Optional (for Nmap scan option):

```bash
sudo apt install nmap
```

---

## Usage

```bash
python netscan.py
```

You will be prompted for subnet range:

```
Example: 192.168.0.0 to 192.168.2.0

Enter base (first two octets, e.g. 192.168):
Enter START of third octet (0-255):
Enter END of third octet (0-255):
```

Defaults (press ENTER):

* Base: `192.168`
* Start: `0`
* End: `2`

---

## Example Output

### Host Discovery

```
Scanning 192.168.0.0/24...

[+] 192.168.0.1
[+] 192.168.0.111
[+] 192.168.0.124
[+] 192.168.0.136
[+] 192.168.0.144
[+] 192.168.0.147
[+] 192.168.0.149
[+] 192.168.0.171
[+] 192.168.0.188
[+] 192.168.0.206
[+] 192.168.0.226
[+] 192.168.0.245
```

```
Scanning 192.168.1.0/24...

[-] Nothing found in this subnet
```

```
Scanning 192.168.2.0/24...

[-] Nothing found in this subnet
```

---

### Port Scan

```
Starting port scan...

[+] 192.168.0.1:53 (DNS)
[+] 192.168.0.1:80 (HTTP) | HTTP/1.1 400 Bad Request
Connection: close
Content-Type: text/plain
Transfer-Encoding: chunked
[+] 192.168.0.1:443 (HTTPS)

[-] 192.168.0.245 (no common ports)
[-] 192.168.0.124 (no common ports)
[-] 192.168.0.149 (no common ports)
[-] 192.168.0.147 (no common ports)
[-] 192.168.0.144 (no common ports)
[-] 192.168.0.111 (no common ports)
[-] 192.168.0.226 (no common ports)
[-] 192.168.0.188 (no common ports)
[-] 192.168.0.171 (no common ports)

[+] 192.168.0.206:80 (HTTP)
[+] 192.168.0.136:443 (HTTPS)
```

---

### Save Results

```
[i] Saved to scan_results.json
```

```json
{
  "hosts": [
    "192.168.0.1",
    "192.168.0.111",
    "192.168.0.124",
    "192.168.0.136",
    "192.168.0.144",
    "192.168.0.147",
    "192.168.0.149",
    "192.168.0.171",
    "192.168.0.188",
    "192.168.0.206",
    "192.168.0.226",
    "192.168.0.245"
  ]
}
```

---

## Menu Options

```
1 - Scan again
2 - Scan common ports
3 - Run Nmap scan
4 - Save results
5 - Exit
```



