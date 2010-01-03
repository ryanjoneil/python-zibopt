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

from zibopt import (
    _scip, _vars, _cons, _soln, 
    _branch, _conflict, _heur, _nodesel, _presol, _prop, _sepa
)

__all__ = 'solver',

BINARY     = _scip.BINARY
INTEGER    = _scip.INTEGER
IMPLINT    = _scip.IMPLINT
CONTINUOUS = _scip.CONTINUOUS

ConstraintError = _cons.error
SolutionError   = _soln.error
SolverError     = _scip.error
VariableError   = _vars.error

# Solver Settings Errors
BranchingError  = _branch.error
ConflictError   = _conflict.error
HeuristicError  = _heur.error
PresolverError  = _presol.error
PropagatorError = _prop.error
SelectorError   = _nodesel.error
SeparatorError  = _sepa.error

class variable(_vars.variable):
    class _cons_builder(object):
        # Constraint builder class: used for allowing mathematical operations 
        # in generating constraints
        def __init__(self, var):
            if isinstance(var, type(self)):
                self.coefficients = var.coefficients.copy()
                self.lower = var.lower # bounds
                self.upper = var.upper
            else:
                self.coefficients = {var: 1.0}
                self.lower = self.upper = None
        
        def __add__(self, other):
            # Filter out 0s from sum(...)
            if other is 0:
                return self
        
            # If we are adding a variable to a _cons_builder, convert it
            if not isinstance(other, type(self)):
                other = type(self)(other)
            
            # Add the coefficients of the other _cons_builder to our dict
            for var, coeff in other.coefficients.iteritems():
                try:
                    self.coefficients[var] += coeff
                except KeyError:
                    self.coefficients[var] = coeff
                    
            return self

        def __sub__(self, other):
            # This looks a lot like __add__
            if other is 0:
                return self

            if not isinstance(other, type(self)):
                other = type(self)(other)
            
            for var, coeff in other.coefficients.iteritems():
                try:
                    self.coefficients[var] -= coeff
                except KeyError:
                    self.coefficients[var] = -coeff
                    
            return self

        def __mul__(self, other):
            # other should always be a number
            other = float(other)
            for var, coeff in self.coefficients.iteritems():
                self.coefficients[var] *= other
            return self

        def __div__(self, other):
            return self * (1.0 / other)

        # Provide methods for reflected versions of the same operators
        __radd__ = __add__
        __rsub__ = __sub__
        __rmul__ = __mul__
        __rdiv__ = __div__
 
        __truediv__  = __div__
        __rtruediv__ = __div__
        
        # This part allows <=, >= and == to populate lower/upper bounds
        def __le__(self, other):
            self.upper = float(other)
            return self            

        def __ge__(self, other):
            self.lower = float(other)
            return self            

        def __eq__(self, other):
            self.lower = self.upper = float(other)
            return self            
    
    def __init__(self, *args, **kwds):
        # Stores a few things locally that will not interfer with the C version
        super(variable, self).__init__(*args, **kwds)
        self._upper_bnd = self._lower_bnd = None # see __iadd__ below
    
    # Convert variables into _cons_builder instances on all math ops
    def __add__(self, other):
        # Using sum(...) will put a 0 in the list
        if other is 0:
            return self._cons_builder(self)
        return self._cons_builder(self) + self._cons_builder(other)

    def __sub__(self, other):
        if other is 0:
            return self._cons_builder(self)
        return self._cons_builder(self) - self._cons_builder(other)

    def __mul__(self, other):
        return self._cons_builder(self) * other

    def __div__(self, other):
        return self._cons_builder(self) / other

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    
    __truediv__  = __div__
    __rtruediv__ = __div__

    # Single-variable bounds
    def __le__(self, other):
        # In cases with one variable, like:  0 <= x <= 1
        # What we want to do is try adjusting its bounds.
        self._upper_bnd = float(other)
        return self
        
    def __ge__(self, other):
        self._lower_bnd = float(other)
        return self

    def __eq__(self, other):
        self._lower_bnd = self._upper_bnd = float(other)
        return self

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
        
    Heuristcs allow priority, max depth, frequency, and frequency offset
    (freqofs) to be set:
    
        solver.heuristics['octane'].priority = 500
        solver.heuristics['octane'].maxdepth = -1
        solver.heuristics['octane'].frequency = 10
        solver.heuristics['octane'].freqofs = 5

    Node selectors have standard and memory saving priority:
    
        solver.selectors['bfs'].stdpriority = 1000
        solver.selectors['bfs'].memsavepriority = 10
    
    Propagotors allow priority and frequencey to be set:
    
        solver.propagators['pseudoobj'].priority = 1000
        solver.propagators['pseudoobj'].frequency = 10
        
    Separators have settinsg for priority, maxbounddist, and frequency:

        solver.separators['clique'].priority = 10000
        solver.separators['clique'].maxbounddist = -1
        solver.separators['clique'].frequency = 10000
    
    Priority can also be set on conflict handlers and presolvers:
    
        solver.conflict['logicor'].priority = 10000
        solver.presolvers['dualfix'].priority = 10000

    See the SCIP documentation for available branching rules, heuristics, 
    any other settings, and what they do.
    '''
    def __init__(self, *args, **kwds):
        '''
        Instantiates a solver with default settings.
        @param quiet=True: turns the SCIP solver output off
        '''
        super(solver, self).__init__(*args, **kwds)
        self.variables = set()
        self.constraints = set()

        self.branching   = dict((n, _branch.branching_rule(self, n)) for n in self.branching_names())
        self.conflict    = dict((n, _conflict.conflict(self, n)) for n in self.conflict_names())
        self.heuristics  = dict((n, _heur.heuristic(self, n)) for n in self.heuristic_names())
        self.presolvers  = dict((n, _presol.presolver(self, n)) for n in self.presolver_names())
        self.propagators = dict((n, _prop.propagator(self, n)) for n in self.propagator_names())
        self.selectors   = dict((n, _nodesel.selector(self, n)) for n in self.selector_names())
        self.separators  = dict((n, _sepa.separator(self, n)) for n in self.separator_names())

    def __iadd__(self, cons_info):
        '''
        Allows a constraint to be added using a more natural algebraic format:
        
            solver += 1 <= x1 + 2*x2 <= 2
        '''
        # This is some annoying magic here.  If we write a constraint like:
        #     0 <= x <= 1
        # Python will apply the variable instance to each inequality, losing
        # anything done along the way.  Thus we have to store the new upper and
        # lower bounds on the variable.  Sad.  This gets rid of them after the 
        # boundes are updated.
        if isinstance(cons_info, variable):
            if cons_info._upper_bnd is not None:
                cons_info.tighten_upper_bound(cons_info._upper_bnd)
            if cons_info._lower_bnd is not None:
                cons_info.tighten_lower_bound(cons_info._lower_bnd)
            cons_info._upper_bnd = cons_info._lower_bnd = None
            
        else:
            self.constraint(
                lower = cons_info.lower,
                upper = cons_info.upper,
                coefficients = cons_info.coefficients
            )
            
        return self

    def _update_coefficients(self, obj_info):
        '''Allows use of algebraic format for objective functions'''
        # Clear out old coefficients.  This may require freeing the transformed
        # problem, thus the restart.
        self.restart()
        for v in self.variables:
            v.set_coefficient(obj_info.coefficients.get(v, 0))

    def variable(self, vartype=CONTINUOUS, coefficient=0, lower=0, **kwds):
        '''
        Adds a variable to the SCIP solver and returns it
        @param vartype=CONTINUOUS: type of variable
        @param coefficient=0:      objective function coefficient
        @param lower=0:            lower bound on variable
        @param upper=+inf:         upper bound on variable
        '''
        v = variable(self, vartype, coefficient, lower, **kwds)
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

        # If upper or lower bounds are None, remove them to be polite
        if 'lower' in kwds and kwds['lower'] is None:
            del kwds['lower']
        if 'upper' in kwds and kwds['upper'] is None:
            del kwds['upper']
            
        cons = _cons.constraint(self, **kwds)
        for k, v in coefficients.iteritems():
            cons.variable(k, v)

        cons.register()
        self.constraints.add(cons)

    def maximize(self, *args, **kwds):
        '''
        Maximizes the objective function and returns a solution instance.
        @param objective:   optional algebraic representation of objective
                            function.  Can also use variable coefficients.
        @param solution={}: optional primal solution dictionary.  Raises a
                            SolverError if the solution is infeasible.
        @param time=inf:    optional time limit for solving
        @param gap=0.0:     optional gap percentage to stop solving (ex: 0.05)
        @param absgap=0.0:  optional primal/dual gap to stop solving
        '''
        if 'objective' in kwds:
            self._update_coefficients(kwds['objective'])
            del kwds['objective']
        super(solver, self).maximize(*args, **kwds)
        return solution(self)
        
    def minimize(self, *args, **kwds):
        '''
        Minimizes the objective function and returns a solution instance.
        @param objective:   optional algebraic representation of objective
                            function.  Can also use variable coefficients.
        @param solution={}: optional primal solution dictionary.  Raises a
                            SolverError if the solution is infeasible.
        @param time=inf:    optional time limit for solving
        @param gap=0.0:     optional gap percentage to stop solving (ex: 0.05)
        @param absgap=0.0:  optional primal/dual gap to stop solving
        '''
        if 'objective' in kwds:
            self._update_coefficients(kwds['objective'])
            del kwds['objective']
        super(solver, self).minimize(*args, **kwds)
        return solution(self)
        
