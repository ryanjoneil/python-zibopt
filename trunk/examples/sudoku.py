#!/usr/bin/env python

from itertools import product
from zibopt import scip

# 0 indicates a cell value is not given
problem = [
    [0, 0, 0,   6, 9, 2,   0, 4, 0],
    [7, 0, 0,   0, 0, 0,   8, 9, 0],
    [0, 0, 0,   0, 0, 0,   0, 0, 6],

    [0, 0, 9,   0, 1, 7,   0, 0, 3],
    [0, 0, 7,   0, 8, 0,   5, 0, 0],
    [8, 0, 0,   4, 6, 0,   1, 0, 0],

    [5, 0, 0,   0, 0, 0,   0, 0, 0],
    [0, 8, 6,   0, 0, 0,   0, 0, 1],
    [0, 3, 0,   7, 2, 8,   0, 0, 0]
]

if __name__ == '__main__':
    # Indexes for creating variables and constraints
    rows = range(len(problem))
    cols = rows
    vals = range(1, 10)
    groups = (0, 3, 6)

    # 9x9x9 structure for storing all binary variables
    # If x[i][j][k] == 1, then problem[i][j] == k.
    x = dict((i, dict((j, {}) for j in cols)) for i in rows)

    # Initialize one binary variable per cell value
    solver = scip.solver()
    for i, j, k in product(rows, cols, vals):
        x[i][j][k] = solver.variable(
            vartype = scip.BINARY,
            lower   = 1 if problem[i][j] == k else 0
        )
     
    # Each cell takes on exactly one value
    for i, j in product(rows, cols):
        solver.constraint( 
            lower = 1,
            upper = 1,
            coefficients = dict((x[i][j][k], 1) for k in vals)
        )

    # Each value occurs in each row once
    for i, k in product(rows, vals):
        solver.constraint(
            lower = 1,
            upper = 1,
            coefficients = dict((x[i][j][k], 1) for j in cols)
        )

    # Each value occurs in each column once
    for j, k in product(cols, vals):
        solver.constraint( 
            lower = 1,
            upper = 1,
            coefficients = dict((x[i][j][k], 1) for i in rows)
        )

    # Each 3x3 group has all unique values    
    for m, n, k in product(groups, groups, vals):
        solver.constraint(
            lower = 1,
            upper = 1,
            coefficients = dict(
                (x[i][j][k], 1) for i, j in product(range(m,m+3), range(n,n+3))
            )
        )    

    # All variables have 0 coefficients, so we can either max or min            
    solution = solver.maximize()
    if solution:
        # Convert solution values to a nice solution matrix
        for i, j in product(rows, cols):
            for k in vals:
                if solution.value(x[i][j][k]):
                    problem[i][j] = k
                    break
                
        for row in problem:
            print row

    else:
        print 'no solution'

