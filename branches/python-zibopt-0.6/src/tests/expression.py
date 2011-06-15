from zibopt import scip
import unittest

class ExpressionTest(unittest.TestCase):
    def setUp(self):
        self.solver = scip.solver()
        self.x1 = self.solver.variable()
        self.x2 = self.solver.variable()
        self.x3 = self.solver.variable()
        self.x4 = self.solver.variable()

        self.set_x1   = frozenset([self.x1])
        self.set_x2   = frozenset([self.x2])
        self.set_x12  = frozenset([self.x1, self.x2])
        self.set_x14  = frozenset([self.x1, self.x4])
        self.set_x23  = frozenset([self.x2, self.x3])
        self.set_x34  = frozenset([self.x3, self.x4])
        self.set_x123 = frozenset([self.x1, self.x2, self.x3])

    def testSimpleTerms(self):
        '''Tests that simple terms are constructed properly via * and /'''
        t0 = 4 * self.x1
        self.assertEqual(t0.variables, self.set_x1)
        self.assertEqual(t0.coefficient, 4.0)
        self.assertEqual((t0/4).coefficient, 1.0)

        t1 = 2 * self.x1 * self.x2 * 3.0
        self.assertEqual(t1.variables, self.set_x12)
        self.assertEqual(t1.coefficient, 6.0)

        t2 = self.x1 * self.x2 / 4 
        self.assertEqual(t2.variables, self.set_x12)
        self.assertEqual(t2.coefficient, 0.25)
        
        t3 = 8 * self.x1 * self.x2 / 4 
        self.assertEqual(t3.variables, self.set_x12)
        self.assertEqual(t3.coefficient, 2.0)

    def testSingleTermAdditionSubtraction(self):
        '''Tests that same terms are added/subtracted properly'''
        t0 = self.x1 + self.x1
        self.assertEqual(t0.variables, self.set_x1)
        self.assertEqual(t0.coefficient, 2.0)
        
        t1 = self.x1 + 2 * self.x1
        self.assertEqual(t1.variables, self.set_x1)
        self.assertEqual(t1.coefficient, 3.0)

        t2 = self.x1 * self.x2 - self.x2 * self.x1
        self.assertEqual(t2.variables, self.set_x12)
        self.assertEqual(t2.coefficient, 0.0)

    def testExpressionAdditionSubtraction(self):
        '''Tests that simple expressions are added/subtracted properly'''
        e0 = 2 * self.x1 + self.x1 * self.x2
        self.assertEqual(e0[self.set_x1].coefficient, 2.0)
        self.assertEqual(e0[self.set_x12].coefficient, 1.0)

        e1 = self.x1 + self.x1 + 3 * self.x2
        self.assertEqual(e1[self.set_x1].coefficient, 2.0)
        self.assertEqual(e1[self.set_x2].coefficient, 3.0)

    def testExpressionMultiplication(self):
        '''Tests that simple expressions/terms can be multiplied'''
        e0 = 2 * (self.x1 + self.x1 + 3 * self.x2) * 1
        self.assertEqual(e0[self.set_x1].coefficient, 4.0)
        self.assertEqual(e0[self.set_x2].coefficient, 6.0)

        e1 = 3 * (self.x1 + self.x3) * (2*self.x2 - self.x4)
        self.assertEqual(len(e1.terms), 4)
        self.assertEqual(e1[self.set_x12].coefficient,  6.0)
        self.assertEqual(e1[self.set_x14].coefficient, -3.0)
        self.assertEqual(e1[self.set_x23].coefficient,  6.0)
        self.assertEqual(e1[self.set_x34].coefficient, -3.0)

        e2 = 4 * self.x1 * (self.x2*self.x3 + 7*self.x2 )# / 2
        self.assertEqual(len(e2.terms), 2)
        self.assertEqual(e2[self.set_x12].coefficient,  28.0)
        self.assertEqual(e2[self.set_x123].coefficient,  4.0)

#        e0 = 2 * (self.x1 + self.x1 + 3 * self.x2) * 1
#        self.assertEqual(e0[self.set_x1].coefficient, 4.0)
#        self.assertEqual(e0[self.set_x2].coefficient, 6.0)

        # EXPONENTS!
        # TODO: (x1 + x2) * (2x1 + x2)
        # TODO: (x1 + x2) * (2x1 - x2)
        # TODO: (x1 + x2) / (2x1 + x2)

        # TODO: self.x1 / self.x2 -> x2 exponent == -1
        # TODO: 4 / self.x1 -> exponent == -1

        # TODO: self.x1 + self.x1 -> coefficient == 2
        # TODO: self.x1 * self.x2 + self.x1 * self.x2 / 2 -> coefficient == 1.5

        # TODO: self.x1 * (self.x1 + self.x2)

        # TODO: self.x1 + 3
        # TODO: self.x1 * self.x2 + 3

#    def testNonlinearConstraint(self):
#        '''Tests bilinear constraints with coefficients'''
#        solver = scip.solver()
#        x1 = solver.variable(scip.INTEGER)
#        x2 = solver.variable(scip.INTEGER)
#        
#        # Terms are stored by combinations of variables
#        term = frozenset([x1, x2])        
#
#        self.assertEqual((2*x1*x2).terms[term].coefficient, 2.0)
#        self.assertEqual((2*x1*3*x2).terms[term].coefficient, 6.0)
#        
#        #self.assertEqual((2*x1*3*x2**2).terms[0].coefficient, 6.0)
#
#        # TODO:
#        # x1/4 + 2*x1 + 3*x1*x2 + 2*x1*x2**2
#        # 3*x1*x2 + 4*x1*x2**2
#        # 3*x1*x2 + (4*x1*x2)**2
        

if __name__ == '__main__':
    unittest.main()

