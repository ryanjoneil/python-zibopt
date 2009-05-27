#ifndef PYTHON_ZIBOPT_H
#define PYTHON_ZIBOPT_H

#include <Python.h>
#include <scip/scip.h>
#include <scip/scipdefplugins.h>
#include <scip/misc.h>

typedef struct {
    PyObject_HEAD
    SCIP *scip;
} solver;

typedef struct {
    PyObject_HEAD
    SCIP_VAR *variable;
} variable;

#endif

