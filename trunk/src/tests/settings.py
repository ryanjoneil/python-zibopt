from zibopt import scip, _branch
import unittest

class SettingsTest(unittest.TestCase):
    def testBadBranchingRule(self):
        '''Test loading a branching rule that doesn't exist'''
        solver = scip.solver()
        self.assertRaises(scip.BranchingRuleError, _branch.branching_rule, solver, 'NOSUCHRULE')
    
    def testLoadBranchingRuleNames(self):
        '''Loads names of branching rules'''
        solver = scip.solver()
        rules = solver.branching_rules()
        self.assertTrue(rules)
        self.assertEqual(set(rules), set(solver.branching.keys()))
        
    def testSetBranchingPriority(self):
        '''Sets branching priority'''
        solver = scip.solver()
        for n, b in solver.branching.items():
            x = b.priority
            b.priority = x + 1
            self.assertEqual(x+1, b.priority)            
        
if __name__ == '__main__':
    unittest.main()

