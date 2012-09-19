cimport scip as cscip

class SCIPException(Exception):
    pass

#SCIP_ERROR_STR = ''

#cdef void PY_SCIP_CAPTURE_ERROR(
#        SCIP_MESSAGEHDLR *messagehdlr, 
#        FILE *file, 
#        char *msg):
#    global SCIP_ERROR_STR
#    SCIP_ERROR_STR += msg

def PY_SCIP_CALL(cscip.SCIP_RETCODE retcode):
    #cdef error.SCIP_MESSAGEHDLR *message_hdlr 
    #global SCIP_ERROR_STR
    if retcode != cscip.SCIP_OKAY:
        #err = SCIP_ERROR_STR
        #SCIP_ERROR_STR = ''
        raise SCIPException('error!: ' + str(retcode))
