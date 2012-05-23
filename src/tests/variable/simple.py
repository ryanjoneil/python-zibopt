from zibopt import scip
import unittest

class SimpleExpressionTest(unittest.TestCase):
    '''These tests cover the most basic symolic algebra'''
    def setUp(self):
        solver = scip.solver()
        self.x1 = solver.variable()
        self.x2 = solver.variable()

        self.tup_x1 = (self.x1,)
        self.tup_x12 = tuple(sorted([self.x1, self.x2]))

    def test_variable_coefficient(self):
        '''A variable * a constant gives a term with that coefficient'''
        e = 4 * self.x1
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x1], 4.0)
        self.assertEqual((e/(2+2))[self.tup_x1], 1.0)

    def test_term_coefficient(self):
        '''A term * a constant gives a term with a new coefficient'''
        e = 2 * self.x1 * self.x2 * 3.0
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x12], 6.0)

    def test_term_division(self):
        '''A term / a constant gives that term * 1/constant'''
        e = self.x1 * self.x2 / 4
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x12], 0.25)

    def test_term_division(self):
        '''A term / a constant gives that term's coefficient/constant'''
        e = 8 * self.x1 * self.x2 / 4
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x12], 2.0)

if __name__ == '__main__':
    unittest.main()
