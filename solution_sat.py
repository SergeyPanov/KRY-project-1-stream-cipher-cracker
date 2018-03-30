#!/usr/bin/env python

count_solutions=True
#count_solutions=False

import sys

def read_text_file (fname):
    with open(fname) as f:
        content = f.readlines()
    return [x.strip() for x in content]

def read_DIMACS (fname):
    content=read_text_file(fname)

    header=content[0].split(" ")

    assert header[0]=="p" and header[1]=="cnf"
    variables_total, clauses_total = int(header[2]), int(header[3])

    # array idx=number (of line) of clause
    # val=list of terms
    # term can be negative signed integer
    clauses=[]
    for c in content[1:]:
        if c.startswith ("c "):
            continue
        clause=[]
        for var_s in c.split(" "):
            var=int(var_s)
            if var!=0:
                clause.append(var)
        clauses.append(clause)

    # this is variables index.
    # for each variable, it has list of clauses, where this variable is used.
    # key=variable
    # val=list of numbers of clause
    variables_idx={}
    for i in range(len(clauses)):
        for term in clauses[i]:
            variables_idx.setdefault(abs(term), []).append(i)

    return clauses, variables_idx

# clause=list of terms. signed integer. -x means negated.
# values=list of values: from 0th: [F,F,F,F,T,F,T,T...]
def eval_clause (terms, values):
    try:
        # we search for at least one True
        for t in terms:
            # variable is non-negated:
            if t>0 and values[t-1]==True:
                return True
            # variable is negated:
            if t<0 and values[(-t)-1]==False:
                return True
        # all terms enumerated at this point
        return False
    except IndexError:
        # values[] has not enough values
        # None means "maybe"
        return None

def chk_vals(clauses, variables_idx, vals):
    # check only clauses which affected by the last (new/changed) value, ignore the rest
    # because since we already got here, all other values are correct, so no need to recheck them
    idx_of_last_var=len(vals)
    # variable can be absent in index, because no clause uses it:
    if idx_of_last_var not in variables_idx:
        return True
    # enumerate clauses which has this variable:
    for clause_n in variables_idx[idx_of_last_var]:
        clause=clauses[clause_n]
        # if any clause evaluated to False, stop checking, new value is incorrect:
        if eval_clause (clause, vals)==False:
            return False
    # all clauses evaluated to True or None ("maybe")
    return True

def print_vals(vals):
    # enumerate all vals[]
    # prepend "-" if vals[i] is False (i.e., negated).
    print( "".join([["-",""][vals[i]] + str(i+1) + " " for i in range(len(vals))])+"0")

clauses, variables_idx = read_DIMACS(sys.argv[1])

solutions=0

def backtrack(vals):
    global solutions

    if len(vals)==len(variables_idx):
        # we reached end - all values are correct
        print( "SAT")
        print_vals(vals)
        if count_solutions:
            solutions=solutions+1
            # go back, if we need more solutions:
            return
        else:
            exit(10) # as in MiniSat
        return

    for next in [False, True]:
        # add new value:
        new_vals=vals+[next]
        if chk_vals(clauses, variables_idx, new_vals):
            # new value is correct, try add another one:
            backtrack(new_vals)
        else:
            # new value (False) is not correct, now try True (variable flip):
            continue

# try to find all values:
backtrack([])
print ("UNSAT")
if count_solutions:
    print( "solutions=", solutions)
exit(20) # as in MiniSat