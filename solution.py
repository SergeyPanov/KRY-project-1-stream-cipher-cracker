"""
Execute basic solution.
"""
from commons import *


def calculateX(y, x):
    """
    Calculate previous X based on actual Y
    :param y: y
    :param x: x
    :return: previous x
    """
    x = x << N
    for i in range(N - 1, -1, -1):
        sub_value = (y & 1 << i) >> i
        if sub_value != SUB[(7 << i & x) >> i]:
            x |= 1 << i
    x = (x & 1) << N - 1 | (x & max_256_bit_val) >> 1
    return x


def decode(keystream):
    """
    Execute decode process.
    Guess first 2 bits and using getPrevStream() function store right previous key.
    :param keystream: actual keystream
    :return: previous key
    """
    guess = []
    prev_stream = keystream
    for i in range(N // 2):
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
