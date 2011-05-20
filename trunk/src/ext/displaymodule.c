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
    ((PyObject *) self)->ob_type->tp_free((PyObject *) self);
}

static PyObject* display_column_getattr(display_column *self, PyObject *attr_name) {
    char *attr;

    // Check and make sure we have a string as attribute name...
    if (PyString_Check(attr_name)) {
        attr = PyString_AsString(attr_name);

        if (!strcmp(attr, "position"))
            return Py_BuildValue("i", SCIPdispGetPosition(self->display));
        if (!strcmp(attr, "priority"))
            return Py_BuildValue("i", SCIPdispGetPriority(self->display));
        if (!strcmp(attr, "width"))
            return Py_BuildValue("i", SCIPdispGetWidth(self->display));
    }
    return PyObject_GenericGetAttr(self, attr_name);
}

static int display_column_setattr(display_column *self, PyObject *attr_name, PyObject *value) {
    char *attr;
    int i;
    
    // Check and make sure we have a string as attribute name...
    if (PyString_Check(attr_name)) {
        attr = PyString_AsString(attr_name);
         PY_SCIP_SET_INT_MIN("position", self->display->position, -1);
         PY_SCIP_SET_INT_MIN("priority", self->display->priority, -1);
         PY_SCIP_SET_INT_MIN("width", self->display->width, -1);
    }
    return PyObject_GenericSetAttr(self, attr_name, value);
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
    PyObject_HEAD_INIT(NULL)
    0,                             /* ob_size */
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
    display_column_getattr,        /* tp_getattro */
    display_column_setattr,        /* tp_setattro */
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

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC init_disp(void) {
    PyObject* m;

    display_column_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&display_column_type) < 0)
        return;

    m = Py_InitModule3("_disp", display_column_methods, "SCIP Display Column");

    Py_INCREF(&display_column_type);
    PyModule_AddObject(m, "display_column", (PyObject *) &display_column_type);
    
    // Initialize exception type
    error = PyErr_NewException("disp.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);   
}
