cdef extern from "scip/scip.h":
    ctypedef struct SCIP_MESSAGEHDLR:
        void *messageerror
    SCIP_MESSAGEHDLR *SCIPmessageGetHandler()
    
    ctypedef enum SCIP_RETCODE:
        pass
    SCIP_RETCODE SCIP_OKAY

cdef void PY_SCIP_CAPTURE_ERROR(void *a, void *b, char *c)

