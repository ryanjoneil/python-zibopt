from itertools import product
from zibopt._variable import variable

__all__ = 'term', 'expression'

class term(object):
    def __init__(self, variables, coefficient=1.0):
        self.variables   = frozenset(variables)
        self.coefficient = coefficient

#    def __hash__(self):
#        return hash(self.variables)
#
#    def __eq__(self, other):
#        # For purposes of constructing expressions, two terms
#        # are the same if they have the same variables.  This
#        # allows us to add coefficients, etc.
#        return self.variables == other.variables

    def __add__(self, other):
        # Other can be another term, a variable, or a number
        # TODO: is this necessary?
        #if isinstance(other, expression):
        #    return expression([self]) + other
        if isinstance(other, type(self)):
            if self.variables == other.variables:
                return term(self.variables, self.coefficient + other.coefficient)
            return expression([self, other])

        elif isinstance(other, variable):
            return self + term([other])

        else:
            assert False # TODO

    def __sub__(self, other):
        return self + (-1) * other

    def __mul__(self, other):
        # TODO: expression?
        # Other can be a variable or another term
        if isinstance(other, type(self)):
            return type(self)(
                self.variables.union(other.variables), 
                self.coefficient * other.coefficient
            )
        elif isinstance(other, variable):
            return type(self)(self.variables.union([other]), self.coefficient)
        else:
            return type(self)(self.variables, self.coefficient * other)

    def __div__(self, other):
        # TODO: expression?
        # Other can be a variable or another term
        if isinstance(other, type(self)):
            assert False # TODO
        elif isinstance(other, variable):
            assert False # TODO
        else:
            return type(self)(self.variables, self.coefficient / other)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__        

    __truediv__  = __div__
    __rtruediv__ = __div__

class expression(object):
    def __init__(self, terms):
        self.terms = {t.variables:t for t in terms}

    def __getitem__(self, key):
        return self.terms[key]

    def __add__(self, other):
        if isinstance(other, type(self)):
            terms = {}
            for v, t in self.terms.items():
                terms[v] = term(t.variables, t.coefficient)
            for v, t in other.terms.items():
                try:
                    terms[v] += term(t.variables, terms[v].coefficient + t.coefficient)
                except KeyError:
                    terms[v] = term(t.variables, t.coefficient)

            return type(self)(terms.values())

        assert False

    def __mul__(self, other):
        if isinstance(other, type(self)):
            # (x + y) * (x - y) logic
            coefficients = {}
            for t1, t2 in product(self.terms.values(), other.terms.values()):
                v = t1.variables.union(t2.variables)
                c = t1.coefficient * t2.coefficient
                try:
                    coefficients[v] += c
                except KeyError:
                    coefficients[v] = c
            
            return type(self)([
                term(variables=v, coefficient=c)
                for v, c in coefficients.items()
            ])

        elif isinstance(other, term):
            # x * (x + y)
            return self * expression([other])

        else:
            # 2 * (x + y)
            return type(self)([
                term(t.variables, coefficient=t.coefficient * other)
                for t in self.terms.values()
            ])
        
    def __sub__(self, other):
        return self + (-1) * other
    
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__        

