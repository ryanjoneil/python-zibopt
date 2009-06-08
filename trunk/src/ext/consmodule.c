#include "python_zibopt.h"

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int constraint_init(constraint *self, PyObject *args, PyObject *kwds) {
    static char *argnames[] = {"solver", "lower", "upper", NULL};
    PyObject *s;     // solver Python object
    solver *solv;    // solver C object
    double lhs, rhs; // lhs <= a'x <= rhs

    // SCIPinfinity requires self->scip, so we have to parse the args twice
    if (!PyArg_ParseTuple(args, "O|dd", &s))
        return NULL;

    // TODO: raise error if solver object of wrong type
    solv = (solver *) s;
    self->scip = solv->scip;
        
    lhs = -SCIPinfinity(self->scip);
    rhs = SCIPinfinity(self->scip);

    // This time is just to get the upper and lower bounds out    
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|dd", argnames, &s, &lhs, &rhs))
        return NULL;

    // Put new constraint at head of linked list
    self->next = solv->first_cons;
    solv->first_cons = self;
    
    // SCIPcreateConsLinear Arguments:
    // scip        SCIP data structure
    // cons        pointer to hold the created constraint
    // name        name of constraint
    // nvars       number of nonzeros in the constraint
    // vars        array with variables of constraint entries
    // vals        array with coefficients of constraint entries
    // lhs         left hand side of constraint
    // rhs         right hand side of constraint
    // initial     should the LP relaxation of constraint be in the initial LP? 
    //             Usually set to TRUE. Set to FALSE for 'lazy constraints'.
    // separate    should the constraint be separated during LP processing? 
    //             Usually set to TRUE.
    // enforce     should the constraint be enforced during node processing? 
    //             TRUE for model constraints, FALSE for additional, redundant 
    //             constraints.
    // check       should the constraint be checked for feasibility? TRUE for 
    //             model constraints, FALSE for additional, redundant constraints.
    // propagate   should the constraint be propagated during node processing? 
    //             Usually set to TRUE.
    // local       is constraint only valid locally? Usually set to FALSE. Has 
    //             to be set to TRUE, e.g., for branching constraints.
    // modifiable  is constraint modifiable (subject to column generation)? 
    //             Usually set to FALSE. In column generation applications, set
    //             to TRUE if pricing adds coefficients to this constraint.
    // dynamic     Is constraint subject to aging? Usually set to FALSE. Set to 
    //             TRUE for own cuts which are seperated as constraints.
    // removable   should the relaxation be removed from the LP due to aging or 
    //             cleanup? Usually set to FALSE. Set to TRUE for 'lazy 
    //             constraints' and 'user cuts'.
    // stickingatnode   should the constraint always be kept at the node where 
    //             it was added, even if it may be moved to a more global node?
    //             Usually set to FALSE. Set to TRUE to for constraints that 
    //             represent node data.
    SCIPcreateConsLinear(self->scip, &self->constraint, "", 0, NULL, NULL, 
        lhs, rhs, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE);

    return 0;
}

static void constraint_dealloc(constraint *self) {
    self->ob_type->tp_free((PyObject *) self);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/
static PyObject *constraint_variable(constraint *self, PyObject *args) {
    PyObject *v;
    double coefficient;
    variable *var;

    if (!PyArg_ParseTuple(args, "Od", &v, &coefficient))
        return NULL;
        
    // TODO: raise error if var object of wrong type
    var = (variable *) v;

    SCIPaddCoefLinear(self->scip, self->constraint, var->variable, coefficient);
    Py_RETURN_NONE;
}

static PyObject *constraint_register(constraint *self) {
    SCIPaddCons(self->scip, self->constraint);
    Py_RETURN_NONE;
}

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMethodDef constraint_methods[] = {
    {"variable", (PyCFunction) constraint_variable, METH_VARARGS, "add a variable to a constraint"},
    {"register", (PyCFunction) constraint_register, METH_NOARGS, "registers the constraint with the solver"},
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
    0,                       /* tp_traverse */
    0,                       /* tp_clear */
    0,                       /* tp_richcompare */
    0,                       /* tp_weaklistoffset */
    0,                       /* tp_iter */
    0,                       /* tp_iternext */
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

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
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

