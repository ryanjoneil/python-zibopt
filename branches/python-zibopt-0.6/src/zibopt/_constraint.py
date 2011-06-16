from zibopt import _cons

__all__ = 'constraint', 'ConstraintError'

ConstraintError = _cons.error

class constraint(_cons.constraint):
    '''Stores bounds and coefficients so they can be looked up later'''
    def __init__(self, solver, expression):
        lower = upper = None

        # Make sure we are in the middle if there are two bounds
        if expression.lower is None and expression.upper and expression.upper.upper:
            expression = expression.upper
        elif expression.upper is None and expression.lower and expression.lower.lower:
            expression = expression.lower

        # Cancel out terms from lhs/rhs and keep constants
        if expression.lower:
            e = expression - expression.lower
            e.lower = expression.lower
            e.upper = expression.upper
            expression = e
            lower = -expression.terms.pop((), 0.0) # just the constant

        if expression.upper:
            e = expression - expression.upper
            e.lower = expression.lower
            e.upper = expression.upper
            expression = e
            upper = -expression.terms.pop((), 0.0) # just the constant

        # Make sure we have at least one bound
        if lower is None and upper is None:
            raise ConstraintError('at least one bound is required')

        # Be polite: only pass in upper and lower bounds if we have them
        kwds = {}
        if lower is not None:
            kwds['lower'] = lower
        if upper is not None:
            kwds['upper'] = upper

        # Determine what type of constraint this is: linear or quadratic.
        # Linear constraints will have one variable per term.
        cons_type = _cons.LINEAR
        for term in expression.terms:
            if len(term) > 1:
                cons_type = _cons.NONLINEAR
            elif len(term) > 2:
                # SCIP allows terms like: x, x*y x^2
                # TODO: i think...
                raise ConstraintError('unsupported constraint type')

        super(constraint, self).__init__(solver, cons_type, **kwds)

        # Add variable cofficients to constraint
        for term in expression.terms:
            if len(term) == 1:
                self.linear_term(term[0], expression[term])
            elif len(set(term)) == 1:
                self.quadratic_term(term[0], expression[term], len(term))
            else:
                self.bilinear_term(term[0], term[1], expression[term])

        # Keep this information so we can look it up later
        self.lower = lower
        self.upper = upper
        self.coefficients = expression.terms.copy()
        self.constraint_type = cons_type

