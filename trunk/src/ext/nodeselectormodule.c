#include "python_zibopt.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int selector_init(selector *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object
    char *name;    // name of selector
    SCIP_NODESEL *r;
    
    if (!PyArg_ParseTuple(args, "Os", &s, &name))
        return -1;
    
    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Load the selector from SCIP
    r = SCIPfindNodesel(self->scip, name);
    if (r == NULL) {
        PyErr_SetString(error, "unrecognized selector");
        return -1;
    }
    self->nodesel = r;

    return 0;
}

static void selector_dealloc(selector *self) {
    ((PyObject *) self)->ob_type->tp_free(self);
}

static PyObject* selector_getattr(selector *self, PyObject *attr_name) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        if (PyUnicode_CompareWithASCIIString(attr_name, "memsavepriority") == 0)
            return Py_BuildValue("i", SCIPnodeselGetMemsavePriority(self->nodesel));
        if (PyUnicode_CompareWithASCIIString(attr_name, "stdpriority") == 0)
            return Py_BuildValue("i", SCIPnodeselGetStdPriority(self->nodesel));
    }
    return PyObject_GenericGetAttr((PyObject *) self, attr_name);
}

static int selector_setattr(selector *self, PyObject *attr_name, PyObject *value) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        if (PyUnicode_CompareWithASCIIString(attr_name, "memsavepriority") == 0) {
            if (PyLong_Check(value)) {
                SCIPnodeselSetMemsavePriority(self->nodesel, self->scip->set, PyLong_AsLong(value));
                return 0;
            } else {
                PyErr_SetString(error, "invalid value for priority");
                return -1;
            }
        }

        if (PyUnicode_CompareWithASCIIString(attr_name, "stdpriority") == 0) {
            if (PyLong_Check(value)) {
                SCIPnodeselSetStdPriority(self->nodesel, self->scip->set, PyLong_AsLong(value));
                return 0;
            } else {
                PyErr_SetString(error, "invalid value for priority");
                return -1;
            }
        }
    }
    return PyObject_GenericSetAttr((PyObject *) self, attr_name, value);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMemberDef selector_members[] = {
    {NULL} /* Sentinel */
};

static PyMethodDef selector_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject selector_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_nodesel.selector",           /* tp_name */
    sizeof(selector),              /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor) selector_dealloc, /* tp_dealloc */
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
    (getattrofunc) selector_getattr, /* tp_getattro */
    (setattrofunc) selector_setattr, /* tp_setattro */
    0,                             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP selectors",              /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    selector_methods,              /* tp_methods */
    selector_members,              /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    (initproc) selector_init,      /* tp_init */
    0,                             /* tp_alloc */
    0 ,                            /* tp_new */
};

static PyModuleDef nodesel_module = {
    PyModuleDef_HEAD_INIT,
    "_nodesel",
    "SCIP Node Selector",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit__nodesel(void) {
    PyObject* m;

    selector_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(& selector_type) < 0)
        return NULL;

    m = PyModule_Create(&nodesel_module); 

    Py_INCREF(& selector_type);
    PyModule_AddObject(m, "selector", (PyObject *) &selector_type);
    
    // Initialize exception type
    error = PyErr_NewException("_nodesel.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   

    return m;
}

