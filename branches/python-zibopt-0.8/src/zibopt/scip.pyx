from error import PY_SCIP_CALL, quiet_solver
cimport scip as cscip

# Variable types
BINARY     = cscip.SCIP_VARTYPE_BINARY
CONTINUOUS = cscip.SCIP_VARTYPE_CONTINUOUS
IMPLINT    = cscip.SCIP_VARTYPE_IMPLINT
INTEGER    = cscip.SCIP_VARTYPE_INTEGER

cdef class solver:
    cdef cscip.SCIP *scip
    
    # Public attributes
    cdef public set variables
    cdef public set constraints
    
    # TODO: deallocation of solver, variables, etc?
    
    def __init__(self, quiet=True):
        '''
        TODO: docs
        '''
        if quiet:
            quiet_solver()

        # Create and prepare solver
        PY_SCIP_CALL(cscip.SCIPcreate(&(self.scip)))
        PY_SCIP_CALL(cscip.SCIPincludeDefaultPlugins(self.scip))
        PY_SCIP_CALL(SCIPcreateProb(self.scip, "python-zibobt", NULL, NULL, 
            NULL, NULL, NULL, NULL, NULL))

        # TODO: (?) Keep SCIP from catching keyboard interrupts.  These go 
        #           to python.
        #self->scip->set->misc_catchctrlc = FALSE

        # Initialize variable and constraint sets
        self.variables = set()
        self.constraints = set()

    def solve(self):
        PY_SCIP_CALL(cscip.SCIPsolve(self.scip))

    def variable(self, foo):
        # TODO: something!
        pass

