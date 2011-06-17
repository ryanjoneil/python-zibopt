#include "python_zibopt.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int conflict_init(conflict *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object
    char *name;    // name of conflict handler
    SCIP_CONFLICTHDLR *r;
    
    if (!PyArg_ParseTuple(args, "Os", &s, &name))
        return -1;
    
    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Load the conflict handler from SCIP
    r = SCIPfindConflicthdlr(self->scip, name);
    if (r == NULL) {
        PyErr_SetString(error, "unrecognized conflict handler");
        return -1;
    }
    self->conflict = r;

    return 0;
}

static void conflict_dealloc(conflict *self) {
    ((PyObject *) self)->ob_type->tp_free(self);
}

static PyObject* conflict_getattr(conflict *self, PyObject *attr_name) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        if (PyUnicode_CompareWithASCIIString(attr_name, "priority")  == 0)
            return Py_BuildValue("i", SCIPconflicthdlrGetPriority(self->conflict));
    }
    return PyObject_GenericGetAttr((PyObject *) self, attr_name);
}

static int conflict_setattr(conflict *self, PyObject *attr_name, PyObject *value) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        PY_SCIP_SET_PRIORITY(SCIPconflicthdlrSetPriority, self->conflict);
    }
    return PyObject_GenericSetAttr((PyObject *) self, attr_name, value);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMemberDef conflict_members[] = {
    {NULL} /* Sentinel */
};

static PyMethodDef conflict_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject conflict_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_conflict.conflict",             /* tp_name */
    sizeof(conflict),             /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor) conflict_dealloc, /* tp_dealloc */
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
    (getattrofunc) conflict_getattr, /* tp_getattro */
    (setattrofunc) conflict_setattr, /* tp_setattro */
    0,                             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP conflicts",             /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    conflict_methods,             /* tp_methods */
    conflict_members,             /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    (initproc) conflict_init,     /* tp_init */
    0,                             /* tp_alloc */
    0 ,                            /* tp_new */
};

static PyModuleDef conflict_module = {
    PyModuleDef_HEAD_INIT,
    "_conflict",
    "SCIP Conflict Handler",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit__conflict(void) {
    PyObject* m;

    conflict_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(& conflict_type) < 0)
        return NULL;

    m = PyModule_Create(&conflict_module); 

    Py_INCREF(& conflict_type);
    PyModule_AddObject(m, "conflict", (PyObject *) &conflict_type);
    
    // Initialize exception type
    error = PyErr_NewException("_conflict.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   

    return m;
}

