from zibopt import _scip
from zibopt import _vars

variables = []

class solver(_scip.solver):
    def add_var(self, name):
        variables.append(_vars.variable(self, name))

