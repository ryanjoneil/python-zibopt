from zibopt import scip
import unittest

class NonlinearConstraintTest(unittest.TestCase):
    def testBilinearConstraints(self):
        '''Tests nonlinear constraints'''
        solver = scip.solver()

        x1 = solver.variable(upper=1)
        x2 = solver.variable(upper=1)

        solver += 0 <= x1*x2 <= 1
        solution = solver.maximize(objective=x1)

        self.assertEqual(solution.objective, 1.0)
        self.assertEqual(solution[x1], 1.0)
        self.assertEqual(solution[x2], 0.0)

    def testBilinearIntegerConstraints(self):
        '''Tests nonlinear integer constraints'''
        solver = scip.solver()

        x1 = solver.variable(scip.INTEGER, upper=2)
        x2 = solver.variable(scip.INTEGER, upper=2)

        solver += 0 <= x1*x2 <= 3
        solution = solver.maximize(objective=5*x1+2*x2)

        self.assertEqual(solution.objective, 12.0)
        self.assertEqual(solution[x1], 2.0)
        self.assertEqual(solution[x2], 1.0)

    def testnonlinearobjective(self):
        '''Tests nonlinear objective functions'''
        solver = scip.solver()
        x1 = solver.variable(scip.INTEGER)
        solver += 0 <= x1 <= 2
        solution = solver.maximize(objective=x1**2)
        self.assertEqual(solution.objective, 4.0)
        self.assertEqual(solution[x1], 2.0)

    def testDivisionByTerms(self):
        '''Tests that 1/expression raises an exception'''
        solver = scip.solver()

        x1 = solver.variable()
        x2 = solver.variable()

        try:
            1 / x1 <= 1
            self.assertTrue(False)
        except TypeError:
            pass

        try:
            1 / (x1+x2) <= 1
            self.assertTrue(False)
        except TypeError:
            pass

if __name__ == '__main__':
    unittest.main()

