"""
Common module.
Holds variables and functions used in both solutions.
"""

# Substitution vector
SUB = [0, 1, 1, 0, 1, 0, 1, 0]

# Indexes of 0s and 1s
ZERO_INDEXES = [0, 3, 5, 7]
ONE_INDEXES = [1, 2, 4, 6]

N_B = 32
N = 8 * N_B
# Init max value on 256 bits
max_256_bit_val = 0
for i in range(N):
    max_256_bit_val |= 1 << i


def readFileByBytes(file):
    """
    Reads input file as bytes
    :param file: path to the file
    :return: read butes
    """
    byteFile = []
    with open(file, "rb") as f:
        byteFile.append(f.read())
    return byteFile


def getPartialKeystream(plaintext1, ciphertext1):
    """
    Make xor operation between plaintext and ciphered text.
    :param plaintext1: Plaintext
    :param ciphertext1: Ciphered text
    :return: key
    """
    firstXor = []
    for plainLine, cipherLine in zip(plaintext1, ciphertext1):
        firstXor = [plainChar ^ cipherChar for (plainChar, cipherChar) in zip(plainLine, cipherLine)]
    return firstXor


def step(x):
    """
    Used for generating next key
    :param x: previous key
    :return: new key
    """
    x = (x & 1) << N + 1 | x << 1 | x >> N - 1
    y = 0
    for i in range(N):
        y |= SUB[(x >> i) & 7] << i
    return y


def getPrevStream(guess, next_stream):
    """
    Return right previous key.
    Basically takes array with guesses and try to apply step(x) function.
    :param guess: guessed values
    :param next_stream: new stream
    :return: previous stream
    """
    for prev_step in guess:
        next_step = step(prev_step)
        if next_step == next_stream:
            return prev_step
