cimport error

class SCIPException(Exception):
    pass

SCIP_ERROR_STR = ''

cdef void PY_SCIP_CAPTURE_ERROR(void *a, void *b, char *c):
    global SCIP_ERROR_STR
    SCIP_ERROR_STR += c   

def PY_SCIP_CALL(error.SCIP_RETCODE retcode):
    cdef error.SCIP_MESSAGEHDLR *message_hdlr 
    global SCIP_ERROR_STR
    if retcode != error.SCIP_OKAY:
        err = SCIP_ERROR_STR
        SCIP_ERROR_STR = ''
        raise SCIPException(err)

