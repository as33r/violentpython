import argparse
import nmap

def nmap_scan(tgt_host, tgt_port):
    scanner = nmap.PortScanner()
    scanner.scan(tgt_host, tgt_port)
    for host in scanner.all_hosts():
        state = scanner[host]['tcp'][int(tgt_port)]['state']
        print(f"[*] {tgt_host}/{host} tcp/{tgt_port} {state}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", dest="host", help="Give target host name to scan")
    parser.add_argument("-p", "--ports", dest="ports", help="Give port/ports to scan")

    args = parser.parse_args()
    host = args.host
    if not host or not args.ports:
        print("[-] Please give host and ports to scan")
        parser.print_help()
        exit(0)
    ports = args.ports.split(",")
    for port in ports:
        nmap_scan(host, port)

if __name__ == "__main__":
    main()