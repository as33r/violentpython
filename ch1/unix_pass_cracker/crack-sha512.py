import crypt

def testpass(hash, salt):
    with open("wordlist.txt", "r") as wordlist:
        for word in wordlist:
            word = word.strip()
            word_hash = crypt.crypt(word, salt)
            if hash == word_hash:
                print(f"[+] Password found! {word}")
                return
        print("[-] Password not found")
        return

def main():
    with open("passwd-sha512.txt", "r") as file:
        for line in file:
            if ":" in line:
                user = line.split(":")[0].strip()
                hash = line.split(":")[1].strip()
                salt = "$6$" + hash.split("$")[2]
                print(f"[+] Testing password for user : {user}")
                testpass(hash, salt)

if __name__ == "__main__":
    main()