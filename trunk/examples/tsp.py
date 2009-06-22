#!/usr/bin/env python

from itertools import product
from zibopt import scip

DISTANCE = [
    [1],
    [5, 2],
    [1, 1, 2],
    [2, 8, 1, 3],
    [8, 5, 2, 1, 2],
    [4, 4, 2, 3, 7, 4],
    [5, 6, 3, 4, 2, 6, 2]
]

if __name__ == '__main__':
    solver = scip.solver()
    
    arcs = []
    for d in DISTANCE:
        arcs.append([solver.variable(c, scip.BINARY) for c in d])
    
    # Assignment Problem Relaxation: each node connects to two other nodes
    l = len(DISTANCE)
    for i in range(l):
        solver.constraint(
            lower = 2,
            upper = 2,
            coefficients = dict((x,1) for x in 
                [arcs[i][j] for j in range(i)] + 
                [arcs[j][i] for j in range(i,l)]
            )
        )

    solution = solver.minimize()
    
    if solution:
        print 'TOUR LENGTH:', solution.objective
        
        # Identify subtours
        subtours = []
        unseen   = set(range(l))
        tour     = []

        # Pick an arbitrary node to start at
        current = list(unseen)[0]
        unseen.remove(current)

        while unseen:
            # Find all nodes our current nodes is connected to that we
            # haven't already visited
            connects = [
                (j, arcs[current][j]) for j in range(current) 
                if j in unseen and solution.value(arcs[current][j]) > 0.5
            ] + [
                (j, arcs[j][current]) for j in range(current,l) 
                if j in unseen and solution.value(arcs[j][current]) > 0.5
            ]
    
            print connects
    
            if connects:
                # Continue down an arbitrary path
                current, v = connects[0]
                tour.append(current)
                print current
                
            else:
                # This subtour is done
                if unseen:
                    current = list(unseen)[0]
                    unseen.remove(current)
                
                subtours.append(tour)
                print tour
                tour = []
            # TODO: finish me
                        
                    
    else:
        print 'infeasible'

