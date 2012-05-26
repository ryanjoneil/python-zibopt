cimport scip as cscip

cdef class expression:
    cdef public terms
    cdef public expr_lower
    cdef public expr_upper

cdef class variable(expression):
    cdef cscip.SCIP *scip
    cdef cscip.SCIP_VAR *var

    cdef readonly cscip.SCIP_VARTYPE vartype
    cdef readonly cscip.SCIP_Real lower
    cdef readonly cscip.SCIP_Real upper
