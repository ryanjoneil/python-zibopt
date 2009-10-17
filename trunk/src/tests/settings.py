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
        rules = solver.branching_names()
        self.assertTrue(rules)
        self.assertEqual(set(rules), set(solver.branching_names()))
        
    def testBranchingRuleSettings(self):
        '''Sets branching priority, maxdepth, etc'''
        solver = scip.solver()
        for n, b in solver.branching.items():
            x = b.maxbounddist
            b.maxbounddist = x + 1
            self.assertEqual(x+1, b.maxbounddist)

            x = b.maxdepth
            b.maxdepth = x + 1
            self.assertEqual(x+1, b.maxdepth)
        
            x = b.priority
            b.priority = x + 1
            self.assertEqual(x+1, b.priority)            

    def testBranchingRuleInvalidSettings(self):
        '''Sets branching maxdepth, maxbounddist to values < -1'''
        solver = scip.solver()
        for b in solver.branching.values():
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'maxbounddist', -5)
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'maxdepth', -2)
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'maxbounddist', 'foo')
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'maxdepth', 'foo')
            self.assertRaises(scip.BranchingRuleError, setattr, b, 'priority', 'foo')

    def testLoadSeparatorNames(self):
        '''Loads names of separators'''
        solver = scip.solver()
        seps = solver.separator_names()
        self.assertTrue(seps)
        self.assertEqual(set(seps), set(solver.separator_names()))

    def testSeparatorSettings(self):
        '''Sets separator priority'''
        solver = scip.solver()
        for n, s in solver.separators.items():
            x = s.priority
            s.priority = x + 1
            self.assertEqual(x+1, s.priority)

    def testSeparatorInvalidSettings(self):
        '''Sets separator priority to an invalid value'''
        solver = scip.solver()
        for s in solver.branching.values():
            self.assertRaises(scip.BranchingRuleError, setattr, s, 'priority', 'foo')
            
if __name__ == '__main__':
    unittest.main()

