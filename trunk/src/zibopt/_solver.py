from zibopt import _scip
from zibopt import (
    _branch, _conflict, _disp, _heur, _nodesel, _presol, _prop, _sepa
)
from zibopt._constraint import constraint
from zibopt._solution import solution
from zibopt._variable import variable

__all__ = 'solver', 'SolverError', 'BINARY', 'INTEGER', 'IMPLINT', 'CONTINUOUS'

BINARY     = _scip.BINARY
INTEGER    = _scip.INTEGER
IMPLINT    = _scip.IMPLINT
CONTINUOUS = _scip.CONTINUOUS

SolverError = _scip.error

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

    Display settings can also be set for solver output.  These are
    useful when passing quiet=False on solver instantiation:

        solver = scip.solver()
        solver.display['cuts'].priority = 5
        solver.display['cuts'].width = 10
        solver.display['cuts'].position = 3

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
        self.display     = dict((n, _disp.display_column(self, n)) for n in self.display_names())
        self.heuristics  = dict((n, _heur.heuristic(self, n)) for n in self.heuristic_names())
        self.presolvers  = dict((n, _presol.presolver(self, n)) for n in self.presolver_names())
        self.propagators = dict((n, _prop.propagator(self, n)) for n in self.propagator_names())
        self.selectors   = dict((n, _nodesel.selector(self, n)) for n in self.selector_names())
        self.separators  = dict((n, _sepa.separator(self, n)) for n in self.separator_names())

    def __iadd__(self, cons_info):
        '''
        Allows a constraint to be added using a more natural algebraic format.
        Note that this does *not* return the constraint, so if you want to
        remove the constraint later, use solver.constraint(...).

            solver += 1 <= x1 + 2*x2 <= 2

        Alternatively, if the constraint already exists in a variable and
        has been removed, it may be reintroduced into the solver this way.

            solver += some_constraint
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
            
        elif isinstance(cons_info, constraint):
            self.constrain(cons_info)

        else:
            self.constraint(
                lower = cons_info.lower,
                upper = cons_info.upper,
                coefficients = cons_info.coefficients
            )
            
        return self

    def __isub__(self, constraint):
        '''
        Allows a constraint to be removed after it was added.  Note that
        the only way to properly construct and store constraints in variables
        is using the solver.constraint(...) method.

            some_constraint = solver.constraint(
                upper = 4,
                coefficients = {x1: 2, x2: 2}
            )
            solver.maximize(objective=x1+x2)
            solver -= some_constraint
        '''
        self.unconstrain(constraint)
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
        @param priority=0:         branching priority for variable
        '''
        v = variable(self, vartype, coefficient, lower, **kwds)
        self.variables.add(v)
        return v

    def constraint(self, **kwds):
        '''
        Adds a constraint to the solver.  Returns the constraint.
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
            
        cons = constraint(self, **kwds)
        for k, v in coefficients.items():
            cons.variable(k, v)

        self.constrain(cons)
        return cons

    def constrain(self, constraint):
        '''
        Adds a constraint back into the solver. Returns None.
        @param constraint: constraint instance to reinstall
        '''
        if constraint not in self.constraints:
            constraint.register()
            self.constraints.add(constraint)

    def unconstrain(self, constraint):
        '''
        Removes a constraint from the solver.  Returns None.
        @param constraint: constraint instance to remove
        '''
        if constraint in self.constraints:
            self.constraints.remove(constraint)
            super(solver, self).unconstrain(constraint)

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
        @param nsol=-1:     number of solutions to find before stopping
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
        @param nsol=-1:     number of solutions to find before stopping
        '''
        if 'objective' in kwds:
            self._update_coefficients(kwds['objective'])
            del kwds['objective']
        super(solver, self).minimize(*args, **kwds)
        return solution(self)
        
