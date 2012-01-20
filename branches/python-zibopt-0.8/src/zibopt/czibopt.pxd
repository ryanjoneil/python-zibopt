cdef extern from "scip/scip.h":
    ctypedef enum SCIP_RETCODE:
        pass
    SCIP_RETCODE SCIP_OKAY

    ctypedef struct SCIP:
        pass

    int SCIPcreate(SCIP **scip)
    int SCIPsolve(SCIP *scip)


