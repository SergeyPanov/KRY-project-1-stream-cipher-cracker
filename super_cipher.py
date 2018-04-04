#!/usr/bin/env python3

import argparse
import sys
import copy
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





# Return previous keystream for next_stream based on guess
def getPrevStream(guess, next_stream):
  for prev_step in guess:
    next_step = step(prev_step)
    if next_step == next_stream:
      return prev_step


########################################################################################################################
def stupid(x, n):
  # print("Original: ")
  # print(x)
  x = (x & 1) << n + 1 | x << 1 | x >> n - 1
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

def getIndexForSub(first_two, sub_value):
  if SUB[(first_two << 1) | 0 ] == sub_value:
    return (first_two << 1) | 0
  else:
    return (first_two << 1) | 1

def constructVector(and_functions, n):
  x = 0
  nn = n - 1
  for function in and_functions:
    val = 1 if function.simplifyed_value.value == True else 0
    x |= (val << nn)
    nn -= 1
  return x

def simpleSatSolver(y, and_functions, initial_number, n):
  nn = n - 1
  msb = (initial_number & 2) >> 1
  lsb = initial_number & 1
  for function in and_functions:
    function.apply(msb, lsb)
    function.simplify()
    sub_value = (y & (1 << nn) ) >> nn
    index = getIndexForSub( ((msb << 1) | lsb), sub_value) & 1
    function.simplifyed_value.value = (index == 1)
    msb = lsb
    lsb = index

    nn -= 1
  return constructVector(and_functions, n)


max_8_bit_val = 0
for i in range(8):
  max_8_bit_val |= 1 << i
def constructFunction(y, n):
  and_functions = []
  for i in range(n - 1, -1, -1):
    sub_value = (y & 1 << i) >> i
    if sub_value == 0:
      or_clauses = [Clause(i, zero_index, False, "and") for zero_index in ZERO_INDEXES]
    else:
      or_clauses = [Clause(i, one_index, False, "and") for one_index in ONE_INDEXES]
    [or_clause.deMorgan() for or_clause in or_clauses]
    and_functions.append(Function(or_clauses[:], 'and', True))
    or_clauses.clear()
  return and_functions




def satDecipher(y, n):
  maybe_x = []
  for i in range(4):
    and_functions = constructFunction(y, n)
    x = simpleSatSolver(y, and_functions, i, n)
    x = (x & 1) << n - 1 | (x & max_256_bit_val) >> 1
    maybe_x.append(x)
  return maybe_x



# NN = 8
# x = 199
# x = stupid(x, NN)

# for i in range(NN//2):
#   print("Prev: {}".format(x))
#   x = stupid(x, NN)
# guess = []
# prev_stream = x

# print(satDecipher(prev_stream, NN))

#
# for i in range(NN//2):
#   guess = satDecipher(prev_stream, NN)
#   prev_stream = getPrevStream(guess, prev_stream, NN)
#   guess.clear()
#
# print("Deciphered: {}".format(prev_stream))

# exit(1)

########################################################################################################################




# Keystream init
keystr = int.from_bytes(args.key.encode(),'little')
print("Initial keystream: {}".format(keystr))
for i in range(N//2):
  keystr = step(keystr)
  print("After step: {}".format(keystr))


guess = []
prev_stream = keystr
for i in range(N//2):
  guess = satDecipher(prev_stream, N)
  prev_stream = getPrevStream(guess, prev_stream)
  guess.clear()

print(prev_stream.to_bytes(N, 'little')[:29].decode())
exit(1)

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