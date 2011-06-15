from itertools import product

__all__ = 'expression',

class expression(object):
    def __init__(self, terms={}):
        '''
        Instantiates an algebraic expression.  This is assumed to be a 
        sum of sets of variables which are multiplied.

        @param terms: {(tuple of variables): coefficient, ...}
        '''
        # Terms should be {(variable sequence): coefficient}
        self.terms = {tuple(sorted(v)):c for v, c in terms.items()}

    def __getitem__(self, key):
        return self.terms[key]

    def __add__(self, other):
        if isinstance(other, type(self)):
            # x + y
            terms = self.terms.copy()
            for v, c in other.terms.items():
                terms[v] = terms.get(v, 0.0) + c

            return type(self)(terms)

        elif isinstance(other, int) or isinstance(other, float):
            # x + 1
            terms = self.terms.copy()
            terms[()] = terms.get((), 0.0) + other
            return type(self)(terms)

        return NotImplemented
        
    def __sub__(self, other):
        # x - y
        # x - 2
        return self + (-1) * other

    def __mul__(self, other):
        if isinstance(other, type(self)):
            # (x + y) * (x * y)
            # (x + y) * (v - w) 
            # x * (y - z)
            terms = {}
            for v1, v2 in product(self.terms, other.terms):
                v = tuple(sorted(v1 + v2))
                c = self.terms.get(v1, 1.0) * other.terms.get(v2, 1.0)
                terms[v] = terms.get(v, 0.0) + c
            
            return type(self)(terms)

        elif isinstance(other, int) or isinstance(other, float):
            # 2 * (x + y)
            return type(self)({
                v:c*float(other) for v, c in self.terms.items()
            })

        return NotImplemented

    def __div__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            # x / 2
            return self * (1.0/other)

        return NotImplemented

    
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__        
    __rdiv__ = __div__
 
    __truediv__  = __div__
    __rtruediv__ = __div__

