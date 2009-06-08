#ifndef PYTHON_ZIBOPT_H
#define PYTHON_ZIBOPT_H

#include <Python.h>
#include <scip/scip.h>
#include <scip/scipdefplugins.h>
#include <scip/misc.h>
#include <scip/prob.h>
#include <scip/sol.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    SCIP_VAR *variable;
    SCIP *scip;
    struct variable *next; // linked list next
} variable;

typedef struct {
    PyObject_HEAD
    SCIP_CONS *constraint;
    SCIP *scip;
    struct constraint *next; // linked list next
} constraint;

typedef struct {
    PyObject_HEAD
    SCIP *scip;
    variable   *first_var;  // linked list head
    constraint *first_cons; // linked list head
} solver;

typedef struct {
    PyObject_HEAD
    SCIP_SOL *solution;
    SCIP *scip;
    double objective; // objective value
} solution;

#endif

