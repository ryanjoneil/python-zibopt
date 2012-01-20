cdef extern from "scip/scip.h":
    ctypedef struct SCIP_MESSAGEHDLR:
        void *messageerror
    SCIP_MESSAGEHDLR *SCIPmessageGetHandler()
    void SCIPmessageSetDefaultHandler()
    
    ctypedef enum SCIP_RETCODE:
        pass
    SCIP_RETCODE SCIP_OKAY

    ctypedef struct SCIP:
        pass

    int SCIPcreate(SCIP **scip)
    int SCIPsolve(SCIP *scip)

