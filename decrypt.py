from Crypto.Cipher import AES
import subprocess
import sys
import numpy as np

def oracle(ciphertext):
    f = open("tmp.cipher", "wb")
    f.write(ciphertext)
    f.close()
    res = subprocess.check_output(['python3', 'oracle.py', 'tmp.cipher'])
    return int(res.decode()[0]) == 1

# def oracle(ciphertext):
#     key = b'dont use the key'
#     iv = b'ABCDEFGHabcdefgh'

#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     plaintext = cipher.decrypt(ciphertext)
#     #last byte tells us how much padding there is
#     padnum = 16 - plaintext[-1]
#     if padnum <= 0:
#         return False
#     passed_check = True
#     for i in range(padnum):
#         if plaintext[-i-1] != 16 - padnum:
#             passed_check = False
#             break
#     return passed_check



def decryptbyte(rs, yn, k):
    for i in range(k+1, 16):
        rs[i] ^= k
    
    for i in range(256):
        rs[k] = i
        guess = bytes(rs + yn)
        if oracle(guess):
            break
    
    if k == 15:

        for i in range(k):
            init = rs[i]
            for j in range(255):
                rs[i] = (init + j) % 256
                guess = bytes(rs + yn)
                if oracle(guess):
                    break
                else:
                    rs[k] ^= i

    rs[k] ^= k

    for i in range(k+1, 16):
        rs[i] ^= k

    return rs

def decryptblock(yn):
    rs = bytearray(list(np.random.randint(low=0, high=256, size=16)))
    for k in range(16):
        rs = decryptbyte(rs, yn, 15-k)
    return rs

def decrypt(ciphertext):
    size = len(ciphertext)
    if size <= 16:
        return

    xn = bytes()

    for i in range(size, 16, -16):
        yn = ciphertext[i-16:i]
        yn1 = ciphertext[i-32:i-16]
        dyn = decryptblock(yn)
        xn = bytes(a ^ b for a, b in zip(dyn, yn1)) + xn

    padnum = xn[-1]
    xn = xn[:padnum-16]
        
    return xn

def main():
    f = open(sys.argv[1], "rb")
    ciphertext = f.read()
    f.close()
    plaintext = decrypt(ciphertext)
    print(plaintext.decode())

if __name__ == '__main__':
    main()