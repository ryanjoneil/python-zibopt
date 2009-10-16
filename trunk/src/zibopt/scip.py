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
        print 'invalid problem'
'''

from zibopt import _scip, _vars, _cons, _soln, _branch, _sepa

__all__ = 'solver',

BINARY     = _scip.BINARY
INTEGER    = _scip.INTEGER
IMPLINT    = _scip.IMPLINT
CONTINUOUS = _scip.CONTINUOUS

ConstraintError    = _cons.error
SolutionError      = _soln.error
SolverError        = _scip.error
VariableError      = _vars.error
BranchingRuleError = _branch.error

class solution(_soln.solution):
    '''
    A solution to a mixed integer program from SCIP.  Solution values can
    be obtained using variable references from the solver:
    
        x1_value = solution[x1]
    
    If a solution is infeasible or unbounded, it will be false when evaluated
    in boolean context:
    
        if solution:
            # do something interesting
    
    Solutions can be tested for optimality using the solution.optimal boolean.
    Available solution statuses include:
    
        solution.optimal:     solution is optimal
        solution.infeasible:  no feasible solution could be found
        solution.unbounded:   solution is unbounded
        solution.inforunbd:   solution is either infeasible or unbounded
    '''
    def __init__(self, solver):
        super(solution, self).__init__(solver)
        self.solver = solver

    def __nonzero__(self):
        return not (self.infeasible or self.unbounded or self.inforunbd)
    
    def __getitem__(self, key):
        return self.value(key)
    
    def values(self):
        vals = {}
        for v in self.solver.variables:
            vals[v] = self.value(v)
        return vals

class solver(_scip.solver):
    '''
    A SCIP mixed integer programming solver.  Normal behavior is to instantiate
    a solver, define variables and constraints for it, and then maximize or
    minimize an objective function.
    
    Solver settings for things like branching rules are accessible through 
    dictionaries on the solver.  For instance, to change settings on the
    inference branching rule:
    
        solver.branching['inference'].priority = 10000
        solver.branching['inference'].maxdepth = -1
        solver.branching['inference'].maxbounddist = -1
    '''
    def __init__(self, *args, **kwds):
        '''
        Instantiates a solver with default settings.
        @param quiet=True: turns the SCIP solver output off
        '''
        super(solver, self).__init__(*args, **kwds)
        self.variables = set()
        self.constraints = set()

        self.branching = dict(
            (name, _branch.branching_rule(self, name))
            for name in self.branching_rules()
        )
        
        self.separators = dict(
            (name, _sepa.separator(self, name))
            for name in self.separators()
        )

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
        @param time=inf:    optional time limit for solving
        @param gap=0.0:     optional gap percentage to stop solving (ex: 0.05)
        @param absgap=0.0:  optional primal/dual gap to stop solving
        '''
        super(solver, self).maximize(*args, **kwds)
        return solution(self)
        
    def minimize(self, *args, **kwds):
        '''
        Minimizes the objective function and returns a solution instance.
        @param solution={}: optional primal solution dictionary.  Raises a
                            SolverError if the solution is infeasible.
        @param time=inf:    optional time limit for solving
        @param gap=0.0:     optional gap percentage to stop solving (ex: 0.05)
        @param absgap=0.0:  optional primal/dual gap to stop solving
        '''
        super(solver, self).minimize(*args, **kwds)
        return solution(self)
        
