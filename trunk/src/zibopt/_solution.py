from zibopt import _soln

__all__ = 'solution', 'SolutionError'

SolutionError = _soln.error

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

    def __bool__(self):
        return not (self.infeasible or self.unbounded or self.inforunbd)
    
    def __getitem__(self, key):
        return self.value(key)
    
    def values(self):
        vals = {}
        for v in self.solver.variables:
            vals[v] = self.value(v)
        return vals

