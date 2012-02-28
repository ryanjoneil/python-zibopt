from zibopt import scip
import unittest

class BoundsTest(unittest.TestCase):
    def setUp(self):
        solver = scip.solver()
        self.x1 = solver.variable()
        self.x2 = solver.variable()

        self.tup_x1 = (self.x1,)
        self.tup_x2 = (self.x2,)
        self.tup_x12 = tuple(sorted([self.x1, self.x2]))

    def test_le_bounds_variable(self):
        '''Test <= bounds for variables'''
        e = self.x1 <= 3
        self.assertEqual(e.expr_upper[()], 3)

    def test_ge_bounds_variable(self):
        '''Test >= bounds for variables'''
        e = self.x1 >= 4
        self.assertEqual(e.expr_lower[()], 4)

    def test_eq_bounds_variable(self):
        '''Test == bounds for variables'''
        e = self.x1 == 5
        self.assertEqual(e.expr_lower[()], 5)
        self.assertEqual(e.expr_upper[()], 5)

    def test_le_bounds_expression(self):
        '''Test <= bounds for expressions'''
        e = self.x1 + self.x2 - 1 <= self.x1 * self.x2 + 2
        self.assertEqual(e[()], -1.0)
        self.assertEqual(e[self.tup_x1], 1.0)
        self.assertEqual(e[self.tup_x2], 1.0)
        self.assertEqual(e.expr_lower, None)
        self.assertEqual(e.expr_upper[()], 2.0)
        self.assertEqual(e.expr_upper[self.tup_x12], 1.0)
        self.assertEqual(e.expr_upper.expr_lower, e)
        self.assertEqual(e.expr_upper.expr_upper, None)

    def test_ge_bounds_expression(self):
        '''Test >= bounds for expressions'''
        e = self.x1 + self.x2 - 1 >= self.x1 * self.x2 + 2
        self.assertEqual(e[()], -1.0)
        self.assertEqual(e[self.tup_x1], 1.0)
        self.assertEqual(e[self.tup_x2], 1.0)
        self.assertEqual(e.expr_lower[()], 2.0)
        self.assertEqual(e.expr_lower[self.tup_x12], 1.0)
        self.assertEqual(e.expr_upper, None)
        self.assertEqual(e.expr_lower.expr_lower, None)
        self.assertEqual(e.expr_lower.expr_upper, e)

    def test_eq_bounds_expression(self):
        '''Test == bounds for expressions'''
        e = self.x1 + self.x2 - 1 == self.x1 * self.x2 + 2
        self.assertEqual(e[()], -1.0)
        self.assertEqual(e[self.tup_x1], 1.0)
        self.assertEqual(e[self.tup_x2], 1.0)
        self.assertEqual(e.expr_lower[()], 2.0)
        self.assertEqual(e.expr_lower[self.tup_x12], 1.0)
        self.assertEqual(e.expr_upper, e.expr_lower)
        self.assertEqual(e.expr_lower.expr_lower, e)
        self.assertEqual(e.expr_lower.expr_upper, e)

    def test_successive_iequalities(self):
        '''Tests chained <= and >= for expressions'''
        e = 5 * self.x1
        1.0 <= e <= 10.0
        self.assertEqual(e.expr_lower.terms[()], 1.0)
        self.assertEqual(e.expr_upper.terms[()], 10.0)

        e.expr_lower = e.expr_upper = None
        20 >= e >= 5
        self.assertEqual(e.expr_lower.terms[()], 5)
        self.assertEqual(e.expr_upper.terms[()], 20)

    def test_variable_inequalities(self):
        '''Tests that bounds are cleared off of x >= y'''
        self.x1 >= self.x2
        self.x1._clear_bounds()
        self.assertEqual(self.x1.expr_lower, None)
        self.assertEqual(self.x1.expr_upper, None)
        self.assertEqual(self.x2.expr_lower, None)
        self.assertEqual(self.x2.expr_upper, None)

if __name__ == '__main__':
    unittest.main()
