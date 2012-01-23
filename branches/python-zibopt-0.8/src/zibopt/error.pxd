from libc.stdio cimport FILE

cdef extern from "scip/scip.h":
    ctypedef enum SCIP_RETCODE:
        pass
    SCIP_RETCODE SCIP_OKAY

    ctypedef struct SCIP_MESSAGEHDLR:
        void *messageerror
        void *messagewarning
        void *messagedialog
        void *messageinfo
    SCIP_MESSAGEHDLR *SCIPmessageGetHandler()

