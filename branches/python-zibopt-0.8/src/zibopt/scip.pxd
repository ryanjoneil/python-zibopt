from error cimport SCIP_RETCODE

cdef extern from "scip/scip.h":
    ctypedef struct SCIP_SET:
        pass

    ctypedef struct SCIP:
        SCIP_SET *set

    ctypedef struct SCIP_VAR:
        pass

    ctypedef int SCIP_VARTYPE        # Variable types allowed in SCIP
    ctypedef double SCIP_Real        # Values for decision variables, etc
    ctypedef unsigned int SCIP_Bool  # TRUE/FALSE = 1/0

    # Constants for variable types
    SCIP_VARTYPE SCIP_VARTYPE_BINARY
    SCIP_VARTYPE SCIP_VARTYPE_CONTINUOUS
    SCIP_VARTYPE SCIP_VARTYPE_IMPLINT
    SCIP_VARTYPE SCIP_VARTYPE_INTEGER

    # Constants for booleans
    SCIP_Bool TRUE
    SCIP_Bool FALSE

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
    SCIP_Real SCIPinfinity(SCIP *scip)
    SCIP_RETCODE SCIPcreateVar(SCIP *scip, SCIP_VAR **var, char *name, 
        SCIP_Real lb, SCIP_Real ub, SCIP_Real obj, SCIP_VARTYPE vartype,
        SCIP_Bool initial, SCIP_Bool removable, void *vardelorig, 
        void *vartrans, void *vardeltrans, void *varcopy, void *vardata)
    SCIP_RETCODE SCIPaddVar(SCIP *scip, SCIP_VAR *var)
    SCIP_Real SCIPvarGetObj(SCIP_VAR *var)
    SCIP_RETCODE SCIPvarChgObj(SCIP_VAR *var, void *blkmem, SCIP_SET *set,
        void *primal, void *lp, void *eventqueue, SCIP_Real coefficient)
    int SCIPvarGetBranchPriority(SCIP_VAR *var)
    SCIP_RETCODE SCIPchgVarBranchPriority(SCIP *scip, SCIP_VAR *var, int p)

cdef extern from "scip/scipdefplugins.h":
    SCIP_RETCODE SCIPincludeDefaultPlugins(SCIP *scip)

cdef class solver:
    cdef SCIP *scip
    
    # Public attributes
    cdef public set variables
    cdef public set constraints

