cimport scip as cscip

cdef class expression:
    cdef public terms
    cdef public expr_lower
    cdef public expr_upper

cdef class variable(expression):
    cdef cscip.SCIP *scip
    cdef cscip.SCIP_VARTYPE vartype
    cdef cscip.SCIP_VAR *var

