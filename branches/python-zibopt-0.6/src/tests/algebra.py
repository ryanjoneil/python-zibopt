from zibopt import scip
import unittest

class ExpressionTest(unittest.TestCase):
    def setUp(self):
        self.solver = scip.solver()
        self.x1 = self.solver.variable()
        self.x2 = self.solver.variable()
        self.x3 = self.solver.variable()
        self.x4 = self.solver.variable()

        self.set_x1   = tuple(sorted([self.x1]))
        self.set_x2   = tuple(sorted([self.x2]))
        self.set_x11  = tuple(sorted([self.x1, self.x1]))
        self.set_x12  = tuple(sorted([self.x1, self.x2]))
        self.set_x14  = tuple(sorted([self.x1, self.x4]))
        self.set_x22  = tuple(sorted([self.x2, self.x2]))
        self.set_x23  = tuple(sorted([self.x2, self.x3]))
        self.set_x34  = tuple(sorted([self.x3, self.x4]))
        self.set_x123 = tuple(sorted([self.x1, self.x2, self.x3]))

    def testSimpleExpressions(self):
        '''Tests that simple expressions are constructed via * and /'''
        e0 = 4 * self.x1
        self.assertEqual(len(e0.terms), 1)
        self.assertEqual(e0[self.set_x1], 4.0)
        self.assertEqual((e0/4)[self.set_x1], 1.0)

        e1 = 2 * self.x1 * self.x2 * 3.0
        self.assertEqual(e1[self.set_x12], 6.0)

        e2 = self.x1 * self.x2 / 4 
        self.assertEqual(e2[self.set_x12], 0.25)
        
        e3 = 8 * self.x1 * self.x2 / 4 
        self.assertEqual(e3[self.set_x12], 2.0)

    def testConstants(self):
        '''Tests that constants can be added to expressions'''
        e0 = self.x1 + 4
        self.assertEqual(len(e0.terms), 2)
        self.assertEqual(e0[self.set_x1], 1.0)
        self.assertEqual(e0[()], 4.0)

        e1 = 3 * (self.x1 - 2)
        self.assertEqual(e1[self.set_x1], 3.0)
        self.assertEqual(e1[()], -6.0)

    def testSingleTermAdditionSubtraction(self):
        '''Tests that same terms are added/subtracted properly'''
        e0 = self.x1 + self.x1
        self.assertEqual(len(e0.terms), 1)
        self.assertEqual(e0[self.set_x1], 2.0)
        
        e1 = self.x1 + 2 * self.x1
        self.assertEqual(e1[self.set_x1], 3.0)

        e2 = self.x1 * self.x2 - self.x2 * self.x1
        self.assertEqual(e2[self.set_x12], 0.0)

    def testExpressionAdditionSubtraction(self):
        '''Tests that simple expressions are added/subtracted properly'''
        e0 = 2 * self.x1 + self.x1 * self.x2
        self.assertEqual(e0[self.set_x1], 2.0)
        self.assertEqual(e0[self.set_x12], 1.0)

        e1 = self.x1 + self.x1 + 3 * self.x2
        self.assertEqual(e1[self.set_x1], 2.0)
        self.assertEqual(e1[self.set_x2], 3.0)

    def testExpressionMultiplication(self):
        '''Tests that simple expressions/terms can be multiplied'''
        e0 = 2 * (self.x1 + self.x1 + 3 * self.x2) * 1
        self.assertEqual(e0[self.set_x1], 4.0)
        self.assertEqual(e0[self.set_x2], 6.0)

        e1 = 3 * (self.x1 + self.x3) * (2*self.x2 - self.x4)
        self.assertEqual(len(e1.terms), 4)
        self.assertEqual(e1[self.set_x12],  6.0)
        self.assertEqual(e1[self.set_x14], -3.0)
        self.assertEqual(e1[self.set_x23],  6.0)
        self.assertEqual(e1[self.set_x34], -3.0)

        e2 = 4 * self.x1 * (self.x2*self.x3 + 7*self.x2 )# / 2
        self.assertEqual(len(e2.terms), 2)
        self.assertEqual(e2[self.set_x12],  28.0)
        self.assertEqual(e2[self.set_x123],  4.0)

        e3 = 2 * (self.x1 + self.x1 + 3 * self.x2) * 1
        self.assertEqual(e3[self.set_x1], 4.0)
        self.assertEqual(e3[self.set_x2], 6.0)

    def testQuadraticBilinearExpressions(self):
        '''Tests quadratic and bilinear expressions'''
        e0 = (self.x1 + self.x2) * (2*self.x1 + self.x2)
        self.assertEqual(len(e0.terms), 3)
        self.assertEqual(e0[self.set_x11], 2.0) 
        self.assertEqual(e0[self.set_x12], 3.0) 
        self.assertEqual(e0[self.set_x22], 1.0) 

        e1 = (self.x1 + self.x2) * (2*self.x1 - self.x2)
        self.assertEqual(len(e1.terms), 3)
        self.assertEqual(e1[self.set_x11],  2.0) 
        self.assertEqual(e1[self.set_x12],  1.0) 
        self.assertEqual(e1[self.set_x22], -1.0) 

        e2 = (self.x1 + self.x2) * (2*self.x1 - 4)
        self.assertEqual(len(e2.terms), 4)
        self.assertEqual(e2[self.set_x1], -4.0) 
        self.assertEqual(e2[self.set_x2], -4.0) 
        self.assertEqual(e2[self.set_x11], 2.0) 
        self.assertEqual(e2[self.set_x12], 2.0) 

    def testNegativePositive(self):
        '''Tests that negative/positive expressions and variables work'''
        e0 = -self.x1
        self.assertEqual(e0[self.set_x1], -1.0)

        e1 = -(4 * self.x1 * self.x2)
        self.assertEqual(e1[self.set_x12], -4.0)

        e2 = +self.x1
        self.assertEqual(e2[self.set_x1], 1.0)
        
        e3 = +(4 * self.x1 * self.x2)
        self.assertEqual(e3[self.set_x12], 4.0)

    def testSimpleVariablePowers(self):
        '''Tests that non-negative integer powers work'''
        e0 = 2*self.x1**0
        self.assertEqual(e0[()], 2.0)

        e1 = 3*self.x1**1
        self.assertEqual(e1[self.set_x1], 3.0)

        e2 = 4*self.x1**2
        self.assertEqual(e2[self.set_x11], 4.0)

        e3 = (5*self.x1)**2
        self.assertEqual(e3[self.set_x11], 25.0)

    def testComplexExpressionPowers(self):
        '''Tests powers of expressions with one variable'''
        e0 = (2*self.x1**3)**4
        self.assertEqual(e0[(self.x1,)*12], 2.0**4)
        
        e1 = (2*self.x1**3)**0
        self.assertEqual(len(e1.terms), 1)
        self.assertEqual(e1[()], 1.0)

        e2 = (4 - 5*self.x1**3)**2
        self.assertEqual(len(e2.terms), 3)
        self.assertEqual(e2[()], 16.0)
        self.assertEqual(e2[(self.x1,)*3], -40.0)
        self.assertEqual(e2[(self.x1,)*6], 25.0)

        e3 = (4 - 5*self.x1**3)**0
        self.assertEqual(len(e3.terms), 1)
        self.assertEqual(e3[()], 1.0)

    def testExpressionBounds(self):
        '''Tests <=, >= and == for expressions'''
        e0 = self.x1 + self.x2 - 1 <= self.x1 * self.x2 + 2
        self.assertEqual(e0[()], -1.0)
        self.assertEqual(e0[self.set_x1], 1.0)
        self.assertEqual(e0[self.set_x2], 1.0)
        self.assertEqual(e0.lower, None)
        self.assertEqual(e0.upper[()], 2.0)
        self.assertEqual(e0.upper[self.set_x12], 1.0)
        self.assertEqual(e0.upper.lower, e0)
        self.assertEqual(e0.upper.upper, None)

        e1 = self.x1 + self.x2 - 1 >= self.x1 * self.x2 + 2
        self.assertEqual(e1[()], -1.0)
        self.assertEqual(e1[self.set_x1], 1.0)
        self.assertEqual(e1[self.set_x2], 1.0)
        self.assertEqual(e1.lower[()], 2.0)
        self.assertEqual(e1.lower[self.set_x12], 1.0)
        self.assertEqual(e1.upper, None)
        self.assertEqual(e1.lower.lower, None)
        self.assertEqual(e1.lower.upper, e1)

        e2 = self.x1 + self.x2 - 1 == self.x1 * self.x2 + 2
        self.assertEqual(e2[()], -1.0)
        self.assertEqual(e2[self.set_x1], 1.0)
        self.assertEqual(e2[self.set_x2], 1.0)
        self.assertEqual(e2.lower[()], 2.0)
        self.assertEqual(e2.lower[self.set_x12], 1.0)
        self.assertEqual(e2.upper, e2.lower)
        self.assertEqual(e2.lower.lower, e2)
        self.assertEqual(e2.lower.upper, e2)

    def testVariableBounds(self):
        '''Tests <=, >= and == for variables'''
        e0 = self.x1 <= 3
        self.assertEqual(e0[self.set_x1], 1.0)
        self.assertEqual(e0.lower, None)
        self.assertEqual(e0.upper[()], 3.0)
        self.assertEqual(e0.upper.lower, e0)
        self.assertEqual(e0.upper.upper, None)

        e1 = self.x1 >= 3
        self.assertEqual(e1[self.set_x1], 1.0)
        self.assertEqual(e1.lower[()], 3.0)
        self.assertEqual(e1.upper, None)
        self.assertEqual(e1.lower.lower, None)
        self.assertEqual(e1.lower.upper, e1)

        e2 = self.x1 == 3
        self.assertEqual(e2[self.set_x1], 1.0)
        self.assertEqual(e2.lower[()], 3.0)
        self.assertEqual(e2.upper, e2.lower)
        self.assertEqual(e2.lower.lower, e2)
        self.assertEqual(e2.lower.upper, e2)

    def testChainedInequalities(self):
        '''Tests chained <= and >= for expressions'''
        e = 5 * self.x1
        1.0 <= e <= 10.0
        self.assertEqual(e.lower.terms[()], 1.0)
        self.assertEqual(e.upper.terms[()], 10.0)

        e.lower = e.upper = None
        20 >= e >= 5
        self.assertEqual(e.lower.terms[()], 5)
        self.assertEqual(e.upper.terms[()], 20)

if __name__ == '__main__':
    unittest.main()

