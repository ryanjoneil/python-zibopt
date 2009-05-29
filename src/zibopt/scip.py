from zibopt import _scip, _vars, _cons, _soln

BINARY     = _scip.BINARY
INTEGER    = _scip.INTEGER
CONTINUOUS = _scip.CONTINUOUS

class variable(_vars.variable):
    def __init__(self, solver, name, coefficient=0, vartype=CONTINUOUS, lower=0, **kwds):
        super(variable, self).__init__(solver, name, coefficient, vartype, lower, **kwds)
        self.solver = solver
        self.name = name
        self.coefficient = coefficient

    def __hash__(self):
        return hash(self.name)
    
    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __repr__(self):
        return self.name

class constraint(_cons.constraint):
    def __init__(self, solver, name, **kwds):
        super(constraint, self).__init__(solver, name, **kwds)
        self.solver = solver
        self.name = name

    def __hash__(self):
        return hash(self.name)
    
    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __repr__(self):
        return self.name

class solution(_soln.solution):
    def __init__(self, solver):
        super(solution, self).__init__(solver)
        self.solver = solver
    
    def values(self):
        vals = {}
        for v in self.solver.variables.itervalues():
            x = self.value(v)
            if x:
                vals[v] = x
        return vals

class solver(_scip.solver):
    def __init__(self, *args, **kwds):
        super(solver, self).__init__(*args, **kwds)
        self.variables = {}
        self.constraints = set()

    def variable(self, name, coefficient=0, vartype=CONTINUOUS, lower=0, **kwds):
        self.variables[name] = variable(self, name, coefficient, vartype, lower, **kwds)

    def constraint(self, name, **kwds):
        # Yank out variable coefficients since C code isn't expecting them
        try:
            coefficients = kwds['coefficients']
            del kwds['coefficients']
        except KeyError:
            coefficients = {}            
                    
        cons = constraint(self, name, **kwds)
        for k, v in coefficients.iteritems():
            cons.variable(self.variables[k], v)
        cons.register()
        self.constraints.add(cons)

    def maximize(self):
        super(solver, self).maximize()
        # TODO: what to do about infeasibility?
        return solution(self)
        
    def minimize(self):
        super(solver, self).minimize()
        return solution(self)
        
