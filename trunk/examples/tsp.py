#!/usr/bin/env python

from itertools import product
from zibopt import scip

# We represent STSP as a lower triangular matrix with the diagonal.
# Thus the first column and row represent connections to the first node.
DISTANCE = [
    [0], 
    [1, 0],
    [5, 2, 0],
    [3, 9, 2, 0],
    [2, 8, 1, 3, 0],
    [8, 5, 2, 1, 8, 0],
    [4, 4, 2, 3, 7, 4, 0],
    [5, 6, 3, 4, 6, 6, 2, 0],
    [2, 3, 6, 4, 2, 8, 1, 3, 0]
]

def walk_subtours(arcs, solution):
    l = len(arcs)
    
    # Unpack arcs into a connections dictionary
    connects = dict((i,set()) for i in range(l))
    for i in range(l):
        # Horizonal row up to node i
        for j in range(i):
            if solution.value(arcs[i][j]) > 0.5:
                connects[i].add(j)
                connects[j].add(i)
            
        # Vertical column below node i
        for j in range(i+1,l):
            if solution.value(arcs[j][i]) > 0.5:
                connects[i].add(j)
                connects[j].add(i)
        
    # Identify subtours
    subtours = []
    unseen   = set(connects.keys())

    # Pick an arbitrary node to start at
    current = list(unseen)[0]
    unseen.remove(current)

    tour = [current]
    while unseen:
        try:
            # Continue down an arbitrary path
            current = [n for n in connects[current] if n in unseen][0]
            unseen.remove(current)
            tour.append(current)

        except IndexError:                
            # This subtour is done
            if unseen:
                current = list(unseen)[0]
                unseen.remove(current)
            
            subtours.append(tour)
            tour = [current]
    
    if tour:
        subtours.append(tour)

    return subtours

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
                [arcs[j][i] for j in range(i+1,l)]
            )
        )
    
    # Our formulation thus far only represents a combinatorial relaxation of
    # STSP as an assignment problem.  It is possible the solver will return
    # disconnected subtours.  
    while True:
        solution = solver.minimize()

        if solution:
            subtours = walk_subtours(arcs, solution)
            print 'length:', solution.objective, '/', 
            print 'subtours:', len(subtours), '/', subtours

            if len(subtours) > 1:
                solver.restart()
                
                # Generate subtour elimination constraints.  These function by
                # adding a 
                for subtour in subtours:
                    coefficients = {}
                    for pair in zip(subtour, subtour[1:]):
                        # Column # is the higher of the two
                        i, j = max(*pair), min(*pair)
                        coefficients[arcs[i][j]] = 1
                    
                    solver.constraint(
                        upper = len(coefficients) - 1,
                        coefficients = coefficients
                    )

            else:
                print 'optimal tour:', subtours[0]
                for i, row in enumerate(arcs):
                    print i , '::',
                    print ' '.join('X' if solution.value(x) else '-' for x in row)
                print '----' + '--' * l
                print '  ::', ' '.join(str(x) for x in range(l))

                break
        
        else:
            print 'infeasible'
            break

