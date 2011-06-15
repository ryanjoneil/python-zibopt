from zibopt import _vars
from zibopt._expression import expression

__all__ = 'variable', 'VariableError'

VariableError = _vars.error

class variable(_vars.variable):
    def __init__(self, *args, **kwds):
        # Stores a few things locally that will not interfer with the C version
        super(variable, self).__init__(*args, **kwds)
    
    def __hash__(self):
        return hash(id(self))

    def __getattr__(self, attr):
        return super(variable, self).__getattr__(attr)

    # Convert variables into _cons_builder instances on all math ops
    def __add__(self, other):
        # TODO: deal with sum 
        # # Using sum(...) will put a 0 in the list
        # if other is 0:
        #     return self._cons_builder(self)
        return expression({(self,):1.0}) + other

    def __sub__(self, other):
        # TODO: deal with sum
        #if other is 0:
        #    return self._cons_builder(self)
        return expression({(self,):1.0}) - other

    def __mul__(self, other):
        return expression({(self,):1.0}) * other

    def __div__(self, other):
        return expression({(self,):1.0}) * other

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    
    __truediv__  = __div__
    __rtruediv__ = __div__

    # These exist for sorting variables and have nothing to do with <=, etc
    def __lt__(self, other):
        return id(self) < id(other)

    def __gt__(self, other):
        return id(self) > id(other)
    
    # These allow single-variable bounds
    def __le__(self, other):
        return expression({(self,):1.0}) <= other
        
    def __ge__(self, other):
        return expression({(self,):1.0}) >= other

    def __eq__(self, other):
        return expression({(self,):1.0}) == other

