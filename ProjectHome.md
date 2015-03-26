# About python-zibopt #
This is a library for generating and solving Mixed Integer Programs in [Python](http://python.org) 2.7 or 3.2 using [SCIP](http://scip.zib.de/) and [SoPlex](http://soplex.zib.de/) from the [ZIB Optimization Suite](http://zibopt.zib.de/).  It aims to provide a seamless integration between the two environments, allowing the programmer to easily solve MIQPs using Python's convenient facilities for data access and manipulation, among other things.

Documentation for the latest version lives [here](http://packages.python.org/python-zibopt/).

# Licensing #
python-zibopt is released under the GPL.  Components of the ZIB Optimization Suite, which it links against, are distributed by ZIB under the ZIB Academic License.  Commercial licenses for SCIP are available.  Please see [the ZIB Optimization Suite website](http://zibopt.zib.de/) for more information.

# Example #
python-zibopt does provide [example scripts](http://code.google.com/p/python-zibopt/source/browse/#svn/trunk/examples) for solving IPs, but for the less patient here is a brief example, in Python 3.2's syntax:
```
from zibopt import scip
solver = scip.solver()

# All variables have default lower bounds of 0
x1 = solver.variable(scip.INTEGER)
x2 = solver.variable(scip.INTEGER)
x3 = solver.variable(scip.INTEGER)

# x1 has an upper bound of 2
solver += x1 <= 2

# Add a constraint such that:  x1 + x2 + 3*x3**2 <= 3
solver += x1 + x2 + 3*x3**2 <= 3

# The objective function is: z = x1*x2 + x2 + 2*x3
solution = solver.maximize(objective=x1*x2 + x2 + 2*x3)

# Print the optimal solution if it is feasible.
if solution:
    print('z  =', solution.objective)
    print('x1 =', solution[x1])
    print('x2 =', solution[x2])
    print('x3 =', solution[x3])
else:
    print('invalid problem')
```