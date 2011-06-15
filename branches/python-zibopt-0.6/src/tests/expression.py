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

    def testExpressionBounds(self):
        '''Tests <=, >= and == for expressions'''
        e0 = self.x1 + self.x2 - 1 <= self.x1 * self.x2 + 2
        self.assertEqual(len(e0.terms), 3)
        self.assertEqual(e0[self.set_x1], 1.0)
        self.assertEqual(e0[self.set_x2], 1.0)
        self.assertEqual(e0[self.set_x12], -1.0)
        self.assertEqual(e0.upper, 3.0)

        e1 = self.x1 + self.x2 - 1 >= self.x1 * self.x2 + 2
        self.assertEqual(len(e1.terms), 3)
        self.assertEqual(e1[self.set_x1], 1.0)
        self.assertEqual(e1[self.set_x2], 1.0)
        self.assertEqual(e1[self.set_x12], -1.0)
        self.assertEqual(e1.lower, 3.0)

        e2 = self.x1 + self.x2 - 1 == self.x1 * self.x2 + 2
        self.assertEqual(len(e2.terms), 3)
        self.assertEqual(e2[self.set_x1], 1.0)
        self.assertEqual(e2[self.set_x2], 1.0)
        self.assertEqual(e2[self.set_x12], -1.0)
        self.assertEqual(e2.lower, 3.0)
        self.assertEqual(e2.upper, 3.0)

    def testVariableBounds(self):
        '''Tests <=, >= and == for variables'''
        e0 = self.x1 <= 3
        self.assertEqual(len(e0.terms), 1)
        self.assertEqual(e0.upper, 3.0)

        e1 = self.x1 >= 3
        self.assertEqual(len(e1.terms), 1)
        self.assertEqual(e1.lower, 3.0)

        e2 = self.x1 == 3
        self.assertEqual(len(e2.terms), 1)
        self.assertEqual(e2.lower, 3.0)
        self.assertEqual(e2.upper, 3.0)

    # TODO: 4 <= x1 + x2 <= 5

if __name__ == '__main__':
    unittest.main()

