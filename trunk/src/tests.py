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

if __name__ == '__main__':
    unittest.main()

