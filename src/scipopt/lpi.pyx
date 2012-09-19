cimport lpi as clpi

cdef class lpi:
    def __init__(self, name=''):
        # TODO: error checking! PY_SCIP_CALL
        # TODO: message hdlr
        # TODO: obj sense
        print type(clpi.SCIP_OBJSEN_MAXIMIZE)
        clpi.SCIPlpiCreate(&(self.lpi), NULL, name, clpi.SCIP_OBJSEN_MAXIMIZE)
