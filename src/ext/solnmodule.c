#include "python_zibopt.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int solution_init(solution *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object

    if (!PyArg_ParseTuple(args, "O", &s))
        return -1;
    
    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Detect infeasibility
    self->solution = SCIPgetBestSol(self->scip);
    
    self->optimal    = self->scip->stat->status == SCIP_STATUS_OPTIMAL;
    self->infeasible = self->scip->stat->status == SCIP_STATUS_INFEASIBLE;
    self->unbounded  = self->scip->stat->status == SCIP_STATUS_UNBOUNDED;
    self->inforunbd  = self->scip->stat->status == SCIP_STATUS_INFORUNBD;

    // Extract objective value into Python float
    self->objective = SCIPgetSolOrigObj(self->scip, self->solution);
    
    return 0;
}

static void solution_dealloc(solution *self) {
    self->ob_type->tp_free((PyObject *) self);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/
static PyObject *solution_value(solution *self, PyObject *v) {
    variable *var;

    // Check and make sure we have a real variable type
    if (strcmp(v->ob_type->tp_name, VARIABLE_TYPE_NAME)) {
        PyErr_SetString(error, "invalid variable type");
        return NULL;
    }
    var = (variable *) v;
    
    // Verify that the variable is associated with this solver
    if (var->scip != self->scip) {
        PyErr_SetString(error, "variable not associated with solver");
        return NULL;
    }    
    
    return Py_BuildValue("d", SCIPgetSolVal(self->scip, self->solution, var->variable));
}

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMemberDef solution_members[] = {
    {"objective", T_DOUBLE, offsetof(solution, objective), 0, "objective value"},
    {"optimal", T_BOOL, offsetof(solution, optimal), 0, "solution is optimal"},
    {"infeasible", T_BOOL, offsetof(solution, infeasible), 0, "solution is infeasible"},
    {"unbounded", T_BOOL, offsetof(solution, unbounded), 0, "solution is unbounded"},
    {"inforunbd", T_BOOL, offsetof(solution, inforunbd), 0, "solution is infeasible or unbounded"},
    {NULL} /* Sentinel */
};

static PyMethodDef solution_methods[] = {
    {"value", (PyCFunction) solution_value, METH_O, "get variable value in a solution"},
    {NULL} /* Sentinel */
};

static PyTypeObject solution_type = {
    PyObject_HEAD_INIT(NULL)
    0,                             /* ob_size */
    "_soln.solution",              /* tp_name */
    sizeof(solution),              /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor) solution_dealloc, /* tp_dealloc */
    0,                             /* tp_print */
    0,                             /* tp_getattr */
    0,                             /* tp_setattr */
    0,                             /* tp_compare */
    0,                             /* tp_repr */
    0,                             /* tp_as_number */
    0,                             /* tp_as_sequence */
    0,                             /* tp_as_mapping */
    0,                             /* tp_hash */
    0,                             /* tp_call */
    0,                             /* tp_str */
    0,                             /* tp_getattro */
    0,                             /* tp_setattro */
    0,                             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP solution objects",       /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    solution_methods,              /* tp_methods */
    solution_members,              /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    (initproc) solution_init,      /* tp_init */
    0,                             /* tp_alloc */
    0 ,                            /* tp_new */
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC init_soln(void) {
    PyObject* m;

    solution_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&solution_type) < 0)
        return;

    m = Py_InitModule3("_soln", solution_methods, "SCIP Solution");

    Py_INCREF(&solution_type);
    PyModule_AddObject(m, "solution", (PyObject *) &solution_type);
    
    // Initialize exception type
    error = PyErr_NewException("_soln.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   
}

