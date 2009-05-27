from zibopt import scip
import unittest

class ScipTest(unittest.TestCase):
    def setUp(self):
        pass
        
    def testLoadSolver(self):
        scip.solver()

    def testAddVariable(self):
        solver = scip.solver()
        solver.add_var('foo')

    def testMax(self):
        solver = scip.solver()
        solver.add_var('x1')
        solver.add_var('x2')
        solver.add_var('x3')
        solver.maximize()

    def testMin(self):
        solver = scip.solver()
        solver.add_var('x1')
        solver.add_var('x2')
        solver.add_var('x3')
        solver.minimize()
        # TODO: assertions
        
if __name__ == '__main__':
    unittest.main()

