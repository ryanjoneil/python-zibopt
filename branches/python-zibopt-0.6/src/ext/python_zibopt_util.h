#ifndef PYTHON_ZIBOPT_UTIL_H
#define PYTHON_ZIBOPT_UTIL_H

// Header file for utility functions and macros.

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
        PyObject *r = PyUnicode_FromString(self->scip->set->setting[i]->name); \
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
        if (PyUnicode_CompareWithASCIIString(attr_name, name) == 0) { \
            if (PyFloat_Check(value) || PyLong_Check(value)) { \
                if (PyFloat_Check(value) || PyLong_Check(value)) \
                    d = (double) PyLong_AsLong(value); \
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
        if (PyUnicode_CompareWithASCIIString(attr_name, name) == 0) { \
            if (PyLong_Check(value)) { \
                i = PyLong_AsLong(value); \
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
        if (PyUnicode_CompareWithASCIIString(attr_name, name) == 0) { \
            if (PyLong_Check(value)) { \
                attribute = PyLong_AsLong(value); \
                return 0; \
            } else { \
                PyErr_SetString(error, "invalid value for SCIP setting"); \
                return -1; \
            } \
        }

#define PY_SCIP_SET_PRIORITY(function, object) \
        if (PyUnicode_CompareWithASCIIString(attr_name, "priority") == 0) { \
            if (PyLong_Check(value)) { \
                function(object, self->scip->set, PyLong_AsLong(value)); \
                return 0; \
            } else { \
                PyErr_SetString(error, "invalid value for priority"); \
                return -1; \
            } \
        }

#endif

