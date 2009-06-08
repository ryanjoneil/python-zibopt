from zibopt import scip
import unittest

class ScipTest(unittest.TestCase):
    # TODO: add assertions
    def setUp(self):
        pass
        
    def testLoadSolver(self):
        scip.solver()

    def testMax(self):
        solver = scip.solver()
        x1 = solver.variable(coefficient=1, vartype=scip.INTEGER, upper=2)
        x2 = solver.variable(coefficient=1, vartype=scip.INTEGER)
        x3 = solver.variable(coefficient=2, vartype=scip.INTEGER)
        solver.constraint(
            lower = 0, 
            upper = 3,
            coefficients = {
                x1: 1,
                x2: 1,
                x3: 3
            }
        )
        solution = solver.maximize()
        values = solution.values()
        print 'x1:', values[x1]
        print 'x2:', values[x2]
        print 'x3:', values[x3]

    def atestMin(self):
        solver = scip.solver()
        solver.variable('x1')
        solver.variable('x2')
        solver.variable('x3')
        solution = solver.minimize()
        print solution.values()
        
if __name__ == '__main__':
    unittest.main()

