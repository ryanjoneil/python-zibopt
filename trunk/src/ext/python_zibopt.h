#ifndef PYTHON_ZIBOPT_H
#define PYTHON_ZIBOPT_H

#include <Python.h>
#include <scip/scip.h>
#include <scip/scipdefplugins.h>
#include <scip/misc.h>
#include <scip/prob.h>
#include <scip/sol.h>

typedef struct {
    PyObject_HEAD
    SCIP_VAR *variable;
    SCIP *scip;
    char *name;
    struct variable *next; // linked list next
} variable;

typedef struct {
    PyObject_HEAD
    SCIP *scip;
    variable *first; // linked list head
} solver;

typedef struct {
    PyObject_HEAD
    SCIP_SOL *solution;
    SCIP *scip;
} solution;

#endif

