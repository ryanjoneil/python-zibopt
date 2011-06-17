from zibopt import scip
import unittest

class VariableTest(unittest.TestCase):
    def testVariablePriority(self):
        '''Sets and gets variable branching priority'''
        solver = scip.solver()
        x = solver.variable()
        
        p = x.priority
        x.priority = p + 1
        self.assertEqual(x.priority, p + 1)
        
        solver.maximize()
        
    def testVariableInitPriority(self):
        '''Sets variable branching priority on constructor'''
        solver = scip.solver()
        x = solver.variable(priority=10)
        self.assertEqual(x.priority, 10)
        
if __name__ == '__main__':
    unittest.main()

