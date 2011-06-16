#include "python_zibopt.h"
#include "python_zibopt_error.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int constraint_init(constraint *self, PyObject *args, PyObject *kwds) {
    static char *argnames[] = {"solver", "constraint_type", "lower", "upper", NULL};
    PyObject *s;     // solver Python object
    solver *solv;    // solver C object
    int cons_type;   // linear or quadratic
    double lhs, rhs; // lhs <= a'x <= rhs

    // SCIPinfinity requires self->scip, so we have to parse the args twice
    if (!PyArg_ParseTuple(args, "Oi|dd", &s, &cons_type))
        return -1;

    // Check solver type in the best way we seem to have available
    if (strcmp(s->ob_type->tp_name, SOLVER_TYPE_NAME)) {
        PyErr_SetString(error, "invalid solver type");
        return -1;
    }
    
    solv = (solver *) s;
    self->scip = solv->scip;
        
    lhs = -SCIPinfinity(self->scip);
    rhs = SCIPinfinity(self->scip);

    // This time is just to get the upper and lower bounds out    
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "Oi|dd", argnames, &s, &cons_type, &lhs, &rhs))
        return -1;

    self->constraint_type = cons_type;

    if (cons_type == PY_SCIP_CONSTRAINT_LINEAR) {
        PY_SCIP_CALL(error, -1,
            SCIPcreateConsLinear(self->scip, &self->constraint, "", 0, NULL, NULL, 
                lhs, rhs, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE)
        );
    } else {
        PY_SCIP_CALL(error, -1,
            SCIPcreateConsQuadratic(self->scip, &self->constraint, "", 0, NULL, NULL, 0, NULL, NULL, NULL,
                lhs, rhs, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE)
        );
    }

    // Put new constraint at head of linked list
    self->next = (struct constraint *) solv->first_cons;
    solv->first_cons = self;

    return 0;
}

static void constraint_dealloc(constraint *self) {
    ((PyObject *) self)->ob_type->tp_free(self);
}

/*****************************************************************************/
/* ADDITONAL METHODS                                                         */
/*****************************************************************************/
static PyObject *constraint_linear_term(constraint *self, PyObject *args) {
    PyObject *v;
    double coefficient;
    variable *var;

    if (!PyArg_ParseTuple(args, "Od", &v, &coefficient))
        return NULL;
        
    // Check and make sure we have a real variable type
    if (strcmp(v->ob_type->tp_name, VARIABLE_TYPE_NAME)) {
        PyErr_SetString(error, "invalid variable type");
        return NULL;
    }
    var = (variable *) v;

    // Verify that the variable is associated with this solver
    if (var->scip != self->scip) {
        PyErr_SetString(error, "variable not associated with solver");
        return NULL;
    }

    // How to add linear variable depends on what type of constraint we have
    if (self->constraint_type == PY_SCIP_CONSTRAINT_LINEAR) {
        PY_SCIP_CALL(error, NULL, 
            SCIPaddCoefLinear(self->scip, self->constraint, var->variable, coefficient)
        );
    } else {
        PY_SCIP_CALL(error, NULL, 
            SCIPaddLinearVarQuadratic(self->scip, self->constraint, var->variable, coefficient)
        );
    }

    Py_RETURN_NONE;
}

static PyObject *constraint_quadratic_term(constraint *self, PyObject *args) {
    PyObject *v;
    double coefficient;
    double exponent;
    variable *var;

    if (!PyArg_ParseTuple(args, "Odd", &v, &coefficient, &exponent))
        return NULL;
        
    // Check and make sure we have a real variable type
    if (strcmp(v->ob_type->tp_name, VARIABLE_TYPE_NAME)) {
        PyErr_SetString(error, "invalid variable type");
        return NULL;
    }
    var = (variable *) v;

    // Verify that the variable is associated with this solver
    if (var->scip != self->scip) {
        PyErr_SetString(error, "variable not associated with solver");
        return NULL;
    }

    PY_SCIP_CALL(error, NULL, 
        SCIPaddQuadVarQuadratic(self->scip, self->constraint, var->variable, coefficient, exponent)
    );
    Py_RETURN_NONE;
}

static PyObject *constraint_bilinear_term(constraint *self, PyObject *args) {
    PyObject *v1;
    PyObject *v2;
    double coefficient;
    variable *var1;
    variable *var2;

    if (!PyArg_ParseTuple(args, "OOd", &v1, &v2, &coefficient))
        return NULL;
        
    // Check and make sure we have a real variable type
    if (strcmp(v1->ob_type->tp_name, VARIABLE_TYPE_NAME) ||
        strcmp(v1->ob_type->tp_name, VARIABLE_TYPE_NAME)) {
        PyErr_SetString(error, "invalid variable type");
        return NULL;
    }
    var1 = (variable *) v1;
    var2 = (variable *) v2;

    // Verify that the variable is associated with this solver
    if (var1->scip != self->scip || var2->scip != self->scip) {
        PyErr_SetString(error, "variable not associated with solver");
        return NULL;
    }

    PY_SCIP_CALL(error, NULL, 
        SCIPaddBilinTermQuadratic(self->scip, self->constraint, var1->variable, var2->variable, coefficient)
    );
    Py_RETURN_NONE;
}

static PyObject *constraint_register(constraint *self) {
    // In case a constraint is being re-added after optimization,
    // it may be necessary to restart the solver.
    PY_SCIP_CALL(error, NULL, SCIPfreeTransform(self->scip));
    PY_SCIP_CALL(error, NULL, SCIPaddCons(self->scip, self->constraint));
    Py_RETURN_NONE;
}

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMethodDef constraint_methods[] = {
    {"linear_term", (PyCFunction) constraint_linear_term, METH_VARARGS, "add a variable to a constraint"},
    {"quadratic_term", (PyCFunction) constraint_quadratic_term, METH_VARARGS, "add a quadratic term to a constraint"},
    {"bilinear_term", (PyCFunction) constraint_bilinear_term, METH_VARARGS, "add a bilinear term to a constraint"},
    {"register", (PyCFunction) constraint_register, METH_NOARGS,  "registers the constraint with the solver"},
    {NULL} /* Sentinel */
};

static PyTypeObject constraint_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_cons.constraint",              /* tp_name */
    sizeof(constraint),              /* tp_basicsize */
    0,                               /* tp_itemsize */
    (destructor) constraint_dealloc, /* tp_dealloc */
    0,                               /* tp_print */
    0,                               /* tp_getattr */
    0,                               /* tp_setattr */
    0,                               /* tp_compare */
    0,                               /* tp_repr */
    0,                               /* tp_as_number */
    0,                               /* tp_as_sequence */
    0,                               /* tp_as_mapping */
    0,                               /* tp_hash */
    0,                               /* tp_call */
    0,                               /* tp_str */
    0,                               /* tp_getattro */
    0,                               /* tp_setattro */
    0,                               /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "SCIP constraint objects",       /* tp_doc */
    0,                               /* tp_traverse */
    0,                               /* tp_clear */
    0,                               /* tp_richcompare */
    0,                               /* tp_weaklistoffset */
    0,                               /* tp_iter */
    0,                               /* tp_iternext */
    constraint_methods,              /* tp_methods */
    0,                               /* tp_members */
    0,                               /* tp_getset */
    0,                               /* tp_base */
    0,                               /* tp_dict */
    0,                               /* tp_descr_get */
    0,                               /* tp_descr_set */
    0,                               /* tp_dictoffset */
    (initproc) constraint_init,      /* tp_init */
    0,                               /* tp_alloc */
    0,                               /* tp_new */
};

static PyModuleDef cons_module = {
    PyModuleDef_HEAD_INIT,
    "_cons",
    "SCIP Constraint",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

#ifndef PyMODINIT_FUNC    /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit__cons(void) {
    PyObject* m;

    constraint_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&constraint_type) < 0)
        return NULL;

    m = PyModule_Create(&cons_module); 

    // Constants on constraint module
    PyModule_AddIntConstant(m, "LINEAR", PY_SCIP_CONSTRAINT_LINEAR);
    PyModule_AddIntConstant(m, "NONLINEAR", PY_SCIP_CONSTRAINT_NONLINEAR);

    Py_INCREF(&constraint_type);
    PyModule_AddObject(m, "constraint", (PyObject *) &constraint_type);

    // Initialize exception type
    error = PyErr_NewException("_cons.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);

    return m;
}

