from commons import *
from logic.Clause import Clause
from logic.Function import Function

def constructVector(and_functions):
  x = 0
  nn = N - 1
  for function in and_functions:
    val = 1 if function.simplifyed_value.value == True else 0
    x |= (val << nn)
    nn -= 1
  return x


def getIndexForSub(first_two, sub_value):
  if SUB[(first_two << 1) | 0 ] == sub_value:
    return (first_two << 1) | 0
  else:
    return (first_two << 1) | 1


def simpleSatSolver(y, and_functions, initial_number):
  nn = N - 1
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
  return constructVector(and_functions)


def constructFunction(y):
  and_functions = []
  for i in range(N - 1, -1, -1):
    sub_value = (y & 1 << i) >> i
    if sub_value == 0:
      or_clauses = [Clause(i, zero_index, False, "and") for zero_index in ZERO_INDEXES]
    else:
      or_clauses = [Clause(i, one_index, False, "and") for one_index in ONE_INDEXES]
    [or_clause.deMorgan() for or_clause in or_clauses]
    and_functions.append(Function(or_clauses[:], 'and', True))
    or_clauses.clear()
  return and_functions



def satDecipher(y):
  maybe_x = []
  for i in range(4):
    and_functions = constructFunction(y)
    x = simpleSatSolver(y, and_functions, i)
    x = (x & 1) << N - 1 | (x & max_256_bit_val) >> 1
    maybe_x.append(x)
  return maybe_x



def decode(keystream):
    guess = []
    prev_stream = keystream
    for i in range(N // 2):
        guess = satDecipher(prev_stream)
        prev_stream = getPrevStream(guess, prev_stream)
        guess.clear()

    return prev_stream.to_bytes(N, "little")[:29].decode()



if __name__ == '__main__':
    bis = readFileByBytes("./in/bis.txt")
    cipherBis = readFileByBytes("./in/bis.txt.enc")
    partialKeystream = getPartialKeystream(bis, cipherBis)
    print(decode(int.from_bytes(bytes(partialKeystream[0:32]), 'little')))
