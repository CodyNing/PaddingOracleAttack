# from decrypt import decryptblock
from Crypto.Cipher import AES
import numpy as np
import sys
import subprocess

def oracle(ciphertext):
    f = open("zna3tmp.cipher", "wb")
    f.write(ciphertext)
    f.close()
    res = subprocess.check_output(['python3', 'oracle.py', 'zna3tmp.cipher'])
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

def bxor(a: bytearray, b: bytearray):
    return bytes(i ^ j for i, j in zip(a, b))

def bytepad(ptext : str):
    ptextbytes = bytearray(ptext.encode())
    rounddown = int((len(ptextbytes))/16) * 16
    diff = len(ptextbytes) - rounddown

    for i in range(16 - diff):
        ptextbytes.append(diff)

    return ptextbytes

def blocksplit(ptextbytes : bytearray):
    ptextblocks = []
    for i in range(0, len(ptextbytes), 16):
        ptextblocks.append(ptextbytes[i:i+16])

    return ptextblocks

def encryptblocks(ptextblocks):
    rs = bytes(list(np.random.randint(low=0, high=256, size=16)))
    c = [None for _ in range(len(ptextblocks))]
    c[-1] = rs

    for i in range(len(ptextblocks)-1, 0, -1):
        c[i-1] = bxor(ptextblocks[i], decryptblock(c[i]))

    iv = bxor(ptextblocks[0], decryptblock(c[0]))

    return b''.join([iv] + c)

def main():
    plaintext = sys.argv[1]
    ptextbytes = bytepad(plaintext)
    ptextblocks = blocksplit(ptextbytes)
    ciphertext = encryptblocks(ptextblocks)
    print(ciphertext)

if __name__ == '__main__':
    main()