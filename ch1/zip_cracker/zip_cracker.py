import zipfile
from threading import Thread
import optparse

def brute_force(zfile, password):
    try:
        zfile.extractall(pwd=password)
        password = password.decode("utf-8")
        print(f"[+] Password found {password}")
    except:
        pass

def main():
    # creating commanline options with optparse lib
    parser = optparse.OptionParser("usage%prog" + " -f <zip file> -d <dictionary file>")
    parser.add_option("-f", dest="zip_file", type="string", help="Specify zip file")
    parser.add_option("-d", dest="dict_file", type="string", help="Specify wordlist")
    (option, agrs) = parser.parse_args()
    if option.zip_file == None or option.dict_file == None:
        print(parser.usage)
        exit(0)
    else:
        zname = option.zip_file
        wordlist = option.dict_file
    #creating zipfile object.
    zfile = zipfile.ZipFile(zname)
    print("[+] Brute-forcing passwords")
    with open(wordlist, "r")as wordlist:
        for word in wordlist:
            password = bytes(word.strip(), "utf-8")
            # creating threads to run bruteforcing in threads to speed up.
            thread = Thread(target=brute_force, args=(zfile, password))
            thread.start()

if __name__ == "__main__":
    main()