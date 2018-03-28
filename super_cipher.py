#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("key")
args = parser.parse_args()

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

# Keystream init
keystr = int.from_bytes(args.key.encode(),'little')
for i in range(N//2):
  keystr = step(keystr)

# Encrypt/decrypt stdin2stdout 
plaintext = sys.stdin.buffer.read(N_B)
while plaintext:
  sys.stdout.buffer.write((
    int.from_bytes(plaintext,'little') ^ keystr
  ).to_bytes(N_B,'little'))
  keystr = step(keystr)
  plaintext = sys.stdin.buffer.read(N_B)
  