from itertools import product

__all__ = 'expression', 'inequality'

class expression(object):
    def __init__(self, terms={}, lower=None, upper=None):
        '''
        Instantiates an algebraic expression.  This is assumed to be a 
        sum of sets of variables which are multiplied.

        @param terms: {(tuple of variables): coefficient, ...}
        @param lower: lower bound
        @param lower: upper bound
        '''
        # Terms should be {(variable sequence): coefficient}
        self.terms = {tuple(sorted(v)):c for v, c in terms.items()}
        self.lower = lower
        self.upper = upper

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

    def __neg__(self):
        # -(x * y)
        return type(self)({v:-c for v, c in self.terms.items()})

    def __pos__(self):
        # +(x * y)
        return self

    def __pow__(self, x):
        if isinstance(x, int) and x >= 0:
            if len(self.terms) == 1:
                # (2 * x) ** 4
                for term, c in self.terms.items():
                    # Make sure we only have one variable
                    if len(set(term)) == 1:
                        variables = term * x
                        coefficient = c ** x
                        return type(self)({variables:coefficient})

            elif len(self.terms) == 2 and () in self.terms:
                # (2 * x**3) ** 4
                e = type(self)({():1.0})
                for _ in range(x):
                    e = e * self
                return e
                
        return NotImplemented
    
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__        
    __rdiv__ = __div__
 
    __truediv__  = __div__
    __rtruediv__ = __div__

    # This part allows <=, >= and == to populate lower/upper bounds
    def __le__(self, other):
        if isinstance(other, type(self)):
            e = self - other
            c = 0.0 - e.terms.pop((), 0.0)
            return inequality(e, upper=c)

        elif isinstance(other, int) or isinstance(other, float):
            # x + y <= 1
            return self <= type(self)({():other})

        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, type(self)):
            e = self - other
            c = 0.0 - e.terms.pop((), 0.0)
            return inequality(e, lower=c)

        elif isinstance(other, int) or isinstance(other, float):
            # x + y >= 1
            return self >= type(self)({():other})         

        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, type(self)):
            e = self - other
            c = 0.0 - e.terms.pop((), 0.0)
            return inequality(e, lower=c, upper=c)

        elif isinstance(other, int) or isinstance(other, float):
            # x + y == 1
            return self == type(self)({():other})         

        return NotImplemented           

class inequality(object):
    '''
    Represents an expression with an upper and/or lower bound.
    Valid inequalitites look like:

        x <= 4
        x >= y
        x <= z*(x + y**2) <= 100
    
    Inequalities can be chained together so that there is one
    less-than and one greater-than inequality.  The following sorts
    of machinations are invalid:

        x <= y >= z
        foo <= bar <= baz <= qux
    '''
    def __init__(self, expression, upper=None, lower=None):
        self.expression = expression
        self.upper = upper
        self.lower = lower

    # TODO: how do we get chained inequalities working? x <= y <= z
#    def __le__(self, other):
#        print('YYY <=', other)
#        if isinstance(other, expression):
#            print('YYY foo', self.lower, self.upper)
#            
#        return NotImplemented           
#
#    def __ge__(self, other):
#        print('YYY >=', other)
#        if isinstance(other, expression):
#            print('YYY bar')
#
#        return NotImplemented           
#
#    def __eq__(self, other):
#        print('YYY ==', other)
#        if isinstance(other, expression):
#            print('YYY baz')
#
#        return NotImplemented           

