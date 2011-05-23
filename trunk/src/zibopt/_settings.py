from zibopt import (
    _branch, _conflict, _disp, _heur, _nodesel, _presol, _prop, _sepa
)

__all__ = (
    'BranchingError', 
    'ConflictError', 
    'DisplayError',
    'HeuristicError',
    'PresolverError',
    'PropagatorError',
    'SelectorError',
    'SeparatorError'
)

# Solver Settings Errors
BranchingError  = _branch.error
ConflictError   = _conflict.error
DisplayError    = _disp.error
HeuristicError  = _heur.error
PresolverError  = _presol.error
PropagatorError = _prop.error
SelectorError   = _nodesel.error
SeparatorError  = _sepa.error

