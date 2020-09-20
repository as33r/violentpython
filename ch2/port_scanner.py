from socket import *
import argparse
from threading import *

def conn_scan(tgt_host, tgt_port):
    screen_lock = Semaphore(value=1)
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((tgt_host, tgt_port))
        s.send(b"ViolentPython\r\n")
        results = s.recv(100)
        results = str(results.decode("utf-8"))
        screen_lock.acquire()
        print(f"[+] Port {tgt_port}  is open")
        print(f"[+] {results} ")
    except Exception as err:
        screen_lock.acquire()
        print(f"[-] Port {tgt_port} is not open")
    finally:
        screen_lock.release()
        s.close()

def port_scan(tgt_host, tgt_ports):
    try:
        tgtIP = gethostbyname(tgt_host)
    except:
        print(f"[-] Cannot resolve {tgt_host}, Unknown host")
        return
    try:
        tgt_name = gethostbyaddr(tgtIP)
        print(f"[+] Scan results for:  {tgt_name[0]} ")
    except:
        print(f"[+] Scan results for : {tgtIP}")

    setdefaulttimeout(1)
    for port in tgt_ports:
        # print(f"[+] Scanning port :  {port}")
        # conn_scan(tgt_host, int(port))
        thread = Thread(target=conn_scan, args=(tgt_host, int(port)))
        thread.start()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", dest="host", help="Give target host name to scan")
    parser.add_argument("-p", "--ports", dest="ports", help="Give port/ports to scan")

    args = parser.parse_args()
    host = args.host
    ports = args.ports.split(",")
    if not host or not ports:
        print("[-] Please give host and ports to scan")
        parser.print_help()
        exit(0)
    port_scan(host, ports)

if __name__ == "__main__":
    main()


