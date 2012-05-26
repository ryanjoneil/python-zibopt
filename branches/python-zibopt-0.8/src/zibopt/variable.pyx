from error import PY_SCIP_CALL
from itertools import product
cimport scip as cscip
cimport variable as cvariable

cdef class expression:
    '''
    Instantiates an algebraic expression.  This is assumed to be a
    sum of sets of variables which are multiplied.  Parameters:

        - terms: {(tuple of variables): coefficient, ...}
        - expr_lower: lower bound
        - expr_lower: upper bound

    Represents an expression with an upper and/or lower bound.  Valid
    expressions can be constructed using any arithmetic operation and
    powers of expressions containing one variable.  Expressions cannot be
    divided by anything but a number.  The following are valid examples::

        (x + 3*y) / 4
        (3 * x**2) ** 4
        (x + y) * (x - y)

    Expressions can take upper and lower bounds.  When two expressions are
    being compared, only one inequality may be used.  Inequalities can be
    chained when the middle is an expression and the upper and lower bounds
    are constants.  Valid inequalitites look like::

        x * y <= x * z**2
        x + z >= y/2

        0 <= 3 * x <= 10
        10 >= 3 * x >= 0
    '''
    def __init__(self, terms={}, expr_lower=None, expr_upper=None):
        # Terms should be {(variable sequence): coefficient}
        self.terms = {tuple(sorted(v)):c for v, c in terms.items()}
        self.expr_lower = expr_lower
        self.expr_upper = expr_upper

    def __getitem__(self, key):
        return self.terms[key]

    def __add__(self, other):
        # No reverse operators, so we test to make sure self is an expression.
        if not isinstance(self, expression):
            self, other = other, self

        if isinstance(other, expression):
            # x + y
            terms = self.terms.copy()
            for v, c in other.terms.items():
                terms[v] = terms.get(v, 0.0) + c

            return expression(terms)

        elif isinstance(other, int) or isinstance(other, float):
            # x + 1
            terms = self.terms.copy()
            terms[()] = terms.get((), 0.0) + other
            return expression(terms)

        return NotImplemented

    def __sub__(self, other):
        # x - y
        # x - 2
        return self + (-1) * other

    def __rsub__(self, other):
        # 1 - x is the same as -x + 1
        return -1*self + other

    def __mul__(self, other):
        # No reverse operators, so we test to make sure self is an expression.
        if not isinstance(self, expression):
            self, other = other, self

        if isinstance(other, expression):
            # (x + y) * (x * y)
            # (x + y) * (v - w)
            # x * (y - z)
            terms = {}
            for v1, v2 in product(self.terms, other.terms):
                v = tuple(sorted(v1 + v2))
                c = self.terms.get(v1, 1.0) * other.terms.get(v2, 1.0)
                terms[v] = terms.get(v, 0.0) + c

            return expression(terms)

        elif isinstance(other, int) or isinstance(other, float):
            # 2 * (x + y)
            return expression({
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
        return expression({v:-c for v, c in self.terms.items()})

    def __pos__(self):
        # +(x * y)
        return self

    def __pow__(self, x, z): # TODO: what's z for?
        if isinstance(x, int) and x >= 0:
            if len(self.terms) == 1:
                # (2 * x) ** 4
                for term, c in self.terms.items():
                    # Make sure we only have one variable
                    if len(set(term)) == 1:
                        variables = term * x
                        coefficient = c ** x
                        return expression({variables:coefficient})

            elif len(self.terms) == 2 and () in self.terms:
                # (2 * x**3) ** 4
                e = expression({():1.0})
                for _ in range(x):
                    e = e * self
                return e

        return NotImplemented

    __truediv__ = __div__

    # TODO: tests for this. There are no reverse operators in cython,
    #       so we have to raise error in these cases.
    # __rdiv__ & __rtruediv__ would allow expressions like 1/x
    # Thus they are specifically NOT implemented here.

    # This part allows <=, >= and == to populate lower/upper bounds
    def __richcmp__(self, other, op):
        # TODO: error on just < or > ?
        if op == 1: # <=
            if isinstance(other, expression):
                if isinstance(self, cvariable.variable) or (
                   self.expr_lower is None and self.expr_upper is None and \
                   other.expr_lower is None and other.expr_upper is None
                ):
                    # x <= 3
                    # 2*x <= 3*y
                    self.expr_upper  = other
                    other.expr_lower = self
                    return self
    
                elif self.expr_upper is None and list(other.terms) == [()]:
                    # x <= 10
                    self.expr_upper  = other
                    other.expr_lower = self
                    return self
    
            elif isinstance(other, int) or isinstance(other, float):
                # x + y <= 1
                return self <= expression({():other})

        elif op == 5: # >=
            if isinstance(other, expression):
                if isinstance(self, cvariable.variable) or (
                   self.expr_lower is None and self.expr_upper is None and \
                   other.expr_lower is None and other.expr_upper is None
                ):
                    # x >= 3
                    # 2*x >= 3*y
                    self.expr_lower  = other
                    other.expr_upper = self
                    return self
    
                elif self.expr_lower is None and list(other.terms) == [()]:
                    # x >= 10
                    self.expr_lower  = other
                    other.expr_upper = self
                    return self
    
            elif isinstance(other, int) or isinstance(other, float):
                # x + y >= 1
                return self >= expression({():other})
    
        elif op == 2: # ==
            if isinstance(other, expression):
                if isinstance(self, cvariable.variable) or (
                   self.expr_lower is None and self.expr_upper is None and \
                   other.expr_lower is None and other.expr_upper is None
                ):
                    # x == 3
                    # 2*x == 3*y
                    self.expr_lower  = other
                    self.expr_upper  = other
                    other.expr_lower = self
                    other.expr_upper = self
                    return self
    
            elif isinstance(other, int) or isinstance(other, float):
                # x + y == 1
                return self == expression({():other})

        return NotImplemented

    def _clear_bounds(self):
        '''
        This is intended for use after an expression is turned into a
        constraint. It clears expression-type bounds off of individual
        variables, since they are not constructed in the same manner.
        '''
        # Only matters for indidividual variables
        for term in self.terms:
            if len(term) == 1 and isinstance(term[0], cvariable.variable):
                # Clear off related terms, but avoid infinite loops.
                lower = term[0].expr_lower
                upper = term[0].expr_upper
                term[0].expr_lower = None
                term[0].expr_upper = None

                if lower is not None:
                    lower._clear_bounds()
                if upper is not None:
                    upper._clear_bounds()

cdef class variable(expression):
    '''Provides a hashable Python decision variable.'''
    def __init__(
        self, 
        cscip.solver solver not None,
        cscip.SCIP_VARTYPE vartype,
        cscip.SCIP_Real coefficient,
        cscip.SCIP_Real lower,
        cscip.SCIP_Real upper, 
        int priority
    ):
        expression.__init__(self)
        self.scip    = solver.scip
        self.vartype = vartype
        self.lower   = lower
        self.upper   = upper

        # Add self to the terms of the base expression
        self.terms[(self,)] = 1.0

        # Create the variable
        PY_SCIP_CALL(cscip.SCIPcreateVar(self.scip, &(self.var), NULL, 
            lower, upper, coefficient, vartype, cscip.TRUE, cscip.FALSE,
            NULL, NULL, NULL, NULL, NULL))

        # Inform the solver the variable exists
        PY_SCIP_CALL(cscip.SCIPaddVar(self.scip, self.var))

        if priority != 0:
            PY_SCIP_CALL(
                cscip.SCIPchgVarBranchPriority(self.scip, self.var, priority))

    def __hash__(self):
        return hash(id(self))

    def __pow__(self, x, z): # TODO: what's z for?
        if isinstance(x, int) and x >= 0:
            if x == 0:
                return expression({():1.0})
            else:
                return expression({(self,)*x:1.0})

        return NotImplementedError

    def __richcmp__(self, other, op):
        # Couldn't get inheritance working here. Would rather just default
        # to the __richcmp__ implementation on expression, but variable
        # can't see it and I can't figure out how to expose it.
        if op == 0:   # <
            return expression.__lt__(self, other)
        elif op == 1: # <= 
            return expression.__le__(self, other)
        elif op == 2: # == 
            return expression.__eq__(self, other)
        elif op == 3: # != 
            return expression.__ne__(self, other)
        elif op == 4: # > 
            return expression.__gt__(self, other)
        elif op == 5: # >= 
            return expression.__ge__(self, other)

        return NotImplementedError

    property priority:
        # Branching priority for a decision variable
        def __get__(self):
            return cscip.SCIPvarGetBranchPriority(self.var)
        
        def __set__(self, int p):
            PY_SCIP_CALL(
                cscip.SCIPchgVarBranchPriority(self.scip, self.var, p))
