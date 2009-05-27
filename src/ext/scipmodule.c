#include "python_zibopt.h"

// TODO: wrap scip calls in exception handling

static PyObject *solver_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    solver *self;

    self = (solver *) type->tp_alloc(type, 0);
    if (self != NULL) {
        // Initialize SCIP
        SCIPcreate(&self->scip);
        
        // Default plugins, heuristics, etc
        SCIPincludeDefaultPlugins(self->scip);
        
        // Create an empty problem
        // TODO: allow user to name problem?
        // TODO: what are all these NULLs for?
        SCIPcreateProb(self->scip, "python-zibobt", NULL, NULL, NULL, NULL, NULL, NULL);
        
        // TODO: make this configurable
        SCIPsetObjsense(self->scip, SCIP_OBJSENSE_MAXIMIZE);
    }

    return (PyObject *) self;
}

static int solver_init(solver *self, PyObject *args, PyObject *kwds) {
    return 0;
}

static void solver_dealloc(solver *self) {
    if (self->scip)
        SCIPfree(&self->scip);

    self->ob_type->tp_free((PyObject *) self);
}

static PyMethodDef solver_methods[] = {
    {NULL} /* Sentinel */
};

static PyTypeObject solver_type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "_scip.solver",             /*tp_name*/
    sizeof(solver),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor) solver_dealloc, /*tp_dealloc*/
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
    "SCIP solver objects",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    solver_methods,             /* tp_methods */
    0,//scip_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc) solver_init,      /* tp_init */
    0,                         /* tp_alloc */
    solver_new,                 /* tp_new */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC init_scip(void) {
    PyObject* m;

    if (PyType_Ready(&solver_type) < 0)
        return;

    m = Py_InitModule3("_scip", solver_methods, "SCIP Solver");

    Py_INCREF(&solver_type);
    PyModule_AddObject(m, "solver", (PyObject *) &solver_type);
}

