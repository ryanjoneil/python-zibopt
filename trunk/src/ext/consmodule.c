#include "python_zibopt.h"
#include "python_zibopt_error.h"

static PyObject *error;

/*****************************************************************************/
/* PYTHON TYPE METHODS                                                       */
/*****************************************************************************/
static int constraint_init(constraint *self, PyObject *args, PyObject *kwds) {
    static char *argnames[] = {
        "solver", "linear_vars", "linear_coef", "bilin_var1", "bilin_var2",
        "bilin_coef", "lower", "upper", NULL
    };
    PyObject *s;           // solver Python object
    solver *solv;          // solver C object
    PyObject *linear_vars; // list of linear terms in constraint
    PyObject *linear_coef; // list of their associated coefficients
    PyObject *bilin_var1;  // list of first bilinear terms in constraint
    PyObject *bilin_var2;  // list of second bilinear terms in constraint
    PyObject *bilin_coef;  // list of their associated coefficients
    double lhs, rhs;       // lhs <= f(x) <= rhs
    int i;

    // SCIPinfinity requires self->scip, so we have to parse the args twice
    if (!PyArg_ParseTuple(args, "OOOOOO|dd", &s, &linear_vars, &linear_coef,
        &bilin_var1, &bilin_var2, &bilin_coef))
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

    // Make sure that linear variables and coefficients are lists containing
    // variables and coefficients, respectively.  Also check that they are
    // the same length and reference the same solver.
    if (!PyList_CheckExact(linear_vars)) {
        PyErr_SetString(error, "linear_vars list required");
        return -1;
    }

    if (!PyList_CheckExact(linear_coef)) {
        PyErr_SetString(error, "linear_coef list required");
        return -1;
    }
 
    self->linear_nvars = PyList_Size(linear_vars);
    if (self->linear_nvars != PyList_Size(linear_coef)) {
        PyErr_SetString(error, "linear_vars and linear_coef must be the same length");
        return -1;
    }

    for (i = 0; i < self->linear_nvars; i++ ) {
        // Check that each element is a variable
        PyObject *v = PyList_GetItem(linear_vars, i);
        if (strcmp(v->ob_type->tp_name, VARIABLE_TYPE_NAME)) {
            PyErr_SetString(error, "invalid variable type");
            return -1;
        }

        // Verify that the variable is associated with this solver
        if (((variable *) v)->scip != self->scip) {
            PyErr_SetString(error, "variable not associated with solver");
            return -1;
        }

        // Check that each element is numeric
        PyObject *o = PyList_GetItem(linear_coef, i);
        if (!(PyLong_Check(o) || PyFloat_Check(o))) {
            PyErr_SetString(error, "invalid coefficient");
            return -1;
        }
    }

    // Do exactly the same thing for bilinear terms
    if (!PyList_CheckExact(bilin_var1)) {
        PyErr_SetString(error, "bilin_var1 list required");
        return -1;
    }

    if (!PyList_CheckExact(bilin_var2)) {
        PyErr_SetString(error, "bilin_var2 list required");
        return -1;
    }

    if (!PyList_CheckExact(bilin_coef)) {
        PyErr_SetString(error, "bilin_coef list required");
        return -1;
    }
 
    self->bilin_nvars = PyList_Size(bilin_var1);
    if (self->bilin_nvars != PyList_Size(bilin_var2) || self->bilin_nvars != PyList_Size(bilin_coef)) {
        PyErr_SetString(error, "bilin_var1, bilin_var2, and bilin_coef must be the same length");
        return -1;
    }

    for (i = 0; i < self->bilin_nvars; i++ ) {
        // Check that each element is a variable
        PyObject *v1 = PyList_GetItem(bilin_var1, i);
        PyObject *v2 = PyList_GetItem(bilin_var2, i);
        if (strcmp(v1->ob_type->tp_name, VARIABLE_TYPE_NAME) || 
            strcmp(v2->ob_type->tp_name, VARIABLE_TYPE_NAME)) {
            PyErr_SetString(error, "invalid variable type");
            return -1;
        }

        // Verify that the variable is associated with this solver
        if (((variable *) v1)->scip != self->scip || ((variable *) v2)->scip != self->scip) {
            PyErr_SetString(error, "variable not associated with solver");
            return -1;
        }

        // Check that each element is numeric
        PyObject *o = PyList_GetItem(bilin_coef, i);
        if (!(PyLong_Check(o) || PyFloat_Check(o))) {
            PyErr_SetString(error, "invalid coefficient");
            return -1;
        }
    }

    // This time is just to get the upper and lower bounds out    
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOOOOO|dd", argnames, &s, 
        &linear_vars, &linear_coef, &bilin_var1, &bilin_var2, &bilin_coef, &lhs, &rhs))
        return -1;

    // Store linear variables and coefficients to pass in to the constraint
    if (self->linear_nvars > 0) {
        self->linear_vars = malloc(self->linear_nvars * sizeof(SCIP_VAR *));
        self->linear_coef = malloc(self->linear_nvars * sizeof(SCIP_Real));

        // Add vars and coefficients into these lists
        for (i = 0; i < self->linear_nvars; i++) {
            self->linear_vars[i] = ((variable *) PyList_GetItem(linear_vars, i))->variable;

            PyObject *coefficient_obj = PyList_GetItem(linear_coef, i);
            SCIP_Real coefficient;
            if (PyLong_Check(coefficient_obj)) {
                coefficient = PyLong_AsDouble(coefficient_obj);
            } else {
                coefficient = PyFloat_AsDouble(coefficient_obj);
            }
            self->linear_coef[i] = coefficient;        
        }

    } else {
        self->linear_vars = NULL;
        self->linear_coef = NULL;
    }

    // Store bilinear variables and coefficients to pass in to the constraint
    if (self->bilin_nvars > 0) {
        self->bilin_var1 = malloc(self->bilin_nvars * sizeof(SCIP_VAR *));
        self->bilin_var2 = malloc(self->bilin_nvars * sizeof(SCIP_VAR *));
        self->bilin_coef = malloc(self->bilin_nvars * sizeof(SCIP_Real));

        // Add vars and coefficients into these lists
        for (i = 0; i < self->bilin_nvars; i++) {
            self->bilin_var1[i] = ((variable *) PyList_GetItem(bilin_var1, i))->variable;
            self->bilin_var2[i] = ((variable *) PyList_GetItem(bilin_var2, i))->variable;

            PyObject *coefficient_obj = PyList_GetItem(bilin_coef, i);
            SCIP_Real coefficient;
            if (PyLong_Check(coefficient_obj)) {
                coefficient = PyLong_AsDouble(coefficient_obj);
            } else {
                coefficient = PyFloat_AsDouble(coefficient_obj);
            }
            self->bilin_coef[i] = coefficient;        
        }

    } else {
        self->bilin_var1 = NULL;
        self->bilin_var2 = NULL;
        self->bilin_coef = NULL;
    }

    // If we have bilinear variables, instantiate a quadratic constraint.
    // Otherwise use the basic linear constraint.
    if (self->bilin_nvars > 0) {
        PY_SCIP_CALL(error, -1,
            SCIPcreateConsQuadratic(self->scip, &self->constraint, "", 
                self->linear_nvars, self->linear_vars, self->linear_coef, 
                self->bilin_nvars, self->bilin_var1, self->bilin_var2, self->bilin_coef,
                lhs, rhs, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE)
        );

    } else {
        PY_SCIP_CALL(error, -1,
            SCIPcreateConsLinear(self->scip, &self->constraint, "", 
                self->linear_nvars, self->linear_vars, self->linear_coef, 
                lhs, rhs, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE)
        );
    }
    

    // Put new constraint at head of linked list
    self->next = (struct constraint *) solv->first_cons;
    solv->first_cons = self;

    return 0;
}

static void constraint_dealloc(constraint *self) {
    if (self->linear_vars != NULL) free(self->linear_vars);
    if (self->linear_coef != NULL) free(self->linear_coef);
    if (self->bilin_var1 != NULL) free(self->bilin_var1);
    if (self->bilin_var2 != NULL) free(self->bilin_var2);
    if (self->bilin_coef != NULL) free(self->bilin_coef);
    ((PyObject *) self)->ob_type->tp_free(self);
}

static PyObject *constraint_register(constraint *self) {
    // In case a constraint is being re-added after optimization,
    // it may be necessary to restart the solver.
    PY_SCIP_CALL(error, NULL, SCIPfreeTransform(self->scip));
    PY_SCIP_CALL(error, NULL, SCIPaddCons(self->scip, self->constraint));
    Py_RETURN_NONE;
}

static PyObject* constraint_getattr(constraint *self, PyObject *attr_name) {
    // Check and make sure we have a string as attribute name...
    if (PyUnicode_Check(attr_name)) {
        if (PyUnicode_CompareWithASCIIString(attr_name, "dual_sol_linear") == 0) {
            SCIP_CONS *transformed;
            SCIPgetTransformedCons(self->scip, self->constraint, &transformed);
            if (transformed == NULL) {
                return Py_BuildValue("d", 0);
            } else {
                return Py_BuildValue("d", SCIPgetDualsolLinear(self->scip, transformed));
            }
        }
    }
    return PyObject_GenericGetAttr((PyObject *) self, attr_name);
}

/*****************************************************************************/
/* MODULE INITIALIZATION                                                     */
/*****************************************************************************/
static PyMethodDef constraint_methods[] = {
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
    (getattrofunc) constraint_getattr, /* tp_getattro */
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

    Py_INCREF(&constraint_type);
    PyModule_AddObject(m, "constraint", (PyObject *) &constraint_type);

    // Initialize exception type
    error = PyErr_NewException("_cons.error", NULL, NULL);
    Py_INCREF(error);
    PyModule_AddObject(m, "error", error);

    return m;
}

