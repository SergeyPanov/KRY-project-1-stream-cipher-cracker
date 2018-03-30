#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("key")
args = parser.parse_args()

SUB = [0, 1, 1, 0, 1, 0, 1, 0]

N_B = 32
N = 8 * N_B

# def calculateY(x):
#   y = keystr
#   for i in range(N-1, -1, -1):
#     y |= SUB[(x << i) & (7 << 255)] >> i
#   return y

# def guessX():
#   for iv in range(8):
#     orgnum = iv << 255
#     calculateY(orgnum)

# Next keystream
def step(x):
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  prev_y = y
  for i in range(N):
    prev_y = y
    y |= SUB[(x >> i) & 7] << i
  return y

# Next keystream
def stupid(x):
  y = 0
  for i in range(8):
    y |= SUB[(x >> i) & 7] << i
  return y

def deStupid(y):
  x = 0
  for i in range(8-1, -1, -1):
    sub_value = (y & 1 << i) >> i
    if sub_value == SUB[(7 << i & x) >> i]:
      x |= x
    else:
      x |= 1 << i
  return x

x = 89
stupidY = stupid(x)
print(deStupid(stupidY) == x)

# Keystream init
keystr = int.from_bytes(args.key.encode(),'little')
for i in range(N//2):
  keystr = step(keystr)

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