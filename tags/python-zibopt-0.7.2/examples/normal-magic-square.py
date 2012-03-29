#!/usr/bin/env python3

# This script solves the Normal Magic Square problem using SCIP.
# http://en.wikipedia.org/wiki/Magic_square
#
# This is a constraint satisfaction problem.  For a square matrix of size
# n, we seek n*n integers such that the following constraints are satisfied:
#
# 1. All variables are integers >= 1, <= n^2
# 2. All rows, all columns, and the diagonal sum to the same value
# 3. All variables are different
#
# The single argument to the script is specifies the size of the matrix.

from itertools import chain, product
from zibopt import scip
import sys

if __name__ == '__main__':
    solver = scip.solver()# quiet=False)

    try:
        # Matrix size is required and should be >= 2
        size = int(sys.argv[1])
        assert size > 1

    except:
        print('usage: %s matrix-size' % sys.argv[0])
        sys.exit()

    # Construct a matrix of decision variables.  Each cell in the square
    # has n^2 binary variables, exactly one of which must be on.
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append([
                solver.variable(scip.BINARY)
                for _ in range(size**2)
            ])
        matrix.append(row)
    
    # Add constraints such that each square cell has exactly one
    # binary variable turned on.
    for row in matrix:
        for cell in row:
            solver += sum(cell) == 1

    # Each value occurs exactly once
    for i in range(size**2):
        solver += sum(
            matrix[r][c][i] for r, c in product(range(size), range(size))
        ) == 1
    
    # Construct an expression for each cell that is the sum of 
    # its binary variables with their associated coefficients.
    sums = []
    for row in matrix:
        sums_row = []
        for cell in row:
            sums_row.append(sum((i+1)*x for i, x in enumerate(cell)))
        sums.append(sums_row)
    
    # The rows and columns must all sum to the same value
    sum_val = solver.variable()
    for row in sums:
        solver += sum(row) == sum_val
    for c in range(size):
        solver += sum(sums[r][c] for r in range(size)) == sum_val    
    solver += sum(sums[i][i] for i in range(size)) == sum_val

    solution = solver.minimize()
    if solution:
        print('sum = %d' % solution[sum_val])
        print('normal magic square:')
        for row in matrix:
            for cell in row:
                for i, x in enumerate(cell):
                    if solution[x] > 0.5:
                        print('% 6d' % (i+1), end=' ')
                        break
            print()
    else:
        print('invalid')
    
