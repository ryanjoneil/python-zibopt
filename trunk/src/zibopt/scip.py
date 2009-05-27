from zibopt import _scip
from zibopt import _vars

class solver(_scip.solver):
    def add_var(self, name):
        _vars.variable(self, name)

