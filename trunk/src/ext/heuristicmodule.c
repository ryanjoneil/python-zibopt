#include "python_zibopt.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int heuristic_init(heuristic *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object
    char *name;    // name of heuristic
    SCIP_HEUR *r;
    
    if (!PyArg_ParseTuple(args, "Os", &s, &name))
        return -1;
    
    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Load the heuristic from SCIP
    r = SCIPfindHeur(self->scip, name);
    if (r == NULL) {
        PyErr_SetString(error, "unrecognized heuristic");
        return -1;
    }
    self->heur = r;

    return 0;
}

static void heuristic_dealloc(heuristic *self) {
    ((PyObject *) self)->ob_type->tp_free(self);
}

static PyObject* heuristic_getattr(heuristic *self, PyObject *attr_name) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        if (PyUnicode_CompareWithASCIIString(attr_name, "freqofs") == 0)
            return Py_BuildValue("i", SCIPheurGetFreqofs(self->heur));
        if (PyUnicode_CompareWithASCIIString(attr_name, "frequency") == 0)
            return Py_BuildValue("i", SCIPheurGetFreq(self->heur));
        if (PyUnicode_CompareWithASCIIString(attr_name, "maxdepth") == 0)
            return Py_BuildValue("i", SCIPheurGetMaxdepth(self->heur));
        if (PyUnicode_CompareWithASCIIString(attr_name, "priority") == 0)
            return Py_BuildValue("i", SCIPheurGetPriority(self->heur));
    }
    return PyObject_GenericGetAttr((PyObject *) self, attr_name);
}

static int heuristic_setattr(heuristic *self, PyObject *attr_name, PyObject *value) {
    int i;
    
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        PY_SCIP_SET_INT_MIN("freqofs", self->heur->freqofs, 0); 
        PY_SCIP_SET_INT_MIN("frequency", self->heur->freq, -1); 
        PY_SCIP_SET_INT_MIN("maxdepth", self->heur->maxdepth, -1); 
        PY_SCIP_SET_PRIORITY(SCIPheurSetPriority, self->heur);
    }
    return PyObject_GenericSetAttr((PyObject *) self, attr_name, value);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMemberDef heuristic_members[] = {
    {NULL} /* Sentinel */
};

static PyMethodDef heuristic_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject heuristic_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_heur.heuristic",             /* tp_name */
    sizeof(heuristic),             /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor) heuristic_dealloc, /* tp_dealloc */
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
    (getattrofunc) heuristic_getattr, /* tp_getattro */
    (setattrofunc) heuristic_setattr, /* tp_setattro */
    0,                             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP heuristics",             /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    heuristic_methods,             /* tp_methods */
    heuristic_members,             /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    (initproc) heuristic_init,     /* tp_init */
    0,                             /* tp_alloc */
    0 ,                            /* tp_new */
};

static PyModuleDef heur_module = {
    PyModuleDef_HEAD_INIT,
    "_heur",
    "SCIP Heuristic",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit__heur(void) {
    PyObject* m;

    heuristic_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(& heuristic_type) < 0)
        return NULL;

    m = PyModule_Create(&heur_module); 

    Py_INCREF(& heuristic_type);
    PyModule_AddObject(m, "heuristic", (PyObject *) &heuristic_type);
    
    // Initialize exception type
    error = PyErr_NewException("_heur.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   

    return m;
}

