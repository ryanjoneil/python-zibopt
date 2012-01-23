cdef extern from "scip/scip.h":
    ctypedef struct SCIP:
        pass

    int SCIPcreate(SCIP **scip)
    int SCIPsolve(SCIP *scip)

