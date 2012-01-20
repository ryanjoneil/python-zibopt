cimport czibopt

def PY_SCIP_CALL(czibopt.SCIP_RETCODE retcode):
    if retcode != czibopt.SCIP_OKAY:
        # TODO: better-ify this!
        raise Exception('Error <%d> in SCIP' % retcode)

def test():
    cdef czibopt.SCIP *scip
    # This should work
    PY_SCIP_CALL(czibopt.SCIPcreate(&scip))
    
    # And this should raise an exception
    PY_SCIP_CALL(czibopt.SCIPsolve(scip))

