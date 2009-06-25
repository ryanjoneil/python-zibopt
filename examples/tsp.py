#!/usr/bin/env python

from itertools import product
from zibopt import scip
import json, sys

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
    # We represent STSP as a lower triangular matrix with the diagonal.
    # Thus the first column and row represent connections to the first node.
    try:
        distance = json.load(open(sys.argv[1]))
    except IndexError:
        print 'usage: %s data.json' % sys.argv[0]
        sys.exit()

    solver = scip.solver()
    
    arcs = []
    for d in distance:
        arcs.append([solver.variable(c, scip.BINARY) for c in d])
    
    # Assignment Problem Relaxation: each node connects to two other nodes
    l = len(distance)
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
    n = 0
    while True:
        solution = solver.minimize()

        if solution:
            subtours = walk_subtours(arcs, solution)
            print '-' * 80
            print '[%d] LENGTH:' % n, solution.objective, '/ SUBTOURS:', len(subtours)
            for s in subtours:
                print '   ', [x+1 for x in s]
 
            n += 1
            if len(subtours) > 1:
                solver.restart()
                
                # Generate subtour elimination constraints.  These function by
                # adding a knapsack constraint setting the sum of the arcs
                # in each subtour to their cardinality minus one.
                for subtour in subtours:
                    coefficients = {}
                    # n points in a tour have n arcs, not n-1.  That means we
                    # have to include the arc that takes us to the start node.
                    for pair in zip(subtour, subtour[1:]+[subtour[0]]):
                        # Column # is the higher of the two
                        i, j = max(*pair), min(*pair)
                        coefficients[arcs[i][j]] = 1
                    
                    solver.constraint(
                        upper = len(coefficients) - 1,
                        coefficients = coefficients
                    )

            else:
                # Optimal tour found.  Stop.
                break

        else:
            print 'infeasible'
            break

