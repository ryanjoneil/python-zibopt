from error import PY_SCIP_CALL
cimport error as cerror
cimport scip as cscip

def test():
    cdef cerror.SCIP_MESSAGEHDLR *message_hdlr 
    cdef cscip.SCIP *scip
    
    message_hdlr = cerror.SCIPmessageGetHandler()
    message_hdlr.messageerror = <void *> cerror.PY_SCIP_CAPTURE_ERROR
        
    # This should work
    PY_SCIP_CALL(cscip.SCIPcreate(&scip))

    # And this should raise an exception
    PY_SCIP_CALL(cscip.SCIPsolve(scip))

