#include "python_zibopt.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int presolver_init(presolver *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object
    char *name;    // name of presolver
    SCIP_PRESOL *r;
    
    if (!PyArg_ParseTuple(args, "Os", &s, &name))
        return -1;
    
    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Load the presolver from SCIP
    r = SCIPfindPresol(self->scip, name);
    if (r == NULL) {
        PyErr_SetString(error, "unrecognized presolver");
        return -1;
    }
    self->presol = r;

    return 0;
}

static void presolver_dealloc(presolver *self) {
    ((PyObject *) self)->ob_type->tp_free(self);
}

static PyObject* presolver_getattr(presolver *self, PyObject *attr_name) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        if (PyUnicode_CompareWithASCIIString(attr_name, "priority") == 0)
            return Py_BuildValue("i", SCIPpresolGetPriority(self->presol));
    }
    return PyObject_GenericGetAttr((PyObject *) self, attr_name);
}

static int presolver_setattr(presolver *self, PyObject *attr_name, PyObject *value) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        PY_SCIP_SET_PRIORITY(SCIPpresolSetPriority, self->presol);
    }
    return PyObject_GenericSetAttr((PyObject *) self, attr_name, value);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMemberDef presolver_members[] = {
    {NULL} /* Sentinel */
};

static PyMethodDef presolver_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject presolver_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_presol.presolver",             /* tp_name */
    sizeof(presolver),             /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor) presolver_dealloc, /* tp_dealloc */
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
    (getattrofunc) presolver_getattr, /* tp_getattro */
    (setattrofunc) presolver_setattr, /* tp_setattro */
    0,                             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP presolvers",             /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    presolver_methods,             /* tp_methods */
    presolver_members,             /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    (initproc) presolver_init,     /* tp_init */
    0,                             /* tp_alloc */
    0 ,                            /* tp_new */
};

#if PY_MAJOR_VERSION >= 3
static PyModuleDef presol_module = {
    PyModuleDef_HEAD_INIT,
    "_presol",
    "SCIP Presolver",
    -1,
    NULL, NULL, NULL, NULL, NULL
};
#endif

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit__presol(void) {
    PyObject* m;

    presolver_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(& presolver_type) < 0)
#if PY_MAJOR_VERSION >= 3
        return NULL;
#else
        return;
#endif

#if PY_MAJOR_VERSION >= 3
    m = PyModule_Create(&presol_module); 
#else
    m = Py_InitModule3("_presol", NULL, "SCIP Presolver");
#endif

    Py_INCREF(& presolver_type);
    PyModule_AddObject(m, "presolver", (PyObject *) &presolver_type);
    
    // Initialize exception type
    error = PyErr_NewException("_presol.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   

#if PY_MAJOR_VERSION >= 3
    return m;
#endif
}

