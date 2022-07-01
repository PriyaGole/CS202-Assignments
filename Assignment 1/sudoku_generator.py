# IMPORT the imp packages
from hashlib import new
from pysat.solvers import Solver
from pysat.formula import CNF
import numpy as np
import pandas as pd
import itertools
import random

# Finding the digits in maximum number of sudoku to help in encoding
def num_digits(k):
    count = 0
    num = k * k
    while num != 0:
        count += 1
        num = num // 10
    return count


# Taking the INPUT
k = int(input("Type the parameter k: "))
sudoku = pd.DataFrame(np.zeros((2*k*k, k*k), dtype=np.int32))

val = num_digits(k)


# Splitting the sudoku dataframe into two sudokus
sudoku1 = sudoku[: k * k]  # SUDOKU 1
sudoku2 = sudoku[k * k :]  # SUDOKU 2


# Declaring the encoder for the variables to be used in the CNF formulas
def encode_id(val, r, c, k, n, s):
    id = s * (10 ** (3 * val)) + r * (10 ** (2 * val)) + c * (10 ** (val)) + n
    return id


# Storing the variables for sudoku 1 in arr1
arr1 = list()

for r in range(0, k * k):
    arr1.append([])
    for c in range(0, k * k):
        arr1[r].append([])
        for n in range(0, k * k):
            arr1[r][c].append(encode_id(val, r + 1, c + 1, k, n + 1, 1))


# Storing the variables for sudoku 2 in arr2
arr2 = list()

for r in range(0, k * k):
    arr2.append([])
    for c in range(0, k * k):
        arr2[r].append([])
        for n in range(0, k * k):
            arr2[r][c].append(encode_id(val, r + 1, c + 1, k, n + 1, 2))


# Initialising the solver
solver = Solver()


# Adding pre-condition clauses as given in the test input file
for c in range(0, k * k):
    for r in range(0, k * k):
        if sudoku1[r][c] != 0:
            n = sudoku1[r][c]
            solver.add_clause([arr1[c][r][n - 1]])
        if sudoku2[r][k * k + c] != 0:
            n = sudoku2[r][k * k + c]
            solver.add_clause([arr2[c][r][n - 1]])


# Initialising the rules for sudoku and adding the clauses in the solver
def sudoku_rules(solver):

    # row has each number once
    for r in range(1, k * k + 1):
        for n in range(1, k * k + 1):
            solver.add_clause([arr1[r - 1][c - 1][n - 1] for c in range(1, k * k + 1)])
            solver.add_clause([arr2[r - 1][c - 1][n - 1] for c in range(1, k * k + 1)])
            for c1, c2 in itertools.combinations(range(1, k * k + 1), 2):
                solver.add_clause(
                    [-arr1[r - 1][c1 - 1][n - 1], -arr1[r - 1][c2 - 1][n - 1]]
                )
                solver.add_clause(
                    [-arr2[r - 1][c1 - 1][n - 1], -arr2[r - 1][c2 - 1][n - 1]]
                )

    # column has each number once
    for c in range(1, k * k + 1):
        for n in range(1, k * k + 1):
            solver.add_clause([arr1[r - 1][c - 1][n - 1] for r in range(1, k * k + 1)])
            solver.add_clause([arr2[r - 1][c - 1][n - 1] for r in range(1, k * k + 1)])
            for r1, r2 in itertools.combinations(range(1, k * k + 1), 2):
                solver.add_clause(
                    [-arr1[r1 - 1][c - 1][n - 1], -arr1[r2 - 1][c - 1][n - 1]]
                )
                solver.add_clause(
                    [-arr2[r1 - 1][c - 1][n - 1], -arr2[r2 - 1][c - 1][n - 1]]
                )

    # each cell is filled
    for r, c in itertools.product(range(1, k * k + 1), repeat=2):
        solver.add_clause([arr1[r - 1][c - 1][n - 1] for n in range(1, k * k + 1)])
        solver.add_clause([arr2[r - 1][c - 1][n - 1] for n in range(1, k * k + 1)])
        for n1, n2 in itertools.combinations(range(1, k * k + 1), 2):
            solver.add_clause(
                [-arr1[r - 1][c - 1][n1 - 1], -arr1[r - 1][c - 1][n2 - 1]]
            )
            solver.add_clause(
                [-arr2[r - 1][c - 1][n1 - 1], -arr2[r - 1][c - 1][n2 - 1]]
            )

    # for each box each number occurs once
    for i, j in itertools.product([num for num in range(1, k * k + 1, k)], repeat=2):
        for n in range(1, k * k + 1):
            solver.add_clause(
                [
                    arr1[i + del_r - 1][j + del_c - 1][n - 1]
                    for del_r, del_c in itertools.product(
                        [x for x in range(k)], repeat=2
                    )
                ]
            )
            solver.add_clause(
                [
                    arr2[i + del_r - 1][j + del_c - 1][n - 1]
                    for del_r, del_c in itertools.product(
                        [x for x in range(k)], repeat=2
                    )
                ]
            )


    # pair wise no same element
    for r in range(1, k * k + 1):
        for c in range(1, k * k + 1):
            for n in range(1, k * k + 1):
                rel = list()
                rel.append(-arr1[r - 1][c - 1][n - 1])
                rel.append(-arr2[r - 1][c - 1][n - 1])
                solver.add_clause(rel)


# Adding the clauses to the solver
sudoku_rules(solver)


# Solving the model
if solver.solve():
    # Getting the model in a list to iterate through
    res = solver.get_model()

    # Saving the numbers in the sudoku dataframe
    for i in res:
        if i > 0:
            str1 = str(i)
            s = int(str1[0])
            if s == 1:
                r = int(str1[1 : val + 1])
                c = int(str1[val + 1 : val + val + 1])
                n = int(str1[2 * (val) + 1 :])

                sudoku[c - 1][r - 1] = n

            else:
                r = int(str1[1 : val + 1])
                c = int(str1[val + 1 : val + val + 1])
                n = int(str1[2 * (val) + 1 :])

                sudoku[c - 1][k * k + r - 1] = n

    # Adding the encoding variables of the get_model() in solution list
    solution=[v for v in res if v>0]

    # Adding the negate of these solutions clauses encoding in the solver
    solver.add_clause([-v for v in solution])

    new_enc = solution[:]  # defining a list containing the solution encodings
    random.shuffle(new_enc)        # shuffling the new_enc list to bring randomization

    imp = [] #defining a empty list for taking assumptions

    flat=list()     # we flatten the arr1 and arr2 holding the encoding of our variables

    for i in range(k*k):
        for j in range(k*k):
            for l in range(k*k):
                flat.append(arr1[i][j][l])
                flat.append(arr2[i][j][l])
    
    
    solver.set_phases(v  for v in flat)        # We use solver to assign phases to the random encoding from the flattened list

    while len(new_enc):        # We loop through the length of the new_enc encodings

        enc = new_enc.pop()     # on each iteration we pop an element from new_enc and put up in enc

        ex=list()

        for i in imp:
            ex.append(i)
        for i in new_enc:
            ex.append(i)

        if solver.solve(assumptions=ex):        # We assume the new_enc and imp list to be True clauses
            # If some other solution does exist then we just append the enc variable to imp list
            imp.append(enc)        
        else:
            # If we found no other solution, we drop the new variable
            core = solver.get_core()
            # Remove encodings not imp for deriving unsatisfiability
            
            sub=list()
            for x in new_enc:
                if x in core:
                    sub.append(x)
            new_enc=sub
            
    
    print("Error! No Sudoku" if solver.solve(assumptions=imp) else "") 
    # Just in case false or No sudoku as a case

    for x in (0,k*k):
        for y in (0,k*k):
            for i in imp:
                str1=str(i)
                s=int(str1[0])
                if s==1 :
                    r=int(str1[1:val+1])
                    c=int(str1[val+1:val+val+1])
                    n=int(str1[2*(val)+1:])
                    if r==x and y==c: sudoku[c-1][r-1]=n
                    else: sudoku[c-1][r-1]=0
                
                else:
                    r=int(str1[1:val+1])
                    c=int(str1[val+1:val+val+1])
                    n=int(str1[2*(val)+1:])
                    if r==x and y==c: sudoku[c-1][k*k+r-1]=n
                    else: sudoku[c-1][k*k+r-1]=0

    sudoku.to_csv(
        ".\Solutions\Solution_{index}.csv".format(index=k), index=False, header=False
    )  # Saving the solved sudoku in a csv file

    # SUDOKU 1
    print("SUDOKU 1")
    r = 0
    for i in range(0, k * k + k + 1):
        c = 0
        for j in range(0, k * k + k + 1):
            if [x for x in range(0, k * k + k + 1, k + 1) if i == x]:
                print("-", end=" ")
            elif [x for x in range(0, k * k + k + 1, k + 1) if j == x]:
                print("|", end=" ")
            else:
                print(sudoku[c][r], end=" ")
                c += 1
        if [x for x in range(0, k * k + k + 1, k + 1) if i == x]:
            pass
        else:
            r += 1
        print()

    # SUDOKU 2
    print("SUDOKU 2")
    r = 0
    for i in range(0, k * k + k + 1):
        c = 0
        for j in range(0, k * k + k + 1):
            if [x for x in range(0, k * k + k + 1, k + 1) if i == x]:
                print("-", end=" ")
            elif [x for x in range(0, k * k + k + 1, k + 1) if j == x]:
                print("|", end=" ")
            else:
                print(sudoku[c][k * k + r], end=" ")
                c += 1
        if [x for x in range(0, k * k + k + 1, k + 1) if i == x]:
            pass
        else:
            r += 1
        print()
