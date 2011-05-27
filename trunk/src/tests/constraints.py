from zibopt import scip
import unittest

class ConstraintTest(unittest.TestCase):
    def testNumericEmulation(self):
        '''Variables emulate math types for constraint generation'''
        solver = scip.solver()
        x1 = solver.variable(scip.INTEGER)
        x2 = solver.variable(scip.INTEGER)
        x3 = solver.variable(scip.INTEGER)
        
        # Addition & subtraction
        self.assertEqual((x1 + x2 + x1).coefficients, {x1: 2.0, x2:  1.0})
        self.assertEqual((x1 - x2 - x1).coefficients, {x1: 0.0, x2: -1.0})
        self.assertEqual((x1 - x2 - x3).coefficients, {x1: 1.0, x2: -1.0, x3: -1.0})

        # Multiplication
        self.assertEqual((3*x1).coefficients, {x1: 3.0})
        self.assertEqual((3*(3*x1 + 2*x2)).coefficients, {x1: 9.0, x2: 6.0})
        self.assertEqual((3*x1 + 4*x1 - 2*x2 + 3*x2).coefficients, {x1: 7.0, x2: 1.0})
        
        # Division
        self.assertEqual((x1/3).coefficients, {x1: 1/3.0})
        self.assertEqual((x1/3 + x1/3 - 2*x2/5 + x2/5).coefficients, {x1: 2/3.0, x2: -1/5.0})
        
    def testSum(self):
        '''Summation adds a 0 to the variable list which needs removing'''
        solver = scip.solver()
        x = solver.variable(scip.INTEGER)
        self.assertTrue(0 not in sum([x]).coefficients)

    def testConstraintBounds(self):
        '''Comparison operators set upper and lower bounds on constraints'''
        solver = scip.solver()
        x1 = solver.variable(scip.INTEGER)
        x2 = solver.variable(scip.INTEGER)
        x3 = solver.variable(scip.INTEGER)
        
        self.assertEqual((x1 + x2 <= 1).upper, 1.0)
        self.assertEqual((x1 + x2 >= 1).lower, 1.0)
        self.assertEqual((x1 + x2 == 1).upper, 1.0)
        self.assertEqual((x1 + x2 == 1).lower, 1.0)
        self.assertEqual((2 <= x1 + x2 <= 2).upper, 2.0)
        self.assertEqual((2 <= x1 + x2 <= 2).lower, 2.0)
        self.assertEqual((2 >= x1 + x2 >= 2).upper, 2.0)
        self.assertEqual((2 >= x1 + x2 >= 2).lower, 2.0)

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
        solver = scip.solver()

        x1 = solver.variable(scip.INTEGER)
        x2 = solver.variable(scip.INTEGER)
        c  = solver.constraint(1 <= x1 + 2*x2 <= 4)
        
        self.assertEqual(c.lower, 1.0)
        self.assertEqual(c.upper, 4.0)
        self.assertEqual(c.coefficients[x1], 1.0)
        self.assertEqual(c.coefficients[x2], 2.0)

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

if __name__ == '__main__':
    unittest.main()

