#include "python_zibopt.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int propagator_init(propagator *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object
    char *name;    // name of propagator
    SCIP_PROP *r;
    
    if (!PyArg_ParseTuple(args, "Os", &s, &name))
        return -1;
    
    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Load the propagator from SCIP
    r = SCIPfindProp(self->scip, name);
    if (r == NULL) {
        PyErr_SetString(error, "unrecognized propagator");
        return -1;
    }
    self->prop = r;

    return 0;
}

static void propagator_dealloc(propagator *self) {
    self->ob_type->tp_free((PyObject *) self);
}

static PyObject* propagator_getattr(propagator *self, PyObject *attr_name) {
    char *attr;

    // Check and make sure we have a string as attribute name...
    if (PyString_Check(attr_name)) {
        attr = PyString_AsString(attr_name);

        if (!strcmp(attr, "frequency"))
            return Py_BuildValue("i", SCIPpropGetFreq(self->prop));
        if (!strcmp(attr, "priority"))
            return Py_BuildValue("i", SCIPpropGetPriority(self->prop));
    }
    return PyObject_GenericGetAttr(self, attr_name);
}

static int propagator_setattr(propagator *self, PyObject *attr_name, PyObject *value) {
    char *attr;
    int i;
    
    // Check and make sure we have a string as attribute name...
    if (PyString_Check(attr_name)) {
        attr = PyString_AsString(attr_name);
        PY_SCIP_SET_INT_MIN("frequency", self->prop->freq, -1); 
        PY_SCIP_SET_PRIORITY(SCIPpropSetPriority, self->prop);
    }
    return PyObject_GenericSetAttr(self, attr_name, value);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMemberDef propagator_members[] = {
    {NULL} /* Sentinel */
};

static PyMethodDef propagator_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject propagator_type = {
    PyObject_HEAD_INIT(NULL)
    0,                             /* ob_size */
    "_prop.propagator",             /* tp_name */
    sizeof(propagator),             /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor) propagator_dealloc, /* tp_dealloc */
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
    propagator_getattr,             /* tp_getattro */
    propagator_setattr,             /* tp_setattro */
    0,                             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP propagators",             /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    propagator_methods,             /* tp_methods */
    propagator_members,             /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    (initproc) propagator_init,     /* tp_init */
    0,                             /* tp_alloc */
    0 ,                            /* tp_new */
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC init_prop(void) {
    PyObject* m;

    propagator_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(& propagator_type) < 0)
        return;

    m = Py_InitModule3("_prop", propagator_methods, "SCIP Propagator");

    Py_INCREF(& propagator_type);
    PyModule_AddObject(m, "propagator", (PyObject *) &propagator_type);
    
    // Initialize exception type
    error = PyErr_NewException("_prop.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   
}

