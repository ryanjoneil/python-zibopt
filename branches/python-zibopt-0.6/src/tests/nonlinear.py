from zibopt import scip
import unittest

class NonlinearConstraintTest(unittest.TestCase):
    def testConstraints(self):
        '''Tests nonlinear constraints'''
        solver = scip.solver()

        x1 = solver.variable()
        x2 = solver.variable()

        solver += 0 <= x1 <= 1
        #solver += 0 <= x1*x2 <= 1
        solution = solver.maximize(objective=x1)

        self.assertEqual(solution.objective, 1.0)
        self.assertEqual(solution[x1], 1.0)
        self.assertEqual(solution[x2], 0.0)

if __name__ == '__main__':
    unittest.main()

