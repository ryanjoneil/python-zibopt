cimport expression
cimport scip as cscip

cdef class variable(expression.expression):
    cdef cscip.SCIP *scip
    cdef cscip.SCIP_VARTYPE vartype

