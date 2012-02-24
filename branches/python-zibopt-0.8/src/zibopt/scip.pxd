from error cimport SCIP_RETCODE

cdef extern from "scip/scip.h":
    ctypedef struct SCIP:
        pass

    # Variable types allowed in SCIP
    enum SCIP_VARTYPE:
        pass

    SCIP_VARTYPE SCIP_VARTYPE_BINARY
    SCIP_VARTYPE SCIP_VARTYPE_CONTINUOUS
    SCIP_VARTYPE SCIP_VARTYPE_IMPLINT
    SCIP_VARTYPE SCIP_VARTYPE_INTEGER

    # I don't want to have to create Cython structs for everything we don't 
    # use, thus all the (void *).  It's tacky, I know.  As we use these,
    # they will get pulled over into the Cython side.

    SCIP_RETCODE SCIPcreate(SCIP **scip)
    SCIP_RETCODE SCIPcreateProb(SCIP *scip, char *name, void *probdelorig, 
        void *probtrans, void *probdeltrans, void *probinitsol, 
        void *probexitsol, void *probcopy, void *probdata)
    SCIP_RETCODE SCIPsolve(SCIP *scip)

cdef extern from "scip/scipdefplugins.h":
    SCIP_RETCODE SCIPincludeDefaultPlugins(SCIP *scip)

