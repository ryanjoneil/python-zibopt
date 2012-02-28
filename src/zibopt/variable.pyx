cimport scip as cscip
import scip as pscip

cdef class variable:
    cdef cscip.SCIP *scip
    cdef cscip.SCIP_VARTYPE vartype

    def __cinit__(
        self, 
        cscip.solver solver not None,
        cscip.SCIP_VARTYPE vartype
        
    ):
        self.scip    = solver.scip
        self.vartype = vartype

