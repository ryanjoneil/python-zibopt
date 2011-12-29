from algebraic import variable as algvar
from zibopt import _vars

__all__ = 'variable', 'VariableError'

VariableError = _vars.error

class variable(_vars.variable, algvar):
    '''Provides a hashable and orderable Python connector to SCIP variables.'''
    def __init__(self, *args, **kwds):
        _vars.variable.__init__(self, *args, **kwds)
        algvar.__init__(self, *args, **kwds)
