#ifndef PYTHON_ZIBOPT_ERROR_H
#define PYTHON_ZIBOPT_ERROR_H

// Function for converting SCIP errors to Python exceptions
static void PyScipSetError(PyObject *error_type, SCIP_RETCODE err_code) {
    switch(err_code) {
        case SCIP_OKAY:
            PyErr_SetString(error_type, "normal termination");
            break;
        case SCIP_ERROR:
            PyErr_SetString(error_type, "unspecified error");
            break;
        case SCIP_NOMEMORY:
            PyErr_SetString(error_type, "insufficient memory error");
            break;
        case SCIP_READERROR:
            PyErr_SetString(error_type, "file read error");
            break;
        case SCIP_WRITEERROR:
            PyErr_SetString(error_type, "file write error");
            break;
        case SCIP_NOFILE:
            PyErr_SetString(error_type, "file not found error");
            break;
        case SCIP_FILECREATEERROR:
            PyErr_SetString(error_type, "cannot create file");
            break;
        case SCIP_LPERROR:
            PyErr_SetString(error_type, "error in LP solver");
            break;
        case SCIP_NOPROBLEM:
            PyErr_SetString(error_type, "no problem exists");
            break;
        case SCIP_INVALIDCALL:
            PyErr_SetString(error_type, "method cannot be called at this time in solution process");
            break;
        case SCIP_INVALIDDATA:
            PyErr_SetString(error_type, "method cannot be called with this type of data");
            break;
        case SCIP_INVALIDRESULT:
            PyErr_SetString(error_type, "method returned an invalid result code");
            break;
        case SCIP_PLUGINNOTFOUND:
            PyErr_SetString(error_type, "a required plugin was not found");
            break;
        case SCIP_PARAMETERUNKNOWN:
            PyErr_SetString(error_type, "the parameter with the given name was not found");
            break;
        case SCIP_PARAMETERWRONGTYPE:
            PyErr_SetString(error_type, "the parameter is not of the expected type");
            break;
        case SCIP_PARAMETERWRONGVAL:
            PyErr_SetString(error_type, "the value is invalid for the given parameter");
            break;
        case SCIP_KEYALREADYEXISTING:
            PyErr_SetString(error_type, "the given key is already existing in table");
            break;
        case SCIP_MAXDEPTHLEVEL:
            PyErr_SetString(error_type, "maximal branching depth level exceeded");
            break;
        default:
            PyErr_SetString(error_type, "an unregocnized error occurred in SCIP");
    }
}

#endif
