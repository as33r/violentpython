import crypt

def testpass(hash, salt):
    with open("wordlist.txt", "r") as wordlist:
        for word in wordlist:
            word = word.strip()
            word_hash = crypt.crypt(word, salt)
            if hash == word_hash:
                print(f"[+] Password found : {word}")
                return
        print("[-] Password not found")

def main():
    with open("passwd.txt", "r") as file:
        for line in file:
            if ":" in line:
                user = line.split(":")[0].strip()
                hash = line.split(":")[1].strip()
                salt = hash[:2]
                print(f"[+] Cracking Password for User : {user}")
                testpass(hash, salt)

if __name__ == "__main__":
    main()