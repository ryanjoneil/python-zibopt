from zibopt import _scip, _vars, _cons, _soln

BINARY     = _scip.BINARY
INTEGER    = _scip.INTEGER
IMPLINT    = _scip.IMPLINT
CONTINUOUS = _scip.CONTINUOUS

ConstraintError = _cons.error
SolutionError   = _soln.error
SolverError     = _scip.error
VariableError   = _vars.error

class solution(_soln.solution):
    def __init__(self, solver):
        super(solution, self).__init__(solver)
        self.solver = solver

    def __nonzero__(self):
        return bool(self.feasible)
    
    def values(self):
        vals = {}
        for v in self.solver.variables:
            vals[v] = self.value(v)
        return vals

class solver(_scip.solver):
    def __init__(self, *args, **kwds):
        super(solver, self).__init__(*args, **kwds)
        self.variables = set()
        self.constraints = set()

    def variable(self, coefficient=0, vartype=CONTINUOUS, lower=0, **kwds):
        v = _vars.variable(self, coefficient, vartype, lower, **kwds)
        self.variables.add(v)
        return v

    def constraint(self, **kwds):
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

    def maximize(self):
        super(solver, self).maximize()
        return solution(self)
        
    def minimize(self):
        super(solver, self).minimize()
        return solution(self)
        
