from zibopt import _scip
from zibopt import (
    _branch, _conflict, _disp, _heur, _nodesel, _presol, _prop, _sepa
)
from zibopt._constraint import constraint
from zibopt._expression import expression
from zibopt._solution import solution
from zibopt._variable import variable
import sys

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

        self.branching   = {n:_branch.branching_rule(self, n) for n in self.branching_names()}
        self.conflict    = {n:_conflict.conflict(self, n) for n in self.conflict_names()}
        self.display     = {n:_disp.display_column(self, n) for n in self.display_names()}
        self.heuristics  = {n:_heur.heuristic(self, n) for n in self.heuristic_names()}
        self.presolvers  = {n:_presol.presolver(self, n) for n in self.presolver_names()}
        self.propagators = {n:_prop.propagator(self, n) for n in self.propagator_names()}
        self.selectors   = {n:_nodesel.selector(self, n) for n in self.selector_names()}
        self.separators  = {n:_sepa.separator(self, n) for n in self.separator_names()}

    def __iadd__(self, expr):
        '''
        Allows a constraint to be added using a more natural algebraic format.
        Note that this does *not* return the constraint, so if you want to
        remove the constraint later, use solver.constraint(...).

            solver += 1 <= x1 + 2*x2 <= 2

        Alternatively, if the constraint already exists in a variable and
        has been removed, it may be reintroduced into the solver this way.

            solver += some_constraint
        '''
        if isinstance(expr, constraint):
            # Is already a constraint
            self.constrain(expr)
        else:
            # Is a zibopt._variable._cons_builder instance
            self.constraint(expr)
            
        return self

    def __isub__(self, constraint):
        '''
        Allows a constraint to be removed after it was added.  Note that
        the only way to properly construct and store constraints in variables
        is using the solver.constraint(...) method.

            some_constraint = solver.constraint(2*x1 + 2*x2 <= 4)
            solver.maximize(objective=x1+x2)
            solver -= some_constraint
        '''
        self.unconstrain(constraint)
        return self

    def _update_coefficients(self, expr):
        '''Allows use of algebraic format for objective functions'''
        # Clear out old coefficients.  This may require freeing the transformed
        # problem, thus the restart.
        self.restart()

        # Make sure it's actually an expression.  It could be a constant or 
        # a variable as well, such as: solver.maximize(objective=x1)
        if isinstance(expr, variable):
            expr = expression({(expr,):1.0})
        elif isinstance(expr, int) or isinstance(expr, float):
            expr = expression({():expr})

        # If it is an expression, make sure there are no bounds on it
        # because that wouldn't make any sense.
        if expr.upper is not None or expr.lower is not None:
            raise SolverError('objective functions should not have bounds')

        # It appears SCIP only allows linear expression for objective
        # functions, so if we get something with bilinear terms, set 
        # that equal to an unbounded variable, min/max that variable.
        for term in expr.terms:
            if len(term) > 1:
                z = self.variable(lower=-sys.maxsize)
                self += z == expr
                expr = expression({(z,):1.0})
                break

        # Now set linear coefficients on the objective function
        for v in self.variables:
            try:
                v.set_coefficient(expr[(v,)])
            except:
                v.set_coefficient(0)

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

    def constraint(self, expression):
        '''
        Adds a constraint to the solver.  Returns the constraint. The user 
        can create the constraint out of keyword arguments or algebraically.
        For instance, the following two statements are equivalent:

            solver.constraint(x1 + 2*x2 <= 4)

            solver.constraint(
                expression(
                    terms = {
                        (x1,): 1.0,
                        (x2,): 2.0
                    },
                    upper = 4
                )
            )

        @param expression: zibopt.expression instance
        '''
        cons = constraint(self, expression)
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
            self._update_coefficients(kwds.pop('objective'))
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
            self._update_coefficients(kwds.pop('objective'))
        super(solver, self).minimize(*args, **kwds)
        return solution(self)
        
