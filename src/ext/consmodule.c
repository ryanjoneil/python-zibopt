#include "python_zibopt.h"

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int constraint_init(variable *self, PyObject *args, PyObject *kwds) {
    PyObject *s;     // solver Python object
    solver *solv;    // solver C object
    const char *n;   // name
    double lhs, rhs; // lhs <= a'x <= rhs

    // TODO: allow +/- infinity for lhs/rhs
    
    if (!PyArg_ParseTuple(args, "Os", &s, &n))
        return NULL;
    
    self->name = n;
    
    // TODO: raise error if solver object of wrong type
    solv = (solver *) s;
    self->scip = solv->scip;
    
    // Put new constraint at head of linked list
    self->next = solv->first_cons;
    solv->first_cons = self;
    
    // TODO: build constraint

    return 0;
}

static void constraint_dealloc(constraint *self) {
    self->ob_type->tp_free((PyObject *) self);
}

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMethodDef constraint_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject constraint_type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "_cons.constraint",             /*tp_name*/
    sizeof(constraint),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor) constraint_dealloc, /*tp_dealloc*/
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
    "SCIP constraint objects",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    constraint_methods,             /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc) constraint_init,      /* tp_init */
    0,                         /* tp_alloc */
    0,                 /* tp_new */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC init_cons(void) {
    PyObject* m;

    constraint_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&constraint_type) < 0)
        return;

    m = Py_InitModule3("_cons", constraint_methods, "SCIP Constraint");

    Py_INCREF(&constraint_type);
    PyModule_AddObject(m, "constraint", (PyObject *) &constraint_type);
}

