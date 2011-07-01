'''
zibopt.scip
===========
This module provides a Python interface to the SCIP mixed integer 
programming solver of the ZIB optimization suite.  It defines two classes
for use by the modeler:

    - *scip.solver*:    interface to SCIP
    - *scip.solution*:  IP solutions returned by solver.minimize/maximize

There are type constants defined for declaring variables:

    - *BINARY*:      variable can be either 0 or 1
    - *INTEGER*:     variable can take only integer values
    - *IMPLINT*:     variable takes only integer values implicitly
    - *CONTINUOUS*:  variable can take fractional values
    
Basic usage of python-zibopt involves constructing a solver, adding variables
and constraints to it, then calling minimize or maximize.  SCIP varialbles
are wrapped in Python variables and can be referenced as such.  Note that
the value of a given variable for a given solution to an IP is not set in the
Python variable itself, but in the solution values.  This is because each
variable may be able to take on multiple values for an IP.

A simple IP model in ZIMPL might like look::

    var x1 integer >= 0 <= 2;
    var x2 integer >= 0;
    var x3 integer >= 0;
    
    maximize z: x1 + x2 + 2*x3;
    subto c: x1 + x2 + 3*x3 <= 3;
 
Translated to python-zibopt this becomes::
    
    from zibopt import scip
    solver = scip.solver()

    # All variables have default lower bounds of 0
    x1 = solver.variable(scip.INTEGER)
    x2 = solver.variable(scip.INTEGER)
    x3 = solver.variable(scip.INTEGER)

    # x1 has an upper bound of 2
    solver += x1 <= 2

    # Add a constraint such that:  x1 + x2 + 3*x3 <= 3
    solver += x1 + x2 + 3*x3 <= 3

    # The objective function is: z = x1 + x2 + 2*x3
    solution = solver.maximize(objective=x1 + x2 + 2*x3)

    # Print the optimal solution if it is feasible.
    if solution:
        print('z  =', solution.objective)
        print('x1 =', solution[x1])
        print('x3 =', solution[x2])
        print('x2 =', solution[x3])
    else:
        print('invalid problem')
'''

# This provide more convenient namespacing
from ._constraint import *
from ._expression import *
from ._settings import *
from ._solution import *
from ._solver import *
from ._variable import *

__all__ = 'solver',

