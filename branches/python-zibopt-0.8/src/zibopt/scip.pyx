cimport czibopt

SCIP_ERROR_STR = ''

cdef void PY_SCIP_CAPTURE_ERROR(void *a, void *b, char *c):
    global SCIP_ERROR_STR
    SCIP_ERROR_STR += c   

def PY_SCIP_CALL(czibopt.SCIP_RETCODE retcode):
    cdef czibopt.SCIP_MESSAGEHDLR *message_hdlr 
    global SCIP_ERROR_STR
    if retcode != czibopt.SCIP_OKAY:
        error = SCIP_ERROR_STR
        SCIP_ERROR_STR = ''
        raise Exception(error)

def test():
    cdef czibopt.SCIP_MESSAGEHDLR *message_hdlr 
    cdef czibopt.SCIP *scip
    
    message_hdlr = czibopt.SCIPmessageGetHandler()
    message_hdlr.messageerror = <void *> PY_SCIP_CAPTURE_ERROR
        
    # This should work
    PY_SCIP_CALL(czibopt.SCIPcreate(&scip))

    # And this should raise an exception
    PY_SCIP_CALL(czibopt.SCIPsolve(scip))

