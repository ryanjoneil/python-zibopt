#!/usr/bin/env python

from itertools import product
from zibopt import scip

# Generic formulation for the Capacitated Facility Location Problem
# This example was converted from the ZIMPL examples directory.

FACILITIES = 'A', 'B', 'C', 'D'
CUSTOMERS  = range(1, 10)

# Costs for opening a facility
FIXED_COST = dict(A=500, B=600, C=700, D=800)

# Capacity of a facility at each site
CAPACITY = dict(A=40, B=55, C=73, D=90)

# Demand from each customer
DEMAND = {1:10, 2:14, 3:17, 4:8, 5:9, 6:12, 7:11, 8:15, 9:16}

# Transportation cost from each facility to each customer
TRANSPORTATION = dict(
  A = {1:55, 2: 4, 3:17, 4:33, 5:47, 6:98, 7:19, 8:10, 9: 6},
  B = {1:42, 2:12, 3: 4, 4:23, 5:16, 6:78, 7:47, 8: 9, 9:82}, 
  C = {1:17, 2:34, 3:65, 4:25, 5: 7, 6:67, 7:45, 8:13, 9:54},
  D = {1:60, 2: 8, 3:79, 4:24, 5:28, 6:19, 7:62, 8:18, 9:45}
)

if __name__ == '__main__':
    solver = scip.solver()

    # Fixed cost variables for opening facilities
    y = {}
    for f in FACILITIES:
        y[f] = solver.variable(
            coefficient = FIXED_COST[f],
            vartype     = scip.BINARY
        )
        
    # Variables to represent facility/customer relations
    x = dict((f, {}) for f in FACILITIES)
    for f, c in product(FACILITIES, CUSTOMERS):
        # A facility completely satisfies its customers' demands
        x[f][c] = solver.variable(
            coefficient = TRANSPORTATION[f][c], 
            vartype     = scip.BINARY
        )

    # Supply each customer from one facility
    for c in CUSTOMERS:
        solver.constraint(
            lower = 1,
            upper = 1,
            coefficients = dict((x[f][c], 1) for f in FACILITIES)
        )

    # Using a facility incurs its fixed cost
    for f, c in product(FACILITIES, CUSTOMERS):
        # x[f][c] <= y[f]    <=>    x[f][c] - y[f] <= 0
        solver.constraint(upper=0, coefficients={x[f][c]:1, y[f]:-1})

    # Facilities cannot exceed their capacities
    for f in FACILITIES:
        solver.constraint(
            upper = CAPACITY[f],
            coefficients = dict((x[f][c], DEMAND[c]) for c in CUSTOMERS)
        )

    # All variables have 0 coefficients, so we can either max or min            
    solution = solver.minimize()
    if solution:
        print 'TOTAL COST:', solution.objective
        for f in FACILITIES:
            if solution.value(y[f]) > 0.5:
                print 'FACTILITY', f, 'CUSTOMERS:',
                for c in CUSTOMERS:
                    if solution.value(x[f][c]) > 0.5:
                        print c,
                print
    else:
        print 'infeasible'

