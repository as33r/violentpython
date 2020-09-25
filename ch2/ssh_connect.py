import pexpect

# ssh connect using pexpect library.
PROMT = ["# ", ">>> ", "> ", "\$ "]
def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMT)
    print(child.before.decode("utf-8"))

def connect(host, user, passwd):
    ssh_newkey = "Are you sure you want to continue connecting"
    conn_string = "ssh " + user + "@" + host
    child = pexpect.spawn(conn_string)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, "[P|p]assword:"])
    if ret == 0:
        print("[-] Error connecting ")
        return
    elif ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, "[P|p]assword:"])
        if ret == 0:
            print("[-] Error connecting..")
            return
        child.sendline(passwd)
        child.expect(PROMT)
        return child
    else:
        child.sendline(passwd)
        child.expect(PROMT)
        return child

def main():
    host = "localhost"
    user = "kali"
    passwd = 'kali'
    child = connect(host, user, passwd)
    cmd = "cat /etc/shadow | head -n 1"
    if child:
        send_command(child, cmd)
    else:
        print("[-] something went wrong")

if __name__ == "__main__":
    main()