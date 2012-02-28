from algebraic import variable
import unittest

class SignTest(unittest.TestCase):
    def setUp(self):
        self.x1 = variable()
        self.x2 = variable()

        self.tup_x1 = (self.x1,)
        self.tup_x2 = (self.x2,)
        self.tup_x12 = tuple(sorted([self.x1, self.x2]))

    def test_negative(self):
        '''-(single variable) returns a -1 coefficient'''
        e = -self.x1
        self.assertEqual(e[self.tup_x1], -1.0)

    def test_negative_term(self):
        '''-(term) negates the coefficient on a term'''
        e = -(4 * self.x1 * self.x2)
        self.assertEqual(e[self.tup_x12], -4.0)

    def test_negative_expression(self):
        '''-(term) negates the coefficient on a term'''
        e = -2*((3 * self.x1) - (4 * self.x1 * self.x2))
        self.assertEqual(e[self.tup_x1], -6.0)
        self.assertEqual(e[self.tup_x12], 8.0)

    def test_postitive(self):
        '''+(single variable) does nothing to it'''
        e = +self.x1
        self.assertEqual(e[self.tup_x1], 1.0)

    def test_postitive_term(self):
        '''+(term) does nothing to it'''
        e = +(4 * self.x1 * self.x2)
        self.assertEqual(e[self.tup_x12], 4.0)

    def test_subtraction_from_constant(self):
        '''1 - expression == -expression + 1'''
        e1 = 1 - (self.x1 + self.x2)
        e2 = -(self.x1 + self.x2) + 1
        self.assertEqual(e1[self.tup_x1], -1.0)
        self.assertEqual(e2[self.tup_x1], -1.0)
        self.assertEqual(e1[self.tup_x2], -1.0)
        self.assertEqual(e2[self.tup_x2], -1.0)
        self.assertEqual(e1[()], 1.0)
        self.assertEqual(e2[()], 1.0)

if __name__ == '__main__':
    unittest.main()
