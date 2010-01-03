#ifndef PYTHON_ZIBOPT_H
#define PYTHON_ZIBOPT_H

#include <Python.h>
#include <stdbool.h>
#include <string.h>

#include <scip/clock.h>
#include <scip/scip.h>
#include <scip/scipdefplugins.h>
#include <scip/misc.h>
#include <scip/prob.h>
#include <scip/sol.h>
#include <scip/struct_branch.h>
#include <scip/struct_conflict.h>
#include <scip/struct_heur.h>
#include <scip/struct_nodesel.h>
#include <scip/struct_presol.h>
#include <scip/struct_prop.h>
#include <scip/struct_sepa.h>
#include <scip/struct_stat.h>

#include "structmember.h"
#include "python_zibopt_util.h"

#define SOLVER_TYPE_NAME "solver"
#define VARIABLE_TYPE_NAME "variable"

// These are from set.c in SCIP code
#define SCIP_DEFAULT_LIMIT_TIME 1e+20 /**< maximal time in seconds to run */
#define SCIP_DEFAULT_LIMIT_GAP    0.0 /**< solving stops, if the gap is below the given value */
#define SCIP_DEFAULT_LIMIT_ABSGAP 0.0 /**< solving stops, if the absolute difference between primal and dual
                                       *   bound reaches this value */

typedef struct {
    PyObject_HEAD
    SCIP_VAR *variable;
    SCIP *scip;
    double upper;          // upper bound
    double lower;          // lower bound
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
    variable   *first_var;   // linked list head
    constraint *first_cons;  // linked list head
} solver;

typedef struct {
    PyObject_HEAD
    SCIP_SOL *solution;
    SCIP *scip;
    double objective; // objective value
    bool optimal;     // solution status flags
    bool infeasible;
    bool unbounded;
    bool inforunbd;
} solution;

#define PY_SCIP_SETTINGS_TYPE(setting_type, setting_field, struct_name) \
typedef struct { \
    PyObject_HEAD \
    setting_type *setting_field; \
    SCIP *scip; \
} struct_name;
  
PY_SCIP_SETTINGS_TYPE(SCIP_BRANCHRULE, branch, branching_rule);
PY_SCIP_SETTINGS_TYPE(SCIP_CONFLICTHDLR, conflict, conflict);
PY_SCIP_SETTINGS_TYPE(SCIP_HEUR, heur, heuristic);
PY_SCIP_SETTINGS_TYPE(SCIP_PRESOL, presol, presolver);
PY_SCIP_SETTINGS_TYPE(SCIP_PROP, prop, propagator);
PY_SCIP_SETTINGS_TYPE(SCIP_NODESEL, nodesel, selector);
PY_SCIP_SETTINGS_TYPE(SCIP_SEPA, sepa, separator);

#endif

