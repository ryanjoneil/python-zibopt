from zibopt import scip
import unittest

class PowersTest(unittest.TestCase):
    def setUp(self):
        solver = scip.solver()
        self.x1 = solver.variable()
        self.tup_x1 = (self.x1,)
        self.tup_x11 = (self.x1, self.x1)

    def test_power_zero(self):
        '''x^0 should return 1'''
        e = 2*self.x1**0
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[()], 2.0)

    def test_power_one(self):
        '''x^1 should return x'''
        e = 3*self.x1**1
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x1], 3.0)

    def test_power_two(self):
        '''Test x^2 * some coefficient'''
        e = 4*self.x1**2
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x11], 4.0)

    def test_power_two_with_coefficient(self):
        '''Test (c*x)^2 where c is a coefficient'''
        e = (5*self.x1)**2
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[self.tup_x11], 25.0)

    def test_expression_one_variable(self):
        '''expression^4 with one variable'''
        e = (2*self.x1**3)**4
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[(self.x1,)*12], 2.0**4)

    def test_expression_one_variable_to_zero(self):
        '''expression^0 = 1'''
        e = (2*self.x1**3)**0
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[()], 1.0)

    def test_complex_expression_squared(self):
        '''expression^2 multiplies constants and terms'''
        e = (4 - 5*self.x1**3)**2
        self.assertEqual(len(e.terms), 3)
        self.assertEqual(e[()], 16.0)
        self.assertEqual(e[(self.x1,)*3], -40.0)
        self.assertEqual(e[(self.x1,)*6], 25.0)

    def test_complex_expression_to_zero(self):
        '''complex expression^0 = 1'''
        e = (4 - 5*self.x1**3)**0
        self.assertEqual(len(e.terms), 1)
        self.assertEqual(e[()], 1.0)

if __name__ == '__main__':
    unittest.main()
