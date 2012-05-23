from zibopt import scip
import unittest

class SingleTermTest(unittest.TestCase):
    def setUp(self):
        solver = scip.solver()
        self.x1 = solver.variable()
        self.x2 = solver.variable()

        self.tup_x1 = (self.x1,)
        self.tup_x12 = tuple(sorted([self.x1, self.x2]))

    def test_twice_term(self):
        '''A term + itself = 2 times the term'''
        e = self.x1 + self.x1
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x1], 2.0)

    def test_thrice_term(self):
        '''A term + itself * c = (1+c) times the term'''
        e = self.x1 + 2 * self.x1
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x1], 3.0)

    def test_term_subtraction(self):
        '''A term - itself = zero'''
        e = self.x1 * self.x2 - self.x2 * self.x1
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x12], 0.0)

if __name__ == '__main__':
    unittest.main()
