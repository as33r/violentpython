from pexpect import pxssh

class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as err:
            print("[-] Error : " + str(err))
            print("[-] Error Connecting ......")
    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before.decode("utf-8")

def botnet_command(command):
    for bot in bot_net:
        output = bot.send_command(command)
        print(f"[+] '{command}' output from {bot.host}  " )
        print(output)

def add_client(host, user, password):
    client = Client(host, user, password)
    bot_net.append(client)

bot_net = []

add_client("localhost", "kali", "kali")
add_client("172.16.0.128", "moris", "moris")

botnet_command("uname -a")
botnet_command("cat /etc/issue")
