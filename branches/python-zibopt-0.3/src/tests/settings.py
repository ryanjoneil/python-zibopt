from zibopt import scip, _branch, _conflict, _sepa
import unittest

class SettingsTest(unittest.TestCase):
    def testBadBranchingRule(self):
        '''Test loading a setting that doesn't exist'''
        solver = scip.solver()
        self.assertRaises(scip.BranchingRuleError, _branch.branching_rule, solver, 'NOSUCHRULE')
        self.assertRaises(scip.ConflictError, _conflict.conflict, solver, 'NOSUCHRULE')
        self.assertRaises(scip.SeparatorError, _sepa.separator, solver, 'NOSUCHRULE')
    
    def testLoadSettingsNames(self):
        '''Loads names of branching rules, separators, etc'''
        solver = scip.solver()
        self.assertTrue(solver.branching_names())
        self.assertTrue(solver.conflict_names())
        self.assertTrue(solver.separator_names())
        
    def testRuleSettings(self):
        '''Sets branching priority, maxdepth, etc'''
        solver = scip.solver()
        for b in solver.branching.values():
            x = b.maxbounddist
            b.maxbounddist = x + 1
            self.assertEqual(x+1, b.maxbounddist)

            x = b.maxdepth
            b.maxdepth = x + 1
            self.assertEqual(x+1, b.maxdepth)
        
            x = b.priority
            b.priority = x + 1
            self.assertEqual(x+1, b.priority)            

        for c in solver.conflict.values():
            x = c.priority
            c.priority = x + 1
            self.assertEqual(x+1, c.priority)

        for s in solver.separators.values():
            x = s.priority
            s.priority = x + 1
            self.assertEqual(x+1, s.priority)

    def testBranchingRuleInvalidSettings(self):
        '''Sets branching maxdepth, maxbounddist to values < -1'''
        solver = scip.solver()
        for b in solver.branching.values():
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'maxbounddist', -5)
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'maxdepth', -2)
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'maxbounddist', 'foo')
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'maxdepth', 'foo')
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'priority', 'foo')

        for c in solver.conflict.values():
            self.assertRaises(scip.ConflictError, setattr, c, 'priority', 'foo')

        for s in solver.separators.values():
            self.assertRaises(scip.SeparatorError, setattr, s, 'priority', 'foo')
            
if __name__ == '__main__':
    unittest.main()

