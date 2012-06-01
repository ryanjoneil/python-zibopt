from zibopt import scip
from zibopt.error import SCIPException
import unittest

class VariableTypeTest(unittest.TestCase):
    '''Tests for variable type errors'''
    def test_invalid_variable_type(self):
        '''Tests errors on invalid variable types'''
        solver = scip.solver()
        self.assertRaises(SCIPException, solver.variable, vartype=4)

if __name__ == '__main__':
    unittest.main()
