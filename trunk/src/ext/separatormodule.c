#include "python_zibopt.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int separator_init(separator *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object
    char *name;    // name of separator
    SCIP_SEPA *r;
    
    if (!PyArg_ParseTuple(args, "Os", &s, &name))
        return -1;
    
    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Load the separator from SCIP
    r = SCIPfindSepa(self->scip, name);
    if (r == NULL) {
        PyErr_SetString(error, "unrecognized separator");
        return -1;
    }
    self->sepa = r;

    return 0;
}

static void separator_dealloc(separator *self) {
    ((PyObject *) self)->ob_type->tp_free(self);
}

static PyObject* separator_getattr(separator *self, PyObject *attr_name) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        if (PyUnicode_CompareWithASCIIString(attr_name, "frequency") == 0)
            return Py_BuildValue("i", SCIPsepaGetFreq(self->sepa));
        if (PyUnicode_CompareWithASCIIString(attr_name, "maxbounddist") == 0)
            return Py_BuildValue("d", SCIPsepaGetMaxbounddist(self->sepa));
        if (PyUnicode_CompareWithASCIIString(attr_name, "priority") == 0)
            return Py_BuildValue("i", SCIPsepaGetPriority(self->sepa));
    }
    return PyObject_GenericGetAttr((PyObject *) self, attr_name);
}

static int separator_setattr(separator *self, PyObject *attr_name, PyObject *value) {
    int i;
    double d;
    
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        PY_SCIP_SET_INT_MIN("frequency", self->sepa->freq, -1); 
        PY_SCIP_SET_DBL_MIN("maxbounddist", self->sepa->maxbounddist, -1); 
        PY_SCIP_SET_PRIORITY(SCIPsepaSetPriority, self->sepa);
    }
    return PyObject_GenericSetAttr((PyObject *) self, attr_name, value);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMemberDef separator_members[] = {
    {NULL} /* Sentinel */
};

static PyMethodDef separator_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject separator_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_sepa.separator",             /* tp_name */
    sizeof(separator),             /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor) separator_dealloc, /* tp_dealloc */
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
    (getattrofunc) separator_getattr, /* tp_getattro */
    (setattrofunc) separator_setattr, /* tp_setattro */
    0,                             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP separators",             /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    separator_methods,             /* tp_methods */
    separator_members,             /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    (initproc) separator_init,     /* tp_init */
    0,                             /* tp_alloc */
    0 ,                            /* tp_new */
};

static PyModuleDef sepa_module = {
    PyModuleDef_HEAD_INIT,
    "_sepa",
    "SCIP Separator",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit__sepa(void) {
    PyObject* m;

    separator_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(& separator_type) < 0)
        return NULL;

    m = PyModule_Create(&sepa_module); 

    Py_INCREF(& separator_type);
    PyModule_AddObject(m, "separator", (PyObject *) &separator_type);
    
    // Initialize exception type
    error = PyErr_NewException("_sepa.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   

    return m;
}

