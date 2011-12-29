from zibopt import scip
import unittest

class NonlinearConstraintTest(unittest.TestCase):
    def testBilinearConstraints(self):
        '''Tests nonlinear constraints'''
        solver = scip.solver()

        x1 = solver.variable(upper=1)
        x2 = solver.variable(upper=1)

        solver += 0 <= x1*x2 <= 1
        solver += 0 == x1*x2
        solution = solver.maximize(objective=x1)

        self.assertAlmostEqual(solution.objective, 1.0)
        self.assertAlmostEqual(max(solution[x1], solution[x2]), 1.0)
        self.assertAlmostEqual(min(solution[x1], solution[x2]), 0.0)

    def testBilinearIntegerConstraints(self):
        '''Tests nonlinear integer constraints'''
        solver = scip.solver()

        x1 = solver.variable(scip.INTEGER, upper=2)
        x2 = solver.variable(scip.INTEGER, upper=2)

        solver += 0 <= x1*x2 <= 3
        solution = solver.maximize(objective=5*x1+2*x2)

        self.assertAlmostEqual(solution.objective, 12.0)
        self.assertAlmostEqual(solution[x1], 2.0)
        self.assertAlmostEqual(solution[x2], 1.0)

    def testNonlinearMaximize(self):
        '''Tests nonlinear objective maximization'''
        solver = scip.solver()
        x1 = solver.variable(scip.INTEGER)
        solver += 0 <= x1 <= 2
        solution = solver.maximize(objective=x1**2)
        self.assertAlmostEqual(solution.objective, 4.0)
        self.assertAlmostEqual(solution[x1], 2.0)

    def testNonlinearMinimize(self):
        '''Tests nonlinear objective maximization'''
        solver = scip.solver()
        x1 = solver.variable(scip.INTEGER)
        solver += 2 <= x1 <= 4
        solution = solver.minimize(objective=x1**2)
        self.assertAlmostEqual(solution.objective, 4.0)
        self.assertAlmostEqual(solution[x1], 2.0)

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

