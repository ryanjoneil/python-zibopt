# 0.7.2 dev #
  * Added backwards compatibility for Python 2 (thanks to [Guillaume Sagnol](http://www.zib.de/sagnol/) for the patch!).
  * Added magic square example
  * [Issue 33](https://code.google.com/p/python-zibopt/issues/detail?id=33): Fixed issue with single-variable objectives subject to constraints:
```
solver += x >= y
solution = solver.minimize(objective=x)
```
  * [Issue 34](https://code.google.com/p/python-zibopt/issues/detail?id=34): Constant objectives no longer raise errors
  * [Issue 32](https://code.google.com/p/python-zibopt/issues/detail?id=32): Fixed obscure constraint issue
```
solver += x <= (y-1) + 100*(1-z)
```

# 0.7.1 dev #
  * [Issue 25](https://code.google.com/p/python-zibopt/issues/detail?id=25): Offsets work in objective functions:
```
solution = solver.maximize(objective=x+3)
```
  * Switched to using [python-algebraic](https://github.com/rzoz/python-algebraic) for symbolic modeling logic
  * Builds against ZIBopt 2.1.1
  * [Issue 31](https://code.google.com/p/python-zibopt/issues/detail?id=31): Fixed issue with rsub so 1-(x+y) == -(x+y)+1

# 0.7 dev #
  * [Issue 20](https://code.google.com/p/python-zibopt/issues/detail?id=20): Build instructions and setup.py now link against Ipopt
  * [Issue 28](https://code.google.com/p/python-zibopt/issues/detail?id=28): Module docs are now being generated using reStructuredText and Sphinx.  They live on [PyPI](http://packages.python.org/python-zibopt/).
  * [Issue 24](https://code.google.com/p/python-zibopt/issues/detail?id=24): Providing both upper and lower bounds on a variable now works properly: 2 <= x <= 4.
  * [Issue 23](https://code.google.com/p/python-zibopt/issues/detail?id=23): Nonlinear objectives now use >= and <= to create new variables instead of ==.  This may give a performance benefit.
  * [Issue 22](https://code.google.com/p/python-zibopt/issues/detail?id=22): Dividing by variables raises a TypeError.

# 0.6 dev #
  * [Issue 19](https://code.google.com/p/python-zibopt/issues/detail?id=19): Added bilinear constraints from SCIP 2.0.1.  This requires restructuring of constraints and expressions, so code that used internal features of these will need to be changed.  The following sorts of programs are now possible:
```
from zibopt import scip
solver = scip.solver()
x1 = solver.variable(upper=10)
x2 = solver.variable(upper=10)
solver += (x1 + x2) * (3*x1 - x2) <= 10
solver += 3*x1 <= 4*x2
solution = solver.maximize(objective=x1**2 + x1*x2/4)
# 21.76
```
```
from zibopt import scip
solver = scip.solver()  
x1 = solver.variable(scip.BINARY)
x2 = solver.variable(scip.BINARY)
solver += x1 * x2 == 0
solution = solver.maximize(objective=3*x1 + 4*x2)
print(solution.objective, solution[x1], solution[x2])
# 4.0 0.0 1.0.
```
> Further, expression handling has been vastly improved and can handle these sorts of constructions now:
```
solver += (x + y) * (3*x - y) <= 10
solver += (3*x)**2 >= 3
```
  * [Issue 21](https://code.google.com/p/python-zibopt/issues/detail?id=21): Allow better expression of constraints in solver.constraint(...)
```
c = solver.constraint(x1 + 2*x2 <= 4)
```
  * [Issue 13](https://code.google.com/p/python-zibopt/issues/detail?id=13): Added the ability to remove and reinstall constraints into the solver
```
from zibopt import scip

solver = scip.solver()

x1 = solver.variable(scip.INTEGER)
x2 = solver.variable(scip.INTEGER)

c1 = solver.constraint(2*x1 + 2*x2 <= 4)
c2 = solver.constraint(2*x1 + 2*x2 <= 3)

print(solver.maximize(objective=x1+x2).objective) # 1.0

solver -= c2
print(solver.maximize(objective=x1+x2).objective) # 2.0

solver += c2
print(solver.maximize(objective=x1+x2).objective) # 1.0
```
  * [Issue 9](https://code.google.com/p/python-zibopt/issues/detail?id=9): Ported to Python 3.2 and resolved all build warnings
  * [Issue 16](https://code.google.com/p/python-zibopt/issues/detail?id=16): Added ability to stop the solver after a number of solutions are found
```
solver.maximize(nsol=30)
```
  * [Issue 14](https://code.google.com/p/python-zibopt/issues/detail?id=14): Added ability to set display settings on the solver
```
solver.display['cuts'].width = 10
```

# 0.5 beta #
  * Entered beta testing
  * Removed dependency on ZIMPL libraries; improved installation docs

# 0.4 dev #
  * [Issue 8](https://code.google.com/p/python-zibopt/issues/detail?id=8): Added an algebraic interface for constraints and objective functions
```
solver += 4 <= 3*x1 + 4*x2 + 2*x3 <= 10
solver.maximize(objective=x1 + 2*x2 + x3)

solver += sum(x[i] for i in rows) == 1
solver.minimize(objective=sum(cost[i] * x[i] for i in rows))
```
  * [Issue 12](https://code.google.com/p/python-zibopt/issues/detail?id=12): Added access to branching priority for variables
```
x = solver.variable(scip.INTEGER)
x.priority = 1000

x = solver.variable(scip.INTEGER, priority=10)
```

# 0.3 dev #
  * [Issue 3](https://code.google.com/p/python-zibopt/issues/detail?id=3) and [Issue 4](https://code.google.com/p/python-zibopt/issues/detail?id=4): Added access for more solver settings
```
solver.branching['inference'].priority = 10000
solver.branching['inference'].maxdepth = -1
solver.branching['inference'].maxbounddist = -1

solver.conflict['logicor'].priority = 10000

solver.heuristics['octane'].priority = 500
solver.heuristics['octane'].maxdepth = -1
solver.heuristics['octane'].frequency = 10
solver.heuristics['octane'].freqofs = 5

solver.presolvers['dualfix'].priority = 10000

solver.propagators['pseudoobj'].priority = 1000s.branching.keys
solver.propagators['pseudoobj'].frequency = 10

solver.selectors['bfs'].stdpriority = 1000
solver.selectors['bfs'].memsavepriority = 10

solver.separators['clique'].priority = 10000
solver.separators['clique'].maxbounddist = -1
solver.separators['clique'].frequency = 10000
```

# 0.2 dev #
  * [Issue 1](https://code.google.com/p/python-zibopt/issues/detail?id=1): Added gap and absgap keywords to maximize/minimize to stop when gap is within a certain limit
```
solver.maximize(absgap=0.5, gap=100) 
```
  * [Issue 1](https://code.google.com/p/python-zibopt/issues/detail?id=1): Added time keyword to maximize/minimize to return best solution after a number of seconds
```
solver.maximize(time=500) 
```
  * Removed solution.feasible, added solution.infeasible, unbounded, inforunbd, and optimal
  * Tested against SCIP 1.2
  * [Issue 2](https://code.google.com/p/python-zibopt/issues/detail?id=2): Added ability to change priority, maxdepth, and maxbounddist on branching rules:
```
solver.branching['inference'].priority = 10000
solver.branching['mostinf'].maxdepth += 2
print(solver.branching['pscost'].maxbounddist)
```
  * Added ability to set priorities on conflict handlers and separators:
```
solver.separators['clique'].priority = 10000
solver.conflict['logicor'].priority = 10000
```

# 0.1 dev #
  * Initial libraries for interfacing to solver, variables, constraints, and solutions
  * Ability to turn off solver verbosity
  * Solutions are false in case of infeasibilty or unboundedness
  * SCIP errors get mapped to Python exception types
  * The solver can be restarted with additional constraints and variables
  * Primal solutions can be fed to minimize/maximize and are checked for feasibility