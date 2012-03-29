from zibopt import scip
import unittest

class VariableTest(unittest.TestCase):
    def testVariablePriority(self):
        '''Sets and gets variable branching priority'''
        solver = scip.solver()
        x = solver.variable()
        
        p = x.priority
        x.priority = p + 1
        self.assertAlmostEqual(x.priority, p + 1)
        
        solver.maximize()
        
    def testVariableInitPriority(self):
        '''Sets variable branching priority on constructor'''
        solver = scip.solver()
        x = solver.variable(priority=10)
        self.assertAlmostEqual(x.priority, 10)

    def testExpressionBounds(self):
        '''Tests that bounds are cleared by constraint construction'''
        solver = scip.solver()
        x = solver.variable()
        c1 = solver.constraint(x >= 2)
        self.assertIsNone(x.expr_upper)
        
        c2 = solver.constraint(3 <= x <= 4)
        solution = solver.maximize(objective=x)
        self.assertAlmostEqual(solution.objective, 4)

        solver -= c2
        solution = solver.minimize(objective=x)
        self.assertAlmostEqual(solution.objective, 2)
        
if __name__ == '__main__':
    unittest.main()

