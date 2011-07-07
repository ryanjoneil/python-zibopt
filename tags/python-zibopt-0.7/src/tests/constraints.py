from zibopt import scip
import unittest

class ConstraintTest(unittest.TestCase):
    def testConstraintsAndObjective(self):
        '''Linear combinations of variables create constraints or objectives'''
        solver = scip.solver()
        x1 = solver.variable(scip.INTEGER)
        x2 = solver.variable(scip.INTEGER)
        solver += 1 <= x1 + 2*x2 <= 2
        
        # Test maximizing
        solution = solver.maximize(objective=x1+x2)
        self.assertEqual(solution[x1], 2.0)
        self.assertEqual(solution[x2], 0.0)
        self.assertEqual(solution.objective, 2.0)
                
        # Test maximizing
        solution = solver.maximize(objective=x1+5*x2)
        self.assertEqual(solution[x1], 0.0)
        self.assertEqual(solution[x2], 1.0)
        self.assertEqual(solution.objective, 5.0)

        # Test minimizing
        solution = solver.minimize(objective=x1+0.25*x2)
        self.assertEqual(solution[x1], 0.0)
        self.assertEqual(solution[x2], 1.0)
        self.assertEqual(solution.objective, 0.25)

    def testAlgebraicConstraints(self):
        '''Tests algebraic format for solver.constraint(...)'''
        solver = scip.solver()

        x1 = solver.variable(scip.INTEGER)
        x2 = solver.variable(scip.INTEGER)
        c  = solver.constraint(1 <= x1 + 2*x2 <= 4)
       
        self.assertEqual(c.lower, 1.0)
        self.assertEqual(c.upper, 4.0)
        self.assertEqual(c.coefficients[(x1,)], 1.0)
        self.assertEqual(c.coefficients[(x2,)], 2.0)

class ConstraintRemovalTest(unittest.TestCase):
    def setUp(self):
        self.solver = scip.solver()
        self.x1 = self.solver.variable(scip.INTEGER)
        self.x2 = self.solver.variable(scip.INTEGER)

        self.c1 = self.solver.constraint(2*self.x1 + 2*self.x2 <= 4)
        self.c2 = self.solver.constraint(2*self.x1 + 2*self.x2 <= 3)

    def testBasicConstraintRemoval(self):
        '''Tests basic removal of a constraint'''
        # Test with both constraints active
        self.assertEqual(1.0, self.solver.maximize(objective=self.x1+self.x2).objective)

        # Remove c2 and test again
        self.solver -= self.c2
        self.assertEqual(2.0, self.solver.maximize(objective=self.x1+self.x2).objective)
        
        self.solver += self.c2

    def testConstraintDuplication(self):
        '''Tests multiple additions/deletions of the same constraint'''
        self.solver -= self.c2
        self.solver -= self.c2
        self.assertEqual(2.0, self.solver.maximize(objective=self.x1+self.x2).objective)

        self.solver += self.c2
        self.solver += self.c2
        self.assertEqual(1.0, self.solver.maximize(objective=self.x1+self.x2).objective)

class ConstraintAttributesTest(unittest.TestCase):
    def setUp(self):
        self.solver = scip.solver()
        self.x1 = self.solver.variable()
        self.x2 = self.solver.variable()
        self.c1 = self.solver.constraint(self.x1 + 3*self.x2 <= 4)
        self.c2 = self.solver.constraint(2*self.x1 + self.x2 <= 6)

    def testMaxDualSolLinear(self):
        '''Tests LP shadow prices on a maximization problem'''
        solution = self.solver.maximize(objective=3*self.x1 + 5*self.x2)
        self.assertAlmostEqual(self.c1.dual_sol_linear, 1.4)
        self.assertAlmostEqual(self.c2.dual_sol_linear, 0.8)
        self.solver.restart()

    def testMinDualSolLinear(self):
        '''Tests LP shadow prices on a minimization problem'''
        solution = self.solver.minimize(objective=-(3*self.x1 + 5*self.x2))
        self.assertAlmostEqual(self.c1.dual_sol_linear, -1.4)
        self.assertAlmostEqual(self.c2.dual_sol_linear, -0.8)
        self.solver.restart()

if __name__ == '__main__':
    unittest.main()

