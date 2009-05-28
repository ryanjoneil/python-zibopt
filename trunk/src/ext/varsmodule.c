#include "python_zibopt.h"

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int variable_init(variable *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object
    const char *n; // name
    double c;      // coefficient

    if (!PyArg_ParseTuple(args, "Osd", &s, &n, &c))
        return NULL;
    
    self->name = n;
    
    // TODO: raise error if solver object of wrong type
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Put new variable at head of linked list
    self->next = solv->first;
    solv->first = self;
    
    // TODO: different types of variables; optional bounds
    
    // SCIPcreateVar Arguments:
    // scip         SCIP data structure
    // var          pointer to variable object
    // name         name of variable, or NULL for automatic name creation
    // lb           lower bound of variable
    // ub           upper bound of variable
    // obj          objective function value
    // vartype      type of variable
    // initial      should var's column be present in the initial root LP?
    // removable    is var's column removable from the LP?
    // vardata      user data for this specific variable 
    SCIPcreateVar(self->scip, &self->variable, n, 0.0, 1.0, c, SCIP_VARTYPE_BINARY, TRUE, FALSE, NULL, NULL, NULL, NULL);
    SCIPaddVar(self->scip, self->variable);

    return 0;
}

static void variable_dealloc(variable *self) {
    self->ob_type->tp_free((PyObject *) self);
}

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMethodDef variable_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject variable_type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "_vars.variable",             /*tp_name*/
    sizeof(variable),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor) variable_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "SCIP variable objects",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    variable_methods,             /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc) variable_init,      /* tp_init */
    0,                         /* tp_alloc */
    0,                 /* tp_new */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC init_vars(void) {
    PyObject* m;

    variable_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&variable_type) < 0)
        return;

    m = Py_InitModule3("_vars", variable_methods, "SCIP Variable");

    Py_INCREF(&variable_type);
    PyModule_AddObject(m, "variable", (PyObject *) &variable_type);
}

