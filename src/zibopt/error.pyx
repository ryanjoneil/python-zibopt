from libc.stdio cimport FILE
cimport error

class SCIPException(Exception):
    pass

SCIP_ERROR_STR = ''

cdef void PY_SCIP_CAPTURE_ERROR(
        SCIP_MESSAGEHDLR *messagehdlr, 
        FILE *file, 
        char *msg):
    global SCIP_ERROR_STR
    SCIP_ERROR_STR += msg

def PY_SCIP_CALL(error.SCIP_RETCODE retcode):
    cdef error.SCIP_MESSAGEHDLR *message_hdlr 
    global SCIP_ERROR_STR
    if retcode != error.SCIP_OKAY:
        err = SCIP_ERROR_STR
        SCIP_ERROR_STR = ''
        raise SCIPException(err)

# Install python-zibopt's error handler into SCIP
cdef error.SCIP_MESSAGEHDLR *message_hdlr 
message_hdlr = error.SCIPmessageGetHandler()
message_hdlr.messageerror = <void *> PY_SCIP_CAPTURE_ERROR

cdef void PY_SCIP_IGNORE_MESSAGE(
        SCIP_MESSAGEHDLR *messagehdlr, 
        FILE *file, 
        char *msg):
    pass

def quiet_solver():
    # TODO: there is a bug here -- if we quiet the solver, then we can't 
    #       turn it back on later in another instance.  Add a test case 
    #       and fix.
    message_hdlr.messagewarning = <void *> PY_SCIP_IGNORE_MESSAGE
    message_hdlr.messagedialog = <void *> PY_SCIP_IGNORE_MESSAGE
    message_hdlr.messageinfo = <void *> PY_SCIP_IGNORE_MESSAGE
