from zibopt import scip, _vars, _cons
import unittest

class ScipTest(unittest.TestCase):
    def setUp(self):
        pass
        
    def atestLoadSolver(self):
        '''Try loading the SCIP solver'''
        solver = scip.solver()

    def testMax(self):
        '''Maximize an objective subject to integer constraints'''
        solver = scip.solver()
        x1 = solver.variable(coefficient=1, vartype=scip.INTEGER, upper=2)
        x2 = solver.variable(coefficient=1, vartype=scip.INTEGER)
        x3 = solver.variable(coefficient=2, vartype=scip.INTEGER)
        solver.constraint(upper=3, coefficients={x1:1, x2:1, x3:3})
        solution = solver.maximize()
        self.assertTrue(solution)

        values = solution.values()
        self.assertEqual(values[x1], 0)
        self.assertEqual(values[x2], 3)
        self.assertEqual(values[x3], 0)
        
    def testAddVarConsError(self):
        '''Test that out-of-stage operations raise appropriate errors'''
        solver = scip.solver()
        solver.minimize()
        self.assertRaises(scip.VariableError, solver.variable)
        self.assertRaises(scip.ConstraintError, solver.constraint)

    def testBadSolverType(self):
        '''Test that solvers must be properly passed'''
        solver = scip.solver()
        self.assertRaises(scip.VariableError, _vars.variable, object(), 0)
        self.assertRaises(scip.ConstraintError, _cons.constraint, object())

    def testInfeasible(self):
        '''Solutions should be false for infeasibility'''
        solver = scip.solver()
        x1 = solver.variable()
        solver.constraint(upper=0, coefficients={x1:1})
        solver.constraint(lower=1, coefficients={x1:1})
        solution = solver.maximize() 
        self.assertFalse(solution)
        
    def testRestart(self):
        '''Test solver restart'''
        solver = scip.solver()
        solver.variable(coefficient=1, vartype=scip.INTEGER, upper=2)
        solution = solver.maximize() 
        self.assertEqual(solution.objective, 2)

        solver.restart()
        solver.variable(coefficient=1, vartype=scip.INTEGER, upper=2)
        solution = solver.maximize() 
        self.assertEqual(solution.objective, 4)
        
    def testPrimal(self):
        '''Test feeding of primal solutions to the solver'''
        solver = scip.solver()
        v1 = solver.variable(coefficient=1, vartype=scip.INTEGER, upper=2)
        v2 = solver.variable(vartype=scip.BINARY)
        v3 = solver.variable()
        solver.constraint(upper=2, coefficients={v1:1})
        solution = solver.maximize(solution={v1:2, v2:1L, v3:5.4}) # pass solution to the solver
        self.assertEqual(solution.objective, 2)
        
    # TODO: deal with unbounded problems
    # TODO: test feeding of primal with variable from another solver
    # TODO: test feeding of primal with invalid key/value types

if __name__ == '__main__':
    unittest.main()

