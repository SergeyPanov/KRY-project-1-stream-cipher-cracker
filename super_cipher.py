#!/usr/bin/env python3

import argparse
import sys
from logic.Clause import Clause
from logic.Function import Function

parser = argparse.ArgumentParser()
parser.add_argument("key")
args = parser.parse_args()

SUB = [0, 1, 1, 0, 1, 0, 1, 0]

ZERO_INDEXES = [0, 3, 5, 7]
ONE_INDEXES = [1, 2, 4, 6]


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


# Next keystream
def step(x):
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  for i in range(N):
    y |= SUB[(x >> i) & 7] << i
  return y

########################################################################################################################
def stupid(x, n):
  # print("Original: ")
  # print(x)
  # x = (x & 1) << n + 1 | x << 1 | x >> n - 1
  y = 0
  for i in range(n):
    y |= SUB[(x >> i) & 7] << i
  return y

max_4_bit_val = 0
for i in range(4):
  max_4_bit_val |= 1 << i

def deStupid(y, x, n):
  x = x << n
  for i in range(n-1, -1, -1):
    sub_value = (y & 1 << i) >> i
    if sub_value == SUB[(7 << i & x) >> i]:
      x |= x
    else:
      x |= 1 << i
  x = (x & 1) << n-1 | (x & max_4_bit_val) >> 1
  return x


def satDecipher(y, x, n):
  x = x << n
  and_clauses = []
  for i in range(n-1, -1, -1):
    sub_value = (y & 1 << i) >> i
    if sub_value == 0:
      or_clauses = [Clause(i, zero_index, False, "and") for zero_index in ZERO_INDEXES]
    else:
      or_clauses = [Clause(i, one_index, False, "and") for one_index in ONE_INDEXES]

    [or_clause.deMorgan() for or_clause in or_clauses]
    and_clauses += or_clauses
    or_clauses.clear()

  fun = Function(and_clauses, 'and', False)



x = 10
y = stupid(x, 4)
satDecipher(y, 0, 4)



initial_key = int.from_bytes("KRY".encode(), "little")
initial_key = stupid(initial_key, 24)
full_key = ""

# key_length = 4
# def satSolver(key):
#
#   if stupid(int.from_bytes(key.encode(), 'little'), 24) == initial_key:
#     print(key)
#     return
#
#   for i in range(256):
#     if len(key) < key_length:
#       satSolver(key + chr(i))
#     else:
#       return
#
# for i in range(256):
#   satSolver(chr(i))

# SAT solver
# Through all symbols from ASCII table
mask = 255 # Takes least 8 bits, 1111 1111
shift_bits = 0
for i in range(3):  # For each ciphered Byte
  for j in range(256): # For each ASCII chart
    ch = chr(j)
    if (initial_key & mask << shift_bits) == (stupid(int.from_bytes((ch + reversed(full_key)).encode(), 'little'), 24) & mask):
      full_key += ch
      shift_bits += 8
    pass

print(full_key)

########################################################################################################################



# Return previous keystream for next_stream based on guess
def getPrevStream(guess, next_stream):
  for prev_step in guess:
    next_step = step(prev_step)
    if next_step == next_stream:
      return prev_step

# Keystream init
keystr = int.from_bytes(args.key.encode(),'little')
print("Initial keystream: {}".format(keystr))
for i in range(N//2):
  keystr = step(keystr)
  print("After step: {}".format(keystr))

# guess = []
# prev_stream = keystr
#
# for i in range(N//2):
#   for i in range(4):
#     guess.append(calculateX(prev_stream, i))
#
#   prev_stream = getPrevStream(guess, prev_stream)
#   guess = []
#
# print("Decipher initial: {}".format(prev_stream))
# print(prev_stream.to_bytes(N, "little")[:29].decode())


# guessedX = guessX()

# Encrypt/decrypt stdin2stdout 
# plaintext = sys.stdin.buffer.read(N_B)
# while plaintext:
#   sys.stdout.buffer.write((
#     int.from_bytes(plaintext,'little') ^ keystr
#   ).to_bytes(N_B,'little'))
#   keystr = step(keystr)
#   plaintext = sys.stdin.buffer.read(N_B)
#