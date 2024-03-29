"""
Execute decoding using SAT-solver with custom DPLL implementation.
"""
from commons import *


def constructVector(and_functions):
    """
    Construct result vector X based on calculated logic function F.
    :param and_functions: Calculated logic function F, constructed by several smaller logic functions
    :return: constructed vector X
    """
    x = 0
    nn = N - 1
    for function in and_functions:
        for key, value in function.items():
            val = int(value["value"])
            x |= (val << nn)
        nn -= 1
    return x


def getIndexForSub(first_two, sub_value):
    """
    Based on 2 left most bits and value in SUB vectors return index
    :param first_two: 2 left most bits
    :param sub_value: value from SUB vector
    :return: right index
    """
    if SUB[(first_two << 1) | 0] == sub_value:
        return (first_two << 1) | 0
    else:
        return (first_two << 1) | 1


def applyClause(msb, lsb, clause):
    """
    Apply 2 left most bits on clause
    :param msb:
    :param lsb:
    :param clause:
    :return: claus after application
    """
    for key, value in clause[0].items():
        clause[0][key]["value"] = msb

    for key, value in clause[1].items():
        clause[1][key]["value"] = lsb

    return clause


def simplifyClause(clause):
    """
    Simplified clause.
    Simplified clause is 1 or xi
    :param clause:
    :return: simplified clause
    """
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
    """
    Execute application msb and lsb on logic function.
    :param msb:
    :param lsb:
    :param function:
    :return:
    """
    return [applyClause(msb, lsb, clause) for clause in function]


def simplify(function):
    """
    Simplification of whole function F
    :param function:
    :return:
    """
    simplified_function = None
    for clause in function:
        res = simplifyClause(clause)
        if res != True:
            simplified_function = res
    return simplified_function


def simpleSatSolver(y, and_functions, initial_number):
    """
    Simplified implementation of DPLL algorithm.
    :param y:
    :param and_functions:
    :param initial_number:
    :return:
    """
    nn = N - 1
    msb = (initial_number & 2) >> 1
    lsb = initial_number & 1
    simple_functions = []
    for function in and_functions:
        applyFunc(msb, lsb, function)
        function = simplify(function)

        sub_value = (y & (1 << nn)) >> nn
        index = getIndexForSub(((msb << 1) | lsb), sub_value) & 1
        for key, value in function.items():
            value["value"] = (index == 1)

        simple_functions.append(function)
        msb = lsb
        lsb = index
        nn -= 1
    return constructVector(simple_functions)


def generateOrClause(bit_index, value_index):
    """
    Create clause with logical or between terms.
    :param bit_index:
    :param value_index:
    :return:
    """
    terms = []
    terms.append({"x" + str(bit_index + 2): {"is_negated": (4 & value_index) == 0, "value": None}})
    terms.append({"x" + str(bit_index + 1): {"is_negated": (2 & value_index) == 0, "value": None}})
    terms.append({"x" + str(bit_index): {"is_negated": (1 & value_index) == 0, "value": None}})
    return terms


def deMorgan(clause):
    """
    Apply De Morgan's laws on clause.
    :param clause:
    :return:
    """
    for term in clause:
        for key, value in term.items():
            term[key]["is_negated"] = not term[key]["is_negated"]

    return clause


def constructFunction(y):
    """
    Construct logical function F based on key y
    :param y:
    :return:
    """
    and_functions = []
    for i in range(N - 1, -1, -1):
        sub_value = (y & 1 << i) >> i
        if sub_value == 0:
            or_clauses = [generateOrClause(i, zero_index) for zero_index in ZERO_INDEXES]
        else:
            or_clauses = [generateOrClause(i, one_index) for one_index in ONE_INDEXES]
        and_functions.append([deMorgan(clause) for clause in or_clauses])
        or_clauses.clear()
    return and_functions


def satDecipher(y):
    """
    Guess 2 left most bits and execute solution with SAT-solver for each combination of bits.
    :param y:
    :return:
    """
    maybe_x = []
    and_functions = constructFunction(y)
    for i in range(4):
        x = simpleSatSolver(y, and_functions[:], i)
        x = (x & 1) << N - 1 | (x & max_256_bit_val) >> 1
        maybe_x.append(x)
    return maybe_x


def decode(keystream):
    """
    Execute decode process N//2 times.
    :param keystream:
    :return:
    """
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
