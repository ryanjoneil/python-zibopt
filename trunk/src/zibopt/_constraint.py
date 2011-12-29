from algebraic import expression
from zibopt import _cons
from zibopt._variable import variable

__all__ = 'constraint', 'ConstraintError'

ConstraintError = _cons.error

class constraint(_cons.constraint):
    '''
    Stores bounds and coefficients for problem formulations.  Valid
    constraints for SCIP include linear and bilinear terms.  Examples::
    
        solver += 4 * (x + y) * (x + z) <= 10
        solver += 3*x**2 - 4*x >= 5*y
        solver += 3 <= 4*y <= 5
    '''
    def __init__(self, solver, expr):
        expr_lower = expr_upper = None

        # Make sure we are in the middle if there are two bounds
        if expr.expr_lower is None and expr.expr_upper and expr.expr_upper.expr_upper:
            expr = expr.expr_upper
        elif expr.expr_upper is None and expr.expr_lower and expr.expr_lower.expr_lower:
            expr = expr.expr_lower

        # Cancel out terms from lhs/rhs and keep constants
        if expr.expr_lower and expr.expr_upper is expr.expr_lower:
            # Special case where x == y.  This keeps from double-counting
            # one side of the constraint.
            expr = expr - expr.expr_lower
            expr_lower = expr_upper = -expr.terms.pop((), 0.0)
            expr.expr_lower = expr_lower
            expr.expr_upper = expr_upper

        else:
            # Logic for constraints constructed via <= and >=
            if expr.expr_lower:
                e = expr - expr.expr_lower
                e.expr_lower = expr.expr_lower
                e.expr_upper = expr.expr_upper
                expr = e
                expr_lower = -expr.terms.pop((), 0.0) # just the constant
    
            if expr.expr_upper:
                e = expr - expr.expr_upper
                e.expr_lower = expr.expr_lower
                e.expr_upper = expr.expr_upper
                expr = e
                expr_upper = -expr.terms.pop((), 0.0) # just the constant

        # Make sure we have at least one bound
        if expr_lower is None and expr_upper is None:
            raise ConstraintError('at least one bound is required')

        # Be polite: only pass in expr_upper and expr_lower bounds if we have them
        kwds = {}
        if expr_lower is not None:
            kwds['lower'] = expr_lower
        if expr_upper is not None:
            kwds['upper'] = expr_upper

        # If expr_upper < expr_lower: constraint error
        if expr_upper is not None and expr_lower is not None and expr_upper < expr_lower:
            raise ConstraintError('invalid constraint: expr_upper < expr_lower')

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

        # Clear off expression bounds if necessary.  This is so we can
        # keep reuse variables without mucking things up, since bounds 
        # are stored on expression (and thus variable) instances.
        expr._clear_bounds()

        # Keep this information so we can look it up later
        self.lower = expr_lower
        self.upper = expr_upper
        self.coefficients = expr.terms.copy()

