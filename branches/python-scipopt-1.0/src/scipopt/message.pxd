cdef extern from "scip/scip.h":
    ctypedef struct SCIP_MESSAGEHDLR:
        pass # TODO
    
    ctypedef struct SCIP_MESSAGEHDLRDATA:
        pass # TODO

    ctypedef enum SCIP_VERBLEVEL:
        SCIP_VERBLEVEL_NONE
        SCIP_VERBLEVEL_DIALOG
        SCIP_VERBLEVEL_MINIMAL
        SCIP_VERBLEVEL_NORMAL
        SCIP_VERBLEVEL_HIGH
        SCIP_VERBLEVEL_FULL
