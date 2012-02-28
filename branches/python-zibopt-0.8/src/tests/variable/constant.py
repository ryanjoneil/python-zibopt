from algebraic import variable
import unittest

class ConstantsTest(unittest.TestCase):
    def setUp(self):
        self.x1 = variable()
        self.tup_x1 = (self.x1,)

    def test_constant_addition(self):
        '''Constants can be added to expressions'''
        e = self.x1 + 4
        self.assertEqual(len(e.terms), 2)
        self.assertEqual(e[self.tup_x1], 1.0)
        self.assertEqual(e[()], 4.0)

    def test_constant_multiplication(self):
        '''Constants can be multiplied in expressions'''
        e = 3 * (self.x1 - 2)
        self.assertEqual(e[self.tup_x1], 3.0)
        self.assertEqual(e[()], -6.0)

    def test_constant_division(self):
        '''Constants can be divided in expressions'''
        e = (self.x1 - 2) / 3
        self.assertEqual(e[self.tup_x1], 1/3.0)
        self.assertEqual(e[()], -2/3.0)

if __name__ == '__main__':
    unittest.main()
