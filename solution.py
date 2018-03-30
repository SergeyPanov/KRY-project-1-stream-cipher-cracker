SUB = [0, 1, 1, 0, 1, 0, 1, 0]

N_B = 32
N = 8 * N_B
max_256_bit_val = 0
for i in range(N):
  max_256_bit_val |= 1 << i

def calculateX(y, x):
  x = x << N
  for i in range(N-1, -1, -1):
    sub_value = (y & 1 << i) >> i
    if sub_value == SUB[(7 << i & x) >> i]:
      x |= x
    else:
      x |= 1 << i
  x = (x & 1) << N - 1 | (x & max_256_bit_val) >> 1
  return x


# Return previous keystream for next_stream based on guess
def getPrevStream(guess, next_stream):
  for prev_step in guess:
    next_step = step(prev_step)
    if next_step == next_stream:
      return prev_step

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



def getPartialKeystream(plaintext1, ciphertext1):
    firstXor = []
    for plainLine, cipherLine in zip(plaintext1, ciphertext1):
        firstXor = [plainChar ^ cipherChar for (plainChar, cipherChar) in zip(plainLine, cipherLine)]
    return  firstXor

def decode(keystream):
    guess = []
    prev_stream = keystream

    for i in range(N//2):
        for j in range(4):
            guess.append(calculateX(prev_stream, j))
        prev_stream = getPrevStream(guess, prev_stream)
        guess = []
    return prev_stream.to_bytes(N, "little")[:29].decode()


if __name__ == '__main__':
    bis = readFileByBytes("./xpanov00/bis.txt")
    cipherBis = readFileByBytes("./xpanov00/bis.txt.enc")
    partialKeystream = getPartialKeystream(bis, cipherBis)
    print(decode(int.from_bytes(bytes(partialKeystream[0:32]), 'little')))
