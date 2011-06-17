#include "python_zibopt.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int display_column_init(display_column *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object
    char *name;    // name of display column
    SCIP_DISP* d;
    
    if (!PyArg_ParseTuple(args, "Os", &s, &name))
        return -1;
    
    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Load the display column from SCIP
    d = SCIPfindDisp(self->scip, name);
    if (d == NULL) {
        PyErr_SetString(error, "unrecognized display column");
        return -1;
    }
    self->display = d;

    return 0;
}

static void display_column_dealloc(display_column *self) {
    ((PyObject *) self)->ob_type->tp_free(self);
}

static PyObject* display_column_getattr(display_column *self, PyObject *attr_name) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        if (PyUnicode_CompareWithASCIIString(attr_name, "position") == 0)
            return Py_BuildValue("i", SCIPdispGetPosition(self->display));
        if (PyUnicode_CompareWithASCIIString(attr_name, "priority") == 0)
            return Py_BuildValue("i", SCIPdispGetPriority(self->display));
        if (PyUnicode_CompareWithASCIIString(attr_name, "width") == 0)
            return Py_BuildValue("i", SCIPdispGetWidth(self->display));
    }
    return PyObject_GenericGetAttr((PyObject *) self, attr_name);
}

static int display_column_setattr(display_column *self, PyObject *attr_name, PyObject *value) {
    int i;
    
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
         PY_SCIP_SET_INT_MIN("position", self->display->position, -1);
         PY_SCIP_SET_INT_MIN("priority", self->display->priority, -1);
         PY_SCIP_SET_INT_MIN("width", self->display->width, -1);
    }
    return PyObject_GenericSetAttr((PyObject *) self, attr_name, value);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMemberDef display_column_members[] = {
    {NULL} /* Sentinel */
};

static PyMethodDef display_column_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject display_column_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_disp.display_column",        /* tp_name */
    sizeof(display_column),        /* tp_basicsize */
    0,                             /* tp_itemsize */
    (destructor) display_column_dealloc, /* tp_dealloc */
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
    (getattrofunc) display_column_getattr, /* tp_getattro */
    (setattrofunc) display_column_setattr, /* tp_setattro */
    0,                             /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP display column",         /* tp_doc */
    0,                             /* tp_traverse */
    0,                             /* tp_clear */
    0,                             /* tp_richcompare */
    0,                             /* tp_weaklistoffset */
    0,                             /* tp_iter */
    0,                             /* tp_iternext */
    display_column_methods,        /* tp_methods */
    display_column_members,        /* tp_members */
    0,                             /* tp_getset */
    0,                             /* tp_base */
    0,                             /* tp_dict */
    0,                             /* tp_descr_get */
    0,                             /* tp_descr_set */
    0,                             /* tp_dictoffset */
    (initproc) display_column_init,/* tp_init */
    0,                             /* tp_alloc */
    0 ,                            /* tp_new */
};

static PyModuleDef disp_module = {
    PyModuleDef_HEAD_INIT,
    "_disp",
    "SCIP Display Column",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit__disp(void) {
    PyObject* m;

    display_column_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&display_column_type) < 0)
        return NULL;

    m = PyModule_Create(&disp_module); 

    Py_INCREF(&display_column_type);
    PyModule_AddObject(m, "display_column", (PyObject *) &display_column_type);
    
    // Initialize exception type
    error = PyErr_NewException("disp.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   

    return m;
}

