from zibopt import _scip, _vars, _cons, _soln

class variable(_vars.variable):
    def __init__(self, solver, name, coefficient=0):
        super(variable, self).__init__(solver, name, coefficient)
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
    def __init__(self, solver, name):
        super(variable, self).__init__(solver, name, coefficient)
        self.solver = solver
        self.name = name
        self.coefficient = coefficient

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
        return dict((v, self.value(v)) for v in self.solver.variables)

class solver(_scip.solver):
    def __init__(self, *args, **kwds):
        super(solver, self).__init__(*args, **kwds)
        self.variables = set()

    def variable(self, name, coefficient=0):
        self.variables.add(variable(self, name, coefficient))

    def maximize(self):
        super(solver, self).maximize()
        # TODO: what to do about infeasibility?
        return solution(self)#, self.variables)
        
    def minimize(self):
        super(solver, self).minimize()
        return solution(self)#, self.variables)
        
