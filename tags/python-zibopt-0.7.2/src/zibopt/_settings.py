'''
Solver settings for things like branching rules are accessible through 
dictionaries on the solver.  For instance, to change settings on the
inference branching rule::

    solver.branching['inference'].priority = 10000
    solver.branching['inference'].maxdepth = -1
    solver.branching['inference'].maxbounddist = -1
    
Heuristcs allow priority, max depth, frequency, and frequency offset
(freqofs) to be set::

    solver.heuristics['octane'].priority = 500
    solver.heuristics['octane'].maxdepth = -1
    solver.heuristics['octane'].frequency = 10
    solver.heuristics['octane'].freqofs = 5

Node selectors have standard and memory saving priority::

    solver.selectors['bfs'].stdpriority = 1000
    solver.selectors['bfs'].memsavepriority = 10

Propagotors allow priority and frequencey to be set::

    solver.propagators['pseudoobj'].priority = 1000
    solver.propagators['pseudoobj'].frequency = 10
    
Separators have settinsg for priority, maxbounddist, and frequency::

    solver.separators['clique'].priority = 10000
    solver.separators['clique'].maxbounddist = -1
    solver.separators['clique'].frequency = 10000

Priority can also be set on conflict handlers and presolvers::

    solver.conflict['logicor'].priority = 10000
    solver.presolvers['dualfix'].priority = 10000

Display settings can also be set for solver output.  These are
useful when passing quiet=False on solver instantiation::

    solver = scip.solver()
    solver.display['cuts'].priority = 5
    solver.display['cuts'].width = 10
    solver.display['cuts'].position = 3

See the SCIP documentation for available branching rules, heuristics, 
any other settings, and what they do.
'''

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

