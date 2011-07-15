#include "python_zibopt.h"
#include "python_zibopt_error.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int lp_init(lp *self, PyObject *args, PyObject *kwds) {
    static char *argnames[] = {"sense", NULL};
    int sense;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "i", argnames, &sense))
        return -1;

    // TODO: unit test this
    if (sense != SCIP_OBJSENSE_MAXIMIZE && sense != SCIP_OBJSENSE_MINIMIZE) {
        PyErr_SetString(error, "invalid objective sense");
        return -1;
    }
    
    PY_SCIP_CALL(error, -1, SCIPlpiCreate(&self->lpi, "", sense));

    return 0;
}

static void lp_dealloc(lp *self) {
    if (self->lpi != NULL)
        SCIPlpiFree(&self->lpi);
    ((PyObject *) self)->ob_type->tp_free(self);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMethodDef lp_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject lp_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_lp.lp",                    /* tp_name */
    sizeof(lp),                  /* tp_basicsize */
    0,                           /* tp_itemsize */
    (destructor) lp_dealloc,     /* tp_dealloc */
    0,                           /* tp_print */
    0,                           /* tp_getattr */
    0,                           /* tp_setattr */
    0,                           /* tp_compare */
    0,                           /* tp_repr */
    0,                           /* tp_as_number */
    0,                           /* tp_as_sequence */
    0,                           /* tp_as_mapping */
    0,                           /* tp_hash */
    0,                           /* tp_call */
    0,                           /* tp_str */
    0,                           /* tp_getattro */
    0,                           /* tp_setattro */
    0,                           /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP LP objects",           /* tp_doc */
    0,                           /* tp_traverse */
    0,                           /* tp_clear */
    0,                           /* tp_richcompare */
    0,                           /* tp_weaklistoffset */
    0,                           /* tp_iter */
    0,                           /* tp_iternext */
    lp_methods,                  /* tp_methods */
    0,                           /* tp_members */
    0,                           /* tp_getset */
    0,                           /* tp_base */
    0,                           /* tp_dict */
    0,                           /* tp_descr_get */
    0,                           /* tp_descr_set */
    0,                           /* tp_dictoffset */
    (initproc) lp_init,          /* tp_init */
    0,                           /* tp_alloc */
    0,                           /* tp_new */
};

static PyModuleDef lp_module = {
    PyModuleDef_HEAD_INIT,
    "_lp",
    "SCIP LP Solver",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit__lp(void) {
    PyObject* m;

    lp_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&lp_type) < 0)
        return NULL;

    m = PyModule_Create(&lp_module); 

    // Constants on scip module
    PyModule_AddIntConstant(m, "MAXIMIZE", SCIP_OBJSENSE_MAXIMIZE);
    PyModule_AddIntConstant(m, "MINIMIZE", SCIP_OBJSENSE_MINIMIZE);

    Py_INCREF(&lp_type);
    PyModule_AddObject(m, "lp", (PyObject *) &lp_type);

    // Initialize exception type
    error = PyErr_NewException("_lp.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);

    return m;
}

