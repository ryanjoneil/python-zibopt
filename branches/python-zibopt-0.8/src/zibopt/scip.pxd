from error cimport SCIP_RETCODE

cdef extern from "scip/scip.h":
    ctypedef struct SCIP:
        pass

    ctypedef struct SCIP_VAR:
        pass

    ctypedef int SCIP_VARTYPE        # Variable types allowed in SCIP
    ctypedef double SCIP_REAL        # Values for decision variables, etc
    ctypedef unsigned int SCIP_BOOL  # TRUE/FALSE = 1/0

    SCIP_VARTYPE SCIP_VARTYPE_BINARY
    SCIP_VARTYPE SCIP_VARTYPE_CONTINUOUS
    SCIP_VARTYPE SCIP_VARTYPE_IMPLINT
    SCIP_VARTYPE SCIP_VARTYPE_INTEGER

    # I don't want to have to create Cython structs for everything we don't 
    # use, thus all the (void *).  It's tacky, I know.  As we use these,
    # they will get pulled over into the Cython side.

    # Functions associated with 
    SCIP_RETCODE SCIPcreate(SCIP **scip)
    SCIP_RETCODE SCIPcreateProb(SCIP *scip, char *name, void *probdelorig, 
        void *probtrans, void *probdeltrans, void *probinitsol, 
        void *probexitsol, void *probcopy, void *probdata)
    SCIP_RETCODE SCIPsolve(SCIP *scip)

    # Functions dealing with SCIP decision variables
    SCIP_RETCODE SCIPcreateVar(SCIP *scip, SCIP_VAR **var, char *name, 
        SCIP_REAL lb, SCIP_REAL ub, SCIP_REAL obj, SCIP_VARTYPE vartype,
        SCIP_BOOL initial, SCIP_BOOL removable, void *vardelorig, 
        void *vartrans, void *vardeltrans, void *varcopy, void *vardata)

cdef extern from "scip/scipdefplugins.h":
    SCIP_RETCODE SCIPincludeDefaultPlugins(SCIP *scip)

cdef class solver:
    cdef SCIP *scip
    
    # Public attributes
    cdef public set variables
    cdef public set constraints

