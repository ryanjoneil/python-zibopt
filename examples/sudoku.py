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

    # Initialize one binary variable per cell value
    solver = scip.solver()
    for i, j, k in product(rows, cols, vals):
        solver.variable('%d %d %d' % (i, j, k),
            vartype = scip.BINARY,
            lower   = 1 if problem[i][j] == k else 0
        )
     
    # Each cell takes on exactly one value
    for i, j in product(rows, cols):
        solver.constraint('value %d %d' % (i, j), 
            lower = 1,
            upper = 1,
            coefficients = dict(('%d %d %d' % (i, j, k), 1) for k in vals)
        )

    # Each value occurs in each row once
    for i, k in product(rows, vals):
        solver.constraint('row %d %d' % (i, k), 
            lower = 1,
            upper = 1,
            coefficients = dict(('%d %d %d' % (i, j, k), 1) for j in cols)
        )

    # Each value occurs in each column once
    for j, k in product(cols, vals):
        solver.constraint('column %d %d' % (j, k), 
            lower = 1,
            upper = 1,
            coefficients = dict(('%d %d %d' % (i, j, k), 1) for i in rows)
        )

    # Each 3x3 group has all unique values    
    for m, n, k in product(groups, groups, vals):
        solver.constraint('group %d %d %d' % (m, n, k),
            lower = 1,
            upper = 1,
            coefficients = dict(
                ('%d %d %d' % (i, j, k), 1) for i, j in product(
                    range(m, m+3), range(n, n+3)
                )
            )
        )    
    
    # All variables have 0 coefficients, so we can either max or min            
    solution = solver.maximize()
    for x in solution.values():
        i, j, k = x.name.split()
        problem[int(i)][int(j)] = int(k)
        
    for row in problem:
        print row

