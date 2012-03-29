#ifndef PYTHON_ZIBOPT_H
#define PYTHON_ZIBOPT_H

#include <Python.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <structmember.h>

#include <blockmemshell/memory.h>

#include <scip/branch.h>
#include <scip/clock.h>
#include <scip/conflict.h>
#include <scip/cons.h>
#include <scip/cons_linear.h>
#include <scip/cons_quadratic.h>
#include <scip/heur.h>
#include <scip/misc.h>
#include <scip/nodesel.h>
#include <scip/presol.h>
#include <scip/prob.h>
#include <scip/prop.h>
#include <scip/sepa.h>
#include <scip/scip.h>
#include <scip/scipdefplugins.h>
#include <scip/sol.h>
#include <scip/var.h>

#include <scip/struct_branch.h>
#include <scip/struct_conflict.h>
#include <scip/struct_disp.h>
#include <scip/struct_heur.h>
#include <scip/struct_mem.h>
#include <scip/struct_nodesel.h>
#include <scip/struct_presol.h>
#include <scip/struct_prop.h>
#include <scip/struct_sepa.h>
#include <scip/struct_stat.h>

// This is what enables us to support both Python 2 and
// Python 3.  It's sort of ugly.
#if PY_MAJOR_VERSION < 3
#define PyLong_Check(A) PyInt_Check(A)
#define PyUnicode_Check(A) PyString_Check(A)
#define PyUnicode_CompareWithASCIIString(A, B) strcmp(PyString_AS_STRING(A), B)

#define PyInit__branch init_branch
#define PyInit__conflict init_conflict
#define PyInit__cons init_cons
#define PyInit__disp init_disp
#define PyInit__heur init_heur
#define PyInit__lp init_lp
#define PyInit__nodesel init_nodesel
#define PyInit__presol init_presol
#define PyInit__prop init_prop
#define PyInit__soln init_soln
#define PyInit__scip init_scip
#define PyInit__sepa init_sepa
#define PyInit__vars init_vars
#endif

// Note that the above macros must apply to the following:
#include "python_zibopt_util.h"

#define CONSTRAINT_TYPE_NAME "constraint"
#define SOLVER_TYPE_NAME "solver"
#define VARIABLE_TYPE_NAME "variable"

// These are from set.c in SCIP code
#define SCIP_DEFAULT_LIMIT_TIME 1e+20 /**< maximal time in seconds to run */
#define SCIP_DEFAULT_LIMIT_GAP    0.0 /**< solving stops, if the gap is below the given value */
#define SCIP_DEFAULT_LIMIT_ABSGAP 0.0 /**< solving stops, if the absolute difference between primal and dual
                                       *   bound reaches this value */
#define SCIP_DEFAULT_LIMIT_SOLUTIONS -1 /** solving stops after this number of solutions */

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
    SCIP_VAR **linear_vars;  // linear terms
    SCIP_Real *linear_coef;  // linear coefficients
    int linear_nvars;        // number of linear terms
    SCIP_VAR **bilin_var1;   // first bilinear terms
    SCIP_VAR **bilin_var2;   // second bilinear terms
    SCIP_Real *bilin_coef;   // bilinear coefficients
    int bilin_nvars;         // number of bilinear terms
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

typedef struct {
    PyObject_HEAD
    SCIP_LPI *lpi;
} lp;

#define PY_SCIP_SETTINGS_TYPE(setting_type, setting_field, struct_name) \
typedef struct { \
    PyObject_HEAD \
    setting_type *setting_field; \
    SCIP *scip; \
} struct_name;
  
PY_SCIP_SETTINGS_TYPE(SCIP_BRANCHRULE, branch, branching_rule);
PY_SCIP_SETTINGS_TYPE(SCIP_CONFLICTHDLR, conflict, conflict);
PY_SCIP_SETTINGS_TYPE(SCIP_DISP, display, display_column);
PY_SCIP_SETTINGS_TYPE(SCIP_HEUR, heur, heuristic);
PY_SCIP_SETTINGS_TYPE(SCIP_PRESOL, presol, presolver);
PY_SCIP_SETTINGS_TYPE(SCIP_PROP, prop, propagator);
PY_SCIP_SETTINGS_TYPE(SCIP_NODESEL, nodesel, selector);
PY_SCIP_SETTINGS_TYPE(SCIP_SEPA, sepa, separator);

#endif

