from zibopt import _vars
from zibopt._expression import expression

__all__ = 'variable', 'VariableError'

VariableError = _vars.error

class variable(_vars.variable):
    def __init__(self, *args, **kwds):
        super(variable, self).__init__(*args, **kwds)

        # We do this to allow single variable bounds: 0 <= x <= 4
        self.lower = None
        self.upper = None

    def __hash__(self):
        return hash(id(self))

    # Convert variables into expression instances on math operations
    def __add__(self, other):
        return expression({(self,):1.0}) + other

    def __sub__(self, other):
        return expression({(self,):1.0}) - other

    def __mul__(self, other):
        return expression({(self,):1.0}) * other

    def __neg__(self):
        return expression({(self,):-1.0})

    def __pos__(self):
        return expression({(self,):1.0})

    def __pow__(self, x):
        if isinstance(x, int) and x >= 0:
            if x == 0:
                return expression({():1.0})
            else:
                return expression({(self,)*x:1.0})

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    
    # These exist for sorting variables and have nothing to do with <=, etc
    def __lt__(self, other):
        return id(self) < id(other)

    def __gt__(self, other):
        return id(self) > id(other)
    
    # These allow single-variable bounds
    def __le__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            self.upper = other
            return self
        else:
            return expression({(self,):1.0}) <= other
        
    def __ge__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            self.lower = other
            return self
        else:
            return expression({(self,):1.0}) >= other

    def __eq__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            self.lower = other
            self.upper = other
            return self
        else:
            return expression({(self,):1.0}) == other

