from zibopt import scip
import unittest

class ScipTest(unittest.TestCase):
    # TODO: add assertions
    def setUp(self):
        pass
        
    def testLoadSolver(self):
        scip.solver()

    def testAddVariable(self):
        solver = scip.solver()
        solver.variable('foo')

    def testMax(self):
        solver = scip.solver()
        solver.variable('x1', coefficient=1, vartype=scip.INTEGER, upper=2)
        solver.variable('x2', coefficient=1, vartype=scip.INTEGER)
        solver.variable('x3', coefficient=2, vartype=scip.INTEGER)
        solver.constraint('foo', 
            lower = 0, 
            upper = 3,
            coefficients = {
                'x1': 1,
                'x2': 1,
                'x3': 3
            }
        )
        solution = solver.maximize()
        print solution.values()

    def testMin(self):
        solver = scip.solver()
        solver.variable('x1')
        solver.variable('x2')
        solver.variable('x3')
        solution = solver.minimize()
        print solution.values()
        
if __name__ == '__main__':
    unittest.main()

