from zibopt import scip
import unittest

class ScipTest(unittest.TestCase):
    def testLoadSolver(self):
        '''Try loading the SCIP solver'''
        solver = scip.solver()
        
    def testMax(self):
        '''Maximize an objective subject to integer constraints'''
        solver = scip.solver()
        x1 = solver.variable(scip.INTEGER)
        x2 = solver.variable(scip.INTEGER)
        x3 = solver.variable(scip.INTEGER)
        print x1 + 2*x2 <= 3
        
        #solver += x1 <= 2
        #solver += x1 + x2 + 3*x3 <= 3
        #solution = solver.maximize(objective=x1+x2+2*x3)

        #self.assertTrue(solution)
        #self.assertAlmostEqual(solution.objective, 3)
        #self.assertAlmostEqual(solution[x3], 0)

if __name__ == '__main__':
    unittest.main()

