#include "python_zibopt.h"

static PyObject *solution_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    solution *self = (solution *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

static int solution_init(solution *self, PyObject *args, PyObject *kwds) {
    PyObject *s;   // solver Python object
    solver *solv;  // solver C object

    if (!PyArg_ParseTuple(args, "O", &s))
        return NULL;
    
    // TODO: raise error if solver object of wrong type
    solv =  (solver *) s;
    self->scip = solv->scip;

    self->solution = SCIPgetBestSol(self->scip);
    printf("OBJECTIVE VALUE: %.02f\n", SCIPgetSolOrigObj(self->scip, self->solution));

    return 0;
}

static void solution_dealloc(solution *self) {
    self->ob_type->tp_free((PyObject *) self);
}

static PyMethodDef solution_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject solution_type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "_soln.solution",             /*tp_name*/
    sizeof(solution),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor) solution_dealloc, /*tp_dealloc*/
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
    "SCIP solution objects",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    solution_methods,             /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc) solution_init,      /* tp_init */
    0,                         /* tp_alloc */
    solution_new,                 /* tp_new */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC init_soln(void) {
    PyObject* m;

    if (PyType_Ready(&solution_type) < 0)
        return;

    m = Py_InitModule3("_soln", solution_methods, "SCIP Solution");

    Py_INCREF(&solution_type);
    PyModule_AddObject(m, "solution", (PyObject *) &solution_type);
}

