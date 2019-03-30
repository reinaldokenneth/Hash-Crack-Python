import hashlib
import time
hashtocrack = ["d100a05fa639c32e26d159d131d1fe1b","98abe3a28383501f4bfd2d9077820f11","ec0e2603172c73a8b644bb9456c1ff6e","70090d3b9c2cc498a35a8a93c2a5b4b1"]

def main(hashtocrack):
    start = time.time()
    with open('wordlist.txt','r',encoding='latin-1') as wordlist:
        for line in wordlist:
            line = line.strip()
            if hashlib.md5(line.encode('utf-8')).hexdigest() == hashtocrack:
                print('Cracked')
                end = time.time()
                t_time = end - start
                print("total runtime -- ",t_time,"second")
                return ""
    print("Failed to crack")
    
if __name__ == "__main__":
    for hashcrack in hashtocrack:
        main(hashcrack)