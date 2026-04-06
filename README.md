# Simple Network Scanner

## What this does

* Scans a range of subnets for alive hosts using ping
* Lists all responding IPs
* Can scan common ports on found hosts (fast, basic)
* Can run Nmap scan on found hosts (if installed)

## How it works

1. You enter:

   * Base network (first two octets, e.g. `192.168`)
   * Start and end of third octet (e.g. `0` to `2`)
2. Script scans each `/24` subnet in that range
3. Uses ping to check if hosts are alive
4. Stores all alive IPs
5. Lets you choose what to do next:

   * Rescan
   * Scan common ports
   * Run Nmap
   * Exit

## Features

* Multithreaded host discovery (fast)
* Multithreaded port scanning
* Cross-platform ping (Windows/Linux)
* Basic service detection via common ports list
* Optional Nmap integration

## Requirements

* Python 3
* colorama

Install dependency:

```
pip install colorama
```

Optional:

* Nmap (must be in PATH if you want deep scans)

## Usage

```
python scanner.py
```

Example input:

```
Base: 192.168
Start: 0
End: 2
```

This scans:

```
192.168.0.0/24
192.168.1.0/24
192.168.2.0/24
```

## Options

```
1 - Scan again
2 - Scan common ports (fast)
3 - Run Nmap scan (deep)
4 - Exit
```

## Notes

* Ping-based discovery can miss hosts with ICMP disabled
* Port scan is limited to predefined common ports
* Nmap scan uses:

  ```
  nmap -sS -Pn -T4 <ip>
  ```
* High thread count may trigger firewall/IDS in some networks

## Disclaimer

Use only on networks you own or have permission to scan.
