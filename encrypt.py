from decrypt import decryptblock
import numpy as np
import sys


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