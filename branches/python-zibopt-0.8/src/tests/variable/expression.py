from algebraic import variable
import unittest

class ExpressionTest(unittest.TestCase):
    def setUp(self):
        self.x1 = variable()
        self.x2 = variable()
        self.x3 = variable()
        self.x4 = variable()

        self.tup_x1   = tuple(sorted([self.x1]))
        self.tup_x2   = tuple(sorted([self.x2]))
        self.tup_x11  = tuple(sorted([self.x1, self.x1]))
        self.tup_x12  = tuple(sorted([self.x1, self.x2]))
        self.tup_x14  = tuple(sorted([self.x1, self.x4]))
        self.tup_x22  = tuple(sorted([self.x2, self.x2]))
        self.tup_x23  = tuple(sorted([self.x2, self.x3]))
        self.tup_x34  = tuple(sorted([self.x3, self.x4]))
        self.tup_x123 = tuple(sorted([self.x1, self.x2, self.x3]))

    def test_addtion_different_terms(self):
        '''Tests addition against two terms'''
        e = 2 * self.x1 + self.x1 * self.x2
        self.assertEqual(e[self.tup_x1], 2.0)
        self.assertEqual(e[self.tup_x12], 1.0)

    def test_addtion_one_term_same(self):
        '''Tests addition against two terms, one appearing twice'''
        e = self.x1 + self.x1 + 3 * self.x2
        self.assertEqual(e[self.tup_x1], 2.0)
        self.assertEqual(e[self.tup_x2], 3.0)

    def test_constant_multiplication(self):
        '''Multiplies an expression by a constant'''
        e = 2 * (self.x1 + self.x1 + 3 * self.x2) * 1
        self.assertEqual(e[self.tup_x1], 4.0)
        self.assertEqual(e[self.tup_x2], 6.0)

    def test_expression_multiplication(self):
        '''Multiplies an expression by a constant'''
        e = 3 * (self.x1 + self.x3) * (2*self.x2 - self.x4)
        self.assertEqual(len(e.terms), 4)
        self.assertEqual(e[self.tup_x12],  6.0)
        self.assertEqual(e[self.tup_x14], -3.0)
        self.assertEqual(e[self.tup_x23],  6.0)
        self.assertEqual(e[self.tup_x34], -3.0)

    def test_complex_expression_multiplication(self):
        '''Multiplies two complex expressions'''
        e = 4 * self.x1 * (self.x2*self.x3 + 7*self.x2 )
        self.assertEqual(len(e.terms), 2)
        self.assertEqual(e[self.tup_x12],  28.0)
        self.assertEqual(e[self.tup_x123],  4.0)

    def test_complex_expression_multiplication_two_constants(self):
        '''Multiplies two complex expressions, divides by a constant'''
        e = 2 * (self.x1 + self.x1 + 3 * self.x2) / 3
        self.assertEqual(e[self.tup_x1], 4/3.)
        self.assertEqual(e[self.tup_x2], 2.0)

    def test_foil_plus_plus(self):
        '''Tests (x+y) * (x+y)'''
        e = (self.x1 + self.x2) * (2*self.x1 + self.x2)
        self.assertEqual(len(e.terms), 3)
        self.assertEqual(e[self.tup_x11], 2.0)
        self.assertEqual(e[self.tup_x12], 3.0)
        self.assertEqual(e[self.tup_x22], 1.0)

    def test_foil_plus_minus(self):
        '''Tests (x+y) * (x-y)'''
        e = (self.x1 + self.x2) * (2*self.x1 - self.x2)
        self.assertEqual(len(e.terms), 3)
        self.assertEqual(e[self.tup_x11],  2.0)
        self.assertEqual(e[self.tup_x12],  1.0)
        self.assertEqual(e[self.tup_x22], -1.0)

    def test_foil_with_constant(self):
        '''Tests (x+y) * (x-c)'''
        e = (self.x1 + self.x2) * (2*self.x1 - 4)
        self.assertEqual(len(e.terms), 4)
        self.assertEqual(e[self.tup_x1], -4.0)
        self.assertEqual(e[self.tup_x2], -4.0)
        self.assertEqual(e[self.tup_x11], 2.0)
        self.assertEqual(e[self.tup_x12], 2.0)

if __name__ == '__main__':
    unittest.main()
