#include "python_zibopt.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int branching_rule_init(branching_rule *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object
    char *name;    // name of branching rule
    SCIP_BRANCHRULE* r;
    
    if (!PyArg_ParseTuple(args, "Os", &s, &name))
        return -1;
    
    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Load the branching rule from SCIP
    r = SCIPfindBranchrule(self->scip, name);
    if (r == NULL) {
        PyErr_SetString(error, "unrecognized branching rule");
        return -1;
    }

    return 0;
}

static void branching_rule_dealloc(solution *self) {
    self->ob_type->tp_free((PyObject *) self);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMemberDef branching_rule_members[] = {
    {NULL} /* Sentinel */
};

static PyMethodDef branching_rule_methods[] = {
//    {"load", (PyCFunction) branching_rule_load, METH_STATIC, "get all branching rules in a dict"},
    {NULL} /* Sentinel */
};

static PyTypeObject branching_rule_type = {
    PyObject_HEAD_INIT(NULL)
    0,                             /* ob_size */
    "_branch.branching_rule",      /* tp_name */
    sizeof(branching_rule),        /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor) branching_rule_dealloc, /* tp_dealloc */
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
    "SCIP branching rules",        /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    branching_rule_methods,        /* tp_methods */
    branching_rule_members,        /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    (initproc) branching_rule_init,/* tp_init */
    0,                             /* tp_alloc */
    0 ,                            /* tp_new */
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC init_branch(void) {
    PyObject* m;

    branching_rule_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(& branching_rule_type) < 0)
        return;

    m = Py_InitModule3("_branch", branching_rule_methods, "SCIP Branching Rule");

    Py_INCREF(& branching_rule_type);
    PyModule_AddObject(m, "branching_rule", (PyObject *) &branching_rule_type);
    
    // Initialize exception type
    error = PyErr_NewException("_branch.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   
}

