from zibopt import scip
import unittest

class ScipTest(unittest.TestCase):
    def setUp(self):
        pass
        
    def atestLoadSolver(self):
        scip.solver()

    def testAddVariable(self):
        solver = scip.solver()
        solver.variable('foo')

    def testMax(self):
        solver = scip.solver()
        solver.variable('x1', 1)
        solver.variable('x2', 1)
        solver.variable('x3', 2)
        solution = solver.maximize()

    def testMin(self):
        solver = scip.solver()
        solver.variable('x1')
        solver.variable('x2')
        solver.variable('x3')
        solution = solver.minimize()
        # TODO: assertions
        
if __name__ == '__main__':
    unittest.main()

