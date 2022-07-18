from Crypto.Cipher import AES

key = b'dont use the key'
iv = b'ABCDEFGHabcdefgh'
msg = bytearray(b'a white rabbit with pink eyes')

#padding
rounddown = int((len(msg))/16) * 16
diff = len(msg) - rounddown

for i in range(16 - diff):
    msg.append(diff)
#encrypt
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(bytes(msg))

f = open("ciphertext", "wb")
f.write(iv)
f.write(ciphertext)
f.close()
