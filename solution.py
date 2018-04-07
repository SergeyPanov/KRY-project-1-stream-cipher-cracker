from commons import *

def calculateX(y, x):
  x = x << N
  for i in range(N-1, -1, -1):
    sub_value = (y & 1 << i) >> i
    if sub_value != SUB[(7 << i & x) >> i]:
        x |= 1 << i
  x = (x & 1) << N - 1 | (x & max_256_bit_val) >> 1
  return x


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
    bis = readFileByBytes("./in/bis.txt")
    cipherBis = readFileByBytes("./in/bis.txt.enc")
    partialKeystream = getPartialKeystream(bis, cipherBis)
    print(decode(int.from_bytes(bytes(partialKeystream[0:32]), 'little')))
