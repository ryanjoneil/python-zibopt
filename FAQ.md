# Frequently Asked Questions #

#### Q: Where are the module docs? ####
A: On [packages.python.org](http://packages.python.org/python-zibopt/).

#### Q: How do I create bilinear constraints? ####
A: Simply multiply variables by each other.  You may also use powers of two.  Examples of valid constraints include:
```
solver += 2*x**2 + (3*y)**2 <= z**2 + 4
solver += (x + y) * (x - y) >= 0
solver += (x/4)**2 == 3
solver += 2 <= x <= 4
```

#### Q: How do I remove a constraint once I've added it? ####
A: Use solver.constraint(...) to capture the constraint.  You may now remove it and add it again later:
```
constraint = solver.constraint(2 <= x <= 4)
solver -= constraint # remove from formulation
solver += constraint # add back to formulation
```

#### Q: How do I change priorities of branching rules and set other settings? ####

A: On instantiation, a SCIP solver is preloaded with dictionaries containing available branching rules, conflict handlers, heuristics, presolvers, heuristics, presolvers, domain propagators, and node selectors.  You can set properties such as priority and frequency on these directly.  See the module docs for complete examples:
```
solver.branching['fullstrong'].priority = 10
```

#### Q: What's IMPLINT? ####

A: This type is for variables that are supposed to take on integer values, but will do so implicitly since they only appear in constraints with other integer variables.  This can save SCIP some time.

#### Q: I can't represent my problem in its entirety and need to solve a combinatorial relaxation before adding more constraints.  How can I do this? ####

A: SCIP keeps the original problem untouched and works against a transformed copy of problem.  Once you've solved by calling solver.minimize() or solver.maximize(), you can make changes to the original problem by first calling solver.restart().
```
# ... instantiate a problem ...
solver.maximize()
new_variable   = solver.variable(coefficient=1)
new_constraint = solver.constraint(new_variable <= 2)
solver.maximize()
```

#### Q: I know a good solution already.  How do I tell the solver about it? ####

A: solver.minimize() and solver.maximize() both take in an optional solution dictionary mapping variable instances to their primal values.  If this is done, the solution is checked for feasibility and a SolverError is raised in case of infeasibility.

#### Q: How do I see what SCIP is doing? ####

A: solver.minimize() and solver.maximize() also take an optional quiet argument, which defaults to true.  If you pass quiet=False to the solver constructor, then you'll see the normal SCIP chatter:
```
solver = scip.solver(quiet=False)
```

#### Q: There seem to be multiple ways to add constraints and objectives.  What should I use? ####

A: python-zibopt creates constraints as collections of terms with coefficients.  Behind the scenes, this gets a little complex to allow for bilinear constraints.  You should always use the algebraic method:
```
from zibopt import scip
solver = scip.solver()

x1 = solver.variable(scip.INTEGER)
x2 = solver.variable(scip.INTEGER)
x3 = solver.variable(scip.INTEGER)

solver += x1 <= 2
solver += x1 + x2 + 3*x3**2 <= 3

solution = solver.maximize(objective=x1*x2 + x2 + 2*x3)
```

The syntax plays nicely with the Python builtin sum(...), examples of which can be found in the source.

#### Q: How can I set branching priority on a variable? ####

A: Variables expose a priority attribute.  You can access that directly or pass in the priority to solver.variable(...):
```
x = solver.variable(scip.INTEGER)
x.priority = 1000

x = solver.variable(scip.INTEGER, priority=10)
```
This uses SCIP's SCIPvarChgBranchPriority function for setting the branching priority.  Depending on the state of the solver, what may actually get set is the priority on a transformed or aggregate variable, meaning that the value of x.priority may not look how you expect.