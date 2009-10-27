#ifndef PYTHON_ZIBOPT_UTIL_H
#define PYTHON_ZIBOPT_UTIL_H

// Header file for utility functions and macros: error handling, etc.

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
        case SCIP_PARSEERROR:
            PyErr_SetString(error_type, "invalid input given to the parser");
            break;
        case SCIP_MAXDEPTHLEVEL:
            PyErr_SetString(error_type, "maximal branching depth level exceeded");
            break;
        default:
            PyErr_SetString(error_type, "an unregocnized error occurred in SCIP");
    }
}

#define PY_SCIP_CALL(error_type, fail_code, code) \
    do { \
        SCIP_RETCODE _restat_; \
        if ((_restat_ = (code)) != SCIP_OKAY) { \
            PyScipSetError(error_type, _restat_); \
            return fail_code; \
        } \
    } while (FALSE);


// SCIP solver: utility to load setting names
#define PY_SCIP_SETTING_NAMES(function_name, setting_count, setting) \
static PyObject *function_name(solver *self) { \
    int i; \
    PyObject *rules = PyList_New(self->scip->set->setting_count); \
    if (!rules) { \
        PyErr_SetString(error, "ran out of memory"); \
        return NULL; \
    } \
    for (i = 0; i < self->scip->set->setting_count; i++) { \
        PyObject *r = PyString_FromString(self->scip->set->setting[i]->name); \
        if (!r) { \
            Py_DECREF(rules); \
            return NULL; \
        } \
        PyList_SET_ITEM(rules, i, r); \
    } \
    return rules; \
}

// SCIP settings modules: generic attribute setting functions
#define PY_SCIP_SET_DBL_MIN(name, attribute, minimum) \
        if (!strcmp(attr, name)) { \
            if (PyFloat_Check(value) || PyInt_Check(value)) { \
                if (PyFloat_Check(value) || PyInt_Check(value)) \
                    d = (double) PyInt_AsLong(value); \
                else \
                    d = PyFloat_AsDouble(value); \
                if (d < minimum) { \
                    PyErr_SetString(error, "SCIP setting value too low"); \
                    return -1; \
                } \
                attribute = d; \
                return 0; \
            } else { \
                PyErr_SetString(error, "invalid value for SCIP setting"); \
                return -1; \
            } \
        }

#define PY_SCIP_SET_INT_MIN(name, attribute, minimum) \
        if (!strcmp(attr, name)) { \
            if (PyInt_Check(value)) { \
                i = PyInt_AsLong(value); \
                if (i < minimum) { \
                    PyErr_SetString(error, "SCIP setting value too low"); \
                    return -1; \
                } \
                attribute = i; \
                return 0; \
            } else { \
                PyErr_SetString(error, "invalid value for SCIP setting"); \
                return -1; \
            } \
        }

#define PY_SCIP_SET_INT(name, attribute) \
        if (!strcmp(attr, name)) { \
            if (PyInt_Check(value)) { \
                attribute = PyInt_AsLong(value); \
                return 0; \
            } else { \
                PyErr_SetString(error, "invalid value for SCIP setting"); \
                return -1; \
            } \
        }

#define PY_SCIP_SET_PRIORITY(function, object) \
        if (!strcmp(attr, "priority")) { \
            if (PyInt_Check(value)) { \
                function(object, self->scip->set, PyInt_AsLong(value)); \
                return 0; \
            } else { \
                PyErr_SetString(error, "invalid value for priority"); \
                return -1; \
            } \
        }

#endif

