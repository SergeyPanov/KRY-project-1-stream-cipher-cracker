from itertools import cycle

SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B

# Next keystream
def step(x):
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  for i in range(N):
    y |= SUB[(x >> i) & 7] << i
  return y

def readFileByBytes(file):
    byteFile = []
    with open(file, "rb") as f:
        byteFile.append(f.read())
    return byteFile

def writeFileByBytes(file, content):
    with open(file, "wb") as output:
        output.write(content)


def expendKey(seed, length):
    next_part = seed
    expended_key = bytes(next_part)
    while len(expended_key) < length:
        next_part = step(int.from_bytes(bytes(next_part), 'little')).to_bytes(32, 'little')
        expended_key = expended_key + next_part

    return expended_key

def decodeFile(input, output, partialKeystream):
    firstPart = partialKeystream[0:32]
    expended_key = expendKey(firstPart, len(input))
    content = bytes([keyChar ^ cipherChar for (keyChar, cipherChar) in zip(expended_key, input)])
    writeFileByBytes(output, content)



def getPartialKeystream(plaintext1, ciphertext1, ciphertext2):

    firstXor = []
    for plainLine, cipherLine in zip(plaintext1, ciphertext1):
        firstXor = [plainChar ^ cipherChar for (plainChar, cipherChar) in zip(plainLine, cipherLine)]

    return  firstXor
    # secondXor = []
    # for cipherLine in ciphertext2:
    #     secondXor = [cipherChar1 ^ cipherChar2 for (cipherChar1, cipherChar2) in zip(firstXor, cipherLine)]
    #
    # return secondXor

if __name__ == '__main__':
    bis = readFileByBytes("./xpanov00/bis.txt")
    cipherBis = readFileByBytes("./xpanov00/bis.txt.enc")
    # decrypt(bis, cipherBis, cipherBis)
    superCipher = readFileByBytes("./xpanov00/super_cipher.py.enc")
    hintGif = readFileByBytes("./xpanov00/hint.gif.enc")
    partialKeystream = getPartialKeystream(bis, cipherBis, superCipher)
    decodeFile(hintGif[0], "./hint.gif", partialKeystream)
    decodeFile(superCipher[0], "./super_cipher2.py", partialKeystream)
