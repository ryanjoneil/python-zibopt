from zibopt import _vars
from zibopt._expression import expression

__all__ = 'variable', 'VariableError'

VariableError = _vars.error

class variable(_vars.variable):
    # This class exists solely to allow algebraic notation for constraints
    # and objective functions.  It shouldn't be used directly.  Instead use
    # the variable method on the solver.
    
#    class _cons_builder(object):
#        # Constraint builder class: used for allowing mathematical operations 
#        # in generating constraints
#        def __init__(self, var):
#            if isinstance(var, type(self)):
#                self.coefficients = var.coefficients.copy()
#                self.lower = var.lower # bounds
#                self.upper = var.upper
#            else:
#                self.coefficients = {var: 1.0}
#                self.lower = self.upper = None
#        
#        def __add__(self, other):
#            # Filter out 0s from sum(...)
#            if other is 0:
#                return self
#        
#            # If we are adding a variable to a _cons_builder, convert it
#            if not isinstance(other, type(self)):
#                other = type(self)(other)
#            
#            # Add the coefficients of the other _cons_builder to our dict
#            for var, coeff in other.coefficients.items():
#                try:
#                    self.coefficients[var] += coeff
#                except KeyError:
#                    self.coefficients[var] = coeff
#                    
#            return self
#
#        def __sub__(self, other):
#            # This looks a lot like __add__
#            if other is 0:
#                return self
#
#            if not isinstance(other, type(self)):
#                other = type(self)(other)
#            
#            for var, coeff in other.coefficients.items():
#                try:
#                    self.coefficients[var] -= coeff
#                except KeyError:
#                    self.coefficients[var] = -coeff
#                    
#            return self
#
#        def __mul__(self, other):
#            # other should always be a number
#            other = float(other)
#            for var, coeff in self.coefficients.items():
#                self.coefficients[var] *= other
#            return self
#
#        def __div__(self, other):
#            return self * (1.0 / other)
#
#        # Provide methods for reflected versions of the same operators
#        __radd__ = __add__
#        __rsub__ = __sub__
#        __rmul__ = __mul__
#        __rdiv__ = __div__
# 
#        __truediv__  = __div__
#        __rtruediv__ = __div__
#        
#        # This part allows <=, >= and == to populate lower/upper bounds
#        def __le__(self, other):
#            self.upper = float(other)
#            return self            
#
#        def __ge__(self, other):
#            self.lower = float(other)
#            return self            
#
#        def __eq__(self, other):
#            self.lower = self.upper = float(other)
#            return self            

    # TODO: is this the right thing to do given logic below for <=, ==, >=?
    #       i think it is... but make sure
    def __lt__(self, other):
        return id(self) < id(other)

    def __gt__(self, other):
        return id(self) > id(other)
    
    def __init__(self, *args, **kwds):
        # Stores a few things locally that will not interfer with the C version
        super(variable, self).__init__(*args, **kwds)
        self._upper_bnd = self._lower_bnd = None # see __iadd__ below
    
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

    # Single-variable bounds
    def __le__(self, other):
        # In cases with one variable, like:  0 <= x <= 1
        # What we want to do is try adjusting its bounds.
        # TODO: allow for x2 <= 4, x2 <= x1, etc
        self._upper_bnd = float(other)
        return self
        
    def __ge__(self, other):
        # TODO: allow for x2 >= 4, x2 >= x1, etc
        self._lower_bnd = float(other)
        return self

    def __eq__(self, other):
        # TODO: allow for x2 == 4, x2 == x1, etc
        self._lower_bnd = self._upper_bnd = float(other)
        return self

    def __hash__(self):
        return hash(id(self))

    def __getattr__(self, attr):
        return super(variable, self).__getattr__(attr)

