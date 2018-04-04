#!/usr/bin/env python3

import argparse
import sys
import copy

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
    for key, value in function.items():
      val = int( value["value"] )
      x |= (val << nn)
    nn -= 1
  return x


def applyClause(msb, lsb, clause):

  for key, value in clause[0].items():
    clause[0][key]["value"] = msb

  for key, value in clause[1].items():
    clause[1][key]["value"] = lsb

  return clause

def silifyClause(clause):
  for term in clause:
    for key, value in term.items():
      if value["value"] != None:
        if value["is_negated"]:
          if not value["value"]:
            return True
        else:
          if value["value"]:
            return True

  return clause[2]

def applyFunc(msb, lsb, function):
  return [applyClause(msb, lsb, clause) for clause in function]

def simplify(function):
  simplified_function = None
  for clause in function:
    res = silifyClause(clause)
    if res != True:
      simplified_function = res
  return simplified_function

def simpleSatSolver(y, and_functions, initial_number, n):
  nn = n - 1
  msb = (initial_number & 2) >> 1
  lsb = initial_number & 1
  simple_functions = []
  for function in and_functions:
    applyFunc(msb, lsb, function)
    function = simplify(function)

    sub_value = (y & (1 << nn) ) >> nn
    index = getIndexForSub( ((msb << 1) | lsb), sub_value) & 1
    for key, value in function.items():
      value["value"] = (index == 1)

    simple_functions.append(function)
    msb = lsb
    lsb = index
    nn -= 1
  return constructVector(simple_functions, n)


max_8_bit_val = 0
for i in range(8):
  max_8_bit_val |= 1 << i

def generateOrClause(bit_index, value_index):
  terms = []
  terms.append({"x" + str(bit_index + 2): {"is_negated": (4 & value_index) == 0, "value": None}})
  terms.append({"x" + str(bit_index + 1): {"is_negated": (2 & value_index) == 0, "value": None}})
  terms.append({"x" + str(bit_index): {"is_negated": (1 & value_index) == 0, "value": None}})
  return terms

def deMorgan(clause):
  for term in clause:
    for key, value in term.items():
      term[key]["is_negated"] = not term[key]["is_negated"]

  return clause


def constructFunction(y, n):
  and_functions = []
  for i in range(n - 1, -1, -1):
    sub_value = (y & 1 << i) >> i
    if sub_value == 0:
      or_clauses = [generateOrClause(i, zero_index) for zero_index in ZERO_INDEXES]
    else:
      or_clauses = [generateOrClause(i, one_index) for one_index in ONE_INDEXES]
    and_functions.append([deMorgan(clause) for clause in or_clauses])
    or_clauses.clear()
  return and_functions


def satDecipher(y, n):
  maybe_x = []
  and_functions = constructFunction(y, n)
  for i in range(4):
    x = simpleSatSolver(y, and_functions[:], i, n)
    x = (x & 1) << n - 1 | (x & max_256_bit_val) >> 1
    maybe_x.append(x)
  return maybe_x



# NN = 8
# x = 215
# # y = stupid(x, NN)
#
# for i in range(NN//2):
#   print("Prev: {}".format(x))
#   x = stupid(x, NN)
# guess = []
# prev_stream = x
#
#
# for i in range(NN//2):
#   guess = satDecipher(prev_stream, NN)
#   prev_stream = getPrevStream(guess, prev_stream, NN)
#   guess.clear()
#
# print("Deciphered: {}".format(prev_stream))
#
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