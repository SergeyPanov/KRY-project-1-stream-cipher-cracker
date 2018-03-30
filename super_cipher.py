#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("key")
args = parser.parse_args()

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


# Next keystream
def step(x):
  # print("Original: ")
  # print(x)
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  for i in range(N):
    y |= SUB[(x >> i) & 7] << i
  return y

# Next keystream
def stupid(x):
  print("Original: ")
  print(x)
  x = (x & 1) << 16 + 1 | x << 1 | x >> 16 - 1
  y = 0
  for i in range(16):
    y |= SUB[(x >> i) & 7] << i
  return y


max_16_bit_val = 0
for i in range(16):
  max_16_bit_val |= 1 << i

def deStupid(y, x):
  x = x << 16
  for i in range(16-1, -1, -1):
    sub_value = (y & 1 << i) >> i
    if sub_value == SUB[(7 << i & x) >> i]:
      x |= x
    else:
      x |= 1 << i
  x = (x & 1) << 16-1 | (x & max_16_bit_val) >> 1
  return x


# x = 12324234
# guess = []
# step_y = step(x)
# for i in range(4):
#   guess.append(calculateX(step_y, i))
#
# print(guess)


# print(deStupid(stupidY) == x)

# Keystream init
keystr = int.from_bytes(args.key.encode(),'little')
# for i in range(N//2):
#   keystr = step(keystr)

guess = []
print("Unknown keystream: {}".format(keystr))
next_stream = step(keystr)
print("Unknown next: {}".format(next_stream))
for i in range(4):
  guess.append(calculateX(next_stream, i))

print(guess)

for prev_step in guess:
  next_step = step(prev_step)
  if next_step == next_stream:
    print(prev_step)




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