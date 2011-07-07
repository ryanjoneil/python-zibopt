from zibopt import _vars
from zibopt._expression import expression

__all__ = 'variable', 'VariableError'

VariableError = _vars.error

class variable(_vars.variable, expression):
    '''Provides a hashable and orderable Python connector to SCIP variables.'''
    def __init__(self, *args, **kwds):
        _vars.variable.__init__(self, *args, **kwds)
        expression.__init__(self, {(self,):1.0})

    def __hash__(self):
        return hash(id(self))

    def __pow__(self, x):
        if isinstance(x, int) and x >= 0:
            if x == 0:
                return expression({():1.0})
            else:
                return expression({(self,)*x:1.0})

        return NotImplementedError

    # These exist for sorting variables and have nothing to do with <=, etc
    def __lt__(self, other):
        return id(self) < id(other)

    def __gt__(self, other):
        return id(self) > id(other)

