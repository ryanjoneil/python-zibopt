from zibopt import _cons

__all__ = 'constraint', 'ConstraintError'

ConstraintError = _cons.error

class constraint(_cons.constraint):
    '''Stores bounds and coefficients so they can be looked up later'''
    def __init__(self, *args, **kwds):
        # Yank out variable coefficients since C code isn't expecting them
        try:
            coefficients = kwds['coefficients']
            del kwds['coefficients']
        except KeyError:
            coefficients = {} 

        # If upper or lower bounds are None, remove them to be polite
        if 'lower' in kwds and kwds['lower'] is None:
            del kwds['lower']
        if 'upper' in kwds and kwds['upper'] is None:
            del kwds['upper']
        
        super(constraint, self).__init__(*args, **kwds)

        # Add variable cofficients to constraint
        for k, v in coefficients.items():
            self.variable(k, v)

        # Keep this information so we can look it up later
        self.lower = kwds.get('lower')
        self.upper = kwds.get('upper')
        self.coefficients = coefficients

