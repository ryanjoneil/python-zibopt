from zibopt import scip, _vars, _cons
import unittest

class ScipTest(unittest.TestCase):
    def setUp(self):
        pass
        
    def testLoadSolver(self):
        scip.solver()

    def testMax(self):
        solver = scip.solver()
        x1 = solver.variable(coefficient=1, vartype=scip.INTEGER, upper=2)
        x2 = solver.variable(coefficient=1, vartype=scip.INTEGER)
        x3 = solver.variable(coefficient=2, vartype=scip.INTEGER)
        solver.constraint(upper=3, coefficients={x1:1, x2:1, x3:3})
        # TODO: why does this segfault!!!???!!!???
        solution = solver.maximize()
        values = solution.values()
            
        self.assertEqual(values[x1], 0)
        self.assertEqual(values[x2], 3)
        self.assertEqual(values[x3], 0)
        
    def testAddVarConsError(self):
        solver = scip.solver()
        solver.minimize()
        self.assertRaises(scip.VariableError, solver.variable)
        self.assertRaises(scip.ConstraintError, solver.constraint)

    def testBadSolverType(self):
        solver = scip.solver()
        self.assertRaises(scip.VariableError, _vars.variable, object(), 0)
        self.assertRaises(scip.ConstraintError, _cons.constraint, object())
        
if __name__ == '__main__':
    unittest.main()

