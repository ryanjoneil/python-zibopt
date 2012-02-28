cimport expression
cimport scip as cscip

cdef class variable(expression.expression):
    '''Provides a hashable and orderable Python decision variable.'''
    #def __init__(self, *args, **kwds):
    #    cexpression.expression.__init__(self, {(self,):1.0})
    def __cinit__(
        self, 
        cscip.solver solver not None,
        cscip.SCIP_VARTYPE vartype
        
    ):
        self.scip    = solver.scip
        self.vartype = vartype

    def __hash__(self):
        return hash(id(self))

    def __pow__(self, x, z): # TODO: what's z for?
        if isinstance(x, int) and x >= 0:
            if x == 0:
                return expression.expression({():1.0})
            else:
                return expression.expression({(self,)*x:1.0})

        return NotImplementedError

    # These exist for sorting variables and have nothing to do with <=, etc.
    # Order doesn't matter so long as it's consistent, so we use id(...).
    def __richcmp__(self, other, op):
        # TODO: error on just < or > ?
        if op == 1: # <=
            return id(self) < id(other)

        elif op == 5: # >=
            return id(self) > id(other)

