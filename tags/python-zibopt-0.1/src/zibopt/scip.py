'''
This module provides a Python interface to the SCIP mixed integer programming
solver of the ZIB optimization suite.  It defines two classes:

    scip.solver:    interface to SCIP
    scip.solution:  IP solutions returned by solver.minimize/maximize

There are type constants defined for declaring variables:

    BINARY:      variable can be either 0 or 1
    INTEGER:     variable can take only integer values
    IMPLINT:     variable takes only integer values implicitly
    CONTINUOUS:  variable can take fractional values
    
Basic usage of python-zibopt involves constructing a solver, adding variables
and constraints to it, then calling minimize or maximize.  SCIP varialbles
are wrapped in Python variables and can be referenced as such.  Note that
the value of a given variable for a given solution to an IP is not set in the
Python variable itself, but in the solution values.  This is because each
variable may be able to take on multiple values for an IP.

A simple IP model in ZIMPL might like look:

    var x1 integer >= 0 <= 2;
    var x2 integer >= 0;
    var x3 integer >= 0;
    
    maximize z: x1 + x2 + 2*x3;
    subto c: x1 + x2 + 3*x3 <= 3;
 
Translated to python-zibopt this becomes:
    
    from zibopt import scip
    solver = scip.solver()

    # Three integer variables with objective coefficients: z = x1 + x2 + 2*x3
    # All variables have default lower bounds of 0.  x1 <= 2.
    x1 = solver.variable(coefficient=1, vartype=scip.INTEGER, upper=2)
    x2 = solver.variable(coefficient=1, vartype=scip.INTEGER)
    x3 = solver.variable(coefficient=2, vartype=scip.INTEGER)

    # Add a constraint such that:  x1 + x2 + 3*x3 <= 3
    solver.constraint(upper=3, coefficients={x1:1, x2:1, x3:3})

    # Solve the IP and print the optimal solution if it is feasible.
    solution = solver.maximize()
    if solution:
        print 'z  =', solution.objective
        print 'x1 =', solution[x1]
        print 'x3 =', solution[x2]
        print 'x2 =', solution[x3]
    else:
        print 'infeasible'
'''

from zibopt import _scip, _vars, _cons, _soln

__all__ = 'solver',

BINARY     = _scip.BINARY
INTEGER    = _scip.INTEGER
IMPLINT    = _scip.IMPLINT
CONTINUOUS = _scip.CONTINUOUS

ConstraintError = _cons.error
SolutionError   = _soln.error
SolverError     = _scip.error
VariableError   = _vars.error

class solution(_soln.solution):
    '''
    A solution to a mixed integer program from SCIP.  Solution values can
    be obtained using variable references from the solver:
    
        x1_value = solution[x1]
    
    If a solution is infeasible or unbounded, it will be false when evaluated
    in boolean context:
    
        if solution:
            # do something interesting
    
    '''
    def __init__(self, solver):
        super(solution, self).__init__(solver)
        self.solver = solver

    def __nonzero__(self):
        return bool(self.feasible)
    
    def __getitem__(self, key):
        return self.value(key)
    
    def values(self):
        vals = {}
        for v in self.solver.variables:
            vals[v] = self.value(v)
        return vals

class solver(_scip.solver):
    '''A SCIP mixed integer programming solver'''
    def __init__(self, *args, **kwds):
        '''
        Instantiates a solver with default settings.
        @param quiet=True: turns the SCIP solver output off
        '''
        super(solver, self).__init__(*args, **kwds)
        self.variables = set()
        self.constraints = set()

    def variable(self, coefficient=0, vartype=CONTINUOUS, lower=0, **kwds):
        '''
        Adds a variable to the SCIP solver and returns it
        @param coefficient=0:      objective function coefficient
        @param vartype=CONTINUOUS: type of variable
        @param lower=0:            lower bound on variable
        @param upper=+inf:         upper bound on variable
        '''
        v = _vars.variable(self, coefficient, vartype, lower, **kwds)
        self.variables.add(v)
        return v

    def constraint(self, **kwds):
        '''
        Adds a constraint to the solver.  Returns None.
        @param lower=-inf:      lhs of constraint (lhs <= a'x)
        @param upper=+inf:      rhs of constraint (a'x <= rhs)
        @param coefficients={}: variable coefficients
        '''
        # Yank out variable coefficients since C code isn't expecting them
        try:
            coefficients = kwds['coefficients']
            del kwds['coefficients']
        except KeyError:
            coefficients = {} 

        cons = _cons.constraint(self, **kwds)
        for k, v in coefficients.iteritems():
            cons.variable(k, v)

        cons.register()
        self.constraints.add(cons)

    def maximize(self, *args, **kwds):
        '''
        Maximizes the objective function and returns a solution instance.
        @param solution={}: optional primal solution dictionary.  Raises a
                            SolverError if the solution is infeasible.
        '''
        super(solver, self).maximize(*args, **kwds)
        return solution(self)
        
    def minimize(self, *args, **kwds):
        '''
        Minimizes the objective function and returns a solution instance.
        @param solution={}: optional primal solution dictionary.  Raises a
                            SolverError if the solution is infeasible.
        '''
        super(solver, self).minimize(*args, **kwds)
        return solution(self)
        
