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
    self->branch = r;

    return 0;
}

static void branching_rule_dealloc(branching_rule *self) {
    ((PyObject *) self)->ob_type->tp_free(self);
}

static PyObject* branching_rule_getattr(branching_rule *self, PyObject *attr_name) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        if (PyUnicode_CompareWithASCIIString(attr_name, "maxbounddist") == 0)
            return Py_BuildValue("d", SCIPbranchruleGetMaxbounddist(self->branch));
        if (PyUnicode_CompareWithASCIIString(attr_name, "maxdepth") == 0)
            return Py_BuildValue("i", SCIPbranchruleGetMaxdepth(self->branch));
        if (PyUnicode_CompareWithASCIIString(attr_name, "priority") == 0)
            return Py_BuildValue("i", SCIPbranchruleGetPriority(self->branch));
    }
    return PyObject_GenericGetAttr((PyObject *) self, attr_name);
}

static int branching_rule_setattr(branching_rule *self, PyObject *attr_name, PyObject *value) {
    double d;
    int i;
    
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        PY_SCIP_SET_DBL_MIN("maxbounddist", self->branch->maxbounddist, -1); 
        PY_SCIP_SET_INT_MIN("maxdepth", self->branch->maxdepth, -1); 
        PY_SCIP_SET_PRIORITY(SCIPbranchruleSetPriority, self->branch);
    }
    return PyObject_GenericSetAttr((PyObject *) self, attr_name, value);
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
    {NULL} /* Sentinel */
};

static PyTypeObject branching_rule_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
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
    (getattrofunc) branching_rule_getattr, /* tp_getattro */
    (setattrofunc) branching_rule_setattr, /* tp_setattro */
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

static PyModuleDef branch_module = {
    PyModuleDef_HEAD_INIT,
    "_branch",
    "SCIP Branching Rule",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit__branch(void) {
    PyObject* m;

    branching_rule_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(& branching_rule_type) < 0)
        return NULL;

    m = PyModule_Create(&branch_module); 

    Py_INCREF(& branching_rule_type);
    PyModule_AddObject(m, "branching_rule", (PyObject *) &branching_rule_type);
    
    // Initialize exception type
    error = PyErr_NewException("_branch.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   

    return m;
}

