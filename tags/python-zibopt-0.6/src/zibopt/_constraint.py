from zibopt import _cons

__all__ = 'constraint', 'ConstraintError'

ConstraintError = _cons.error

class constraint(_cons.constraint):
    '''
    Stores bounds and coefficients for problem formulations.  Valid
    constraints for SCIP include linear and bilinear terms.  Examples:
    
        solver += 4 * (x + y) * (x + z) <= 10
        solver += 3*x**2 - 4*x >= 5*y
        solver += 3 <= 4*y <= 5
    '''
    def __init__(self, solver, expression):
        lower = upper = None

        # Make sure we are in the middle if there are two bounds
        if expression.lower is None and expression.upper and expression.upper.upper:
            expression = expression.upper
        elif expression.upper is None and expression.lower and expression.lower.lower:
            expression = expression.lower

        # Cancel out terms from lhs/rhs and keep constants
        if expression.lower and expression.upper is expression.lower:
            # Special case where x == y.  This keeps from double-counting
            # one side of the constraint.
            expression = expression - expression.lower
            lower = upper = -expression.terms.pop((), 0.0)
            expression.lower = lower
            expression.upper = upper

        else:
            # Logic for constraints constructed via <= and >=
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

        # Separate out variables by term type (linear/bilinear)
        linear_vars = [] # information for linear terms
        linear_coef = []
        bilin_var1  = [] # information for bilinear terms
        bilin_var2  = []
        bilin_coef  = []

        for term in expression.terms:
            coef = expression[term]

            # SCIP supports linear terms (3*x) and bilinear (3*x*y + 4*x**2).
            # Everything else should raise a NotImplementedError.
            if len(term) == 1:
                linear_vars.append(term[0])
                linear_coef.append(coef)

            elif len(term) == 2:
                bilin_var1.append(term[0])
                bilin_var2.append(term[1])
                bilin_coef.append(coef)

            else:
                raise NotImplementedError('unsupported term type in constraint')

        super(constraint, self).__init__(
            solver,
            linear_vars,
            linear_coef,
            bilin_var1,
            bilin_var2,
            bilin_coef,
            **kwds
        )

        # Keep this information so we can look it up later
        self.lower = lower
        self.upper = upper
        self.coefficients = expression.terms.copy()

