from zibopt import _cons
from zibopt._expression import expression
from zibopt._variable import variable

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
    def __init__(self, solver, expr):
        # Allows constraints like x <= 1
        if isinstance(expr, variable):
            if expr.lower is not None or expr.upper is not None:
                kwds = {}
                if expr.lower is not None:
                    kwds['lower'] = expression({():expr.lower})
                if expr.upper is not None:
                    kwds['upper'] = expression({():expr.upper})
                expr = expression({(expr,):1.0}, **kwds)

        lower = upper = None

        # Make sure we are in the middle if there are two bounds
        if expr.lower is None and expr.upper and expr.upper.upper:
            expr = expr.upper
        elif expr.upper is None and expr.lower and expr.lower.lower:
            expr = expr.lower

        # Cancel out terms from lhs/rhs and keep constants
        if expr.lower and expr.upper is expr.lower:
            # Special case where x == y.  This keeps from double-counting
            # one side of the constraint.
            expr = expr - expr.lower
            lower = upper = -expr.terms.pop((), 0.0)
            expr.lower = lower
            expr.upper = upper

        else:
            # Logic for constraints constructed via <= and >=
            if expr.lower:
                e = expr - expr.lower
                e.lower = expr.lower
                e.upper = expr.upper
                expr = e
                lower = -expr.terms.pop((), 0.0) # just the constant
    
            if expr.upper:
                e = expr - expr.upper
                e.lower = expr.lower
                e.upper = expr.upper
                expr = e
                upper = -expr.terms.pop((), 0.0) # just the constant

        # Make sure we have at least one bound
        if lower is None and upper is None:
            raise ConstraintError('at least one bound is required')

        # Be polite: only pass in upper and lower bounds if we have them
        kwds = {}
        if lower is not None:
            kwds['lower'] = lower
        if upper is not None:
            kwds['upper'] = upper

        # If upper < lower: constraint error
        if upper is not None and lower is not None and upper < lower:
            raise ConstraintError('invalid constraint: upper < lower')

        # Separate out variables by term type (linear/bilinear)
        linear_vars = [] # information for linear terms
        linear_coef = []
        bilin_var1  = [] # information for bilinear terms
        bilin_var2  = []
        bilin_coef  = []

        for term in expr.terms:
            coef = expr[term]

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
        self.coefficients = expr.terms.copy()

