#!/usr/bin/env python3

# This script solves the Magic Square problem using SCIP.
# http://en.wikipedia.org/wiki/Magic_square

from itertools import chain
from zibopt import scip
import sys

if __name__ == '__main__':
    solver = scip.solver(quiet=False)

    try:
        # Matrix size is required and should be >= 2
        size = int(sys.argv[1])
        assert size > 1

        # Big-M is optional.  If provided it must be a positive integer.
        # If not, we allow the optimizer to choose an M for us.
        try:
            M = int(sys.argv[2])
        except IndexError:
            M = solver.variable()
        else:
            assert M > 1

    except:
        print('usage: %s matrix-size [big-M]' % sys.argv[0])
        sys.exit()

    # Construct a matrix of decision variables
    matrix = []
    for i in range(size):
        matrix.append([
            solver.variable(scip.INTEGER, lower=1) 
            for j in range(size)
        ])

    # For convenience, mash all variables into a single list
    all_vars = list(chain(*matrix))
        
    # The rows and columns must all sum to the same value
    sum_val = solver.variable()
    for i in range(size):
        # Row i sum
        solver += sum(matrix[i]) == sum_val
        
        # Column i sum
        solver += sum(matrix[j][i] for j in range(size)) == sum_val
    
    # Diagonal sum must be the same too
    solver += sum(matrix[i][i] for i in range(size)) == sum_val
    
    # No two variables can have the same value.  In pure integer
    # programming, this would require big-M, but we don't know how
    # big the M should be.  We can get around this using another variable
    # which has the maximum value and bilinear constraints.
    for i, x in enumerate(all_vars):
        #if not isinstance(M, int):
        #    solver += M >= x

        for y in all_vars[i+1:]:
            z = solver.variable(scip.BINARY)
#            solver += x >= (y+1) - (100*z)
#            solver += x <= (y-1) + 100*(1-z)
            solver += x  >= y + 1 - M*z
            solver += x - M*(1-z) <= y - 1

    solution = solver.minimize()#objective=max_val) # combine with isinstance check
    if solution:
        print('sum = %d' % solution[sum_val])
        print('magic square:')
        for row in matrix:
            for x in row:
                print('% 6d' % solution[x], end=' ')
            print()
    else:
        print('invalid')
    
    
