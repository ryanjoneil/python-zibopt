from zibopt import scip, _branch, _conflict, _heur, _nodesel, _presol, _prop, _sepa
import unittest

class SettingsTest(unittest.TestCase):
    def testBadBranchingRule(self):
        '''Test loading a setting that doesn't exist'''
        solver = scip.solver()
        self.assertRaises(scip.BranchingError, _branch.branching_rule, solver, 'NOSUCHRULE')
        self.assertRaises(scip.ConflictError, _conflict.conflict, solver, 'NOSUCHRULE')
        self.assertRaises(scip.HeuristicError, _heur.heuristic, solver, 'NOSUCHRULE')
        self.assertRaises(scip.PresolverError, _presol.presolver, solver, 'NOSUCHRULE')
        self.assertRaises(scip.PropagatorError, _prop.propagator, solver, 'NOSUCHRULE')
        self.assertRaises(scip.SelectorError, _nodesel.selector, solver, 'NOSUCHRULE')
        self.assertRaises(scip.SeparatorError, _sepa.separator, solver, 'NOSUCHRULE')

    def testLoadSettingsNames(self):
        '''Loads names of branching rules, separators, etc'''
        solver = scip.solver()
        self.assertTrue(solver.branching_names())
        self.assertTrue(solver.conflict_names())
        self.assertTrue(solver.heuristic_names())
        self.assertTrue(solver.presolver_names())
        self.assertTrue(solver.propagator_names())
        self.assertTrue(solver.selector_names())
        self.assertTrue(solver.separator_names())

    def testBranchRuleSettings(self):
        '''Sets branching priority, maxdepth, etc'''
        solver = scip.solver()
        for b in solver.branching.values():
            for a in ('maxbounddist', 'maxdepth', 'priority'):
                x = getattr(b, a)
                setattr(b, a, x + 1)
                self.assertEqual(x+1, getattr(b, a))

    def testBranchingRuleInvalidSettings(self):
        '''Sets branching maxdepth, maxbounddist to values < -1'''
        solver = scip.solver()
        for b in solver.branching.values():
            self.assertRaises(scip.BranchingError, setattr, b, 'maxbounddist', -5)
            self.assertRaises(scip.BranchingError, setattr, b, 'maxdepth', -2)
            self.assertRaises(scip.BranchingError, setattr, b, 'maxbounddist', 'foo')
            self.assertRaises(scip.BranchingError, setattr, b, 'maxdepth', 'foo')
            self.assertRaises(scip.BranchingError, setattr, b, 'priority', 'foo')

    def testConflictHandlerSettings(self):
        '''Sets conflict handler priority'''
        solver = scip.solver()
        for c in solver.conflict.values():
            x = c.priority
            c.priority = x + 1
            self.assertEqual(x+1, c.priority)

    def testConflictHandlerInvalidSettings(self):
        '''Sets invalid conflict handler priority'''
        solver = scip.solver()
        for c in solver.conflict.values():
            self.assertRaises(scip.ConflictError, setattr, c, 'priority', 'foo')

    def testHeuristicSettings(self):
        '''Sets heuristic priority, maxdepth, etc'''
        solver = scip.solver()
        for h in solver.heuristics.values():
            for a in ('freqofs', 'frequency', 'maxdepth', 'priority'):
                x = getattr(h, a)
                setattr(h, a, x + 1)
                self.assertEqual(x+1, getattr(h, a))

    def testHeuristicInvalidSettings(self):
        '''Sets invalid heuristic priority'''
        solver = scip.solver()
        for h in solver.heuristics.values():
            self.assertRaises(scip.HeuristicError, setattr, h, 'freqofs', -1)
            self.assertRaises(scip.HeuristicError, setattr, h, 'frequency', -2)
            self.assertRaises(scip.HeuristicError, setattr, h, 'maxdepth', -2)
            self.assertRaises(scip.HeuristicError, setattr, h, 'freqofs', 'foo')
            self.assertRaises(scip.HeuristicError, setattr, h, 'frequency', 'foo')
            self.assertRaises(scip.HeuristicError, setattr, h, 'priority', 'foo')

    def testPresolverSettings(self):
        '''Sets presolver priority'''
        solver = scip.solver()
        for p in solver.presolvers.values():
            x = p.priority
            p.priority = x + 1
            self.assertEqual(x+1, p.priority)

    def testPresolverInvalidSettings(self):
        '''Sets invalid presolver priority'''
        solver = scip.solver()
        for p in solver.presolvers.values():
            self.assertRaises(scip.PresolverError, setattr, p, 'priority', 'foo')

    def testPropagatorSettings(self):
        '''Sets propagator priority and frequency'''
        solver = scip.solver()
        for p in solver.propagators.values():
            for a in ('frequency', 'priority'):
                x = getattr(p, a)
                setattr(p, a, x + 1)
                self.assertEqual(x+1, getattr(p, a))

    def testPropagatorInvalidSettings(self):
        '''Sets invalid propagator priority & frequency'''
        solver = scip.solver()
        for p in solver.propagators.values():
            self.assertRaises(scip.PropagatorError, setattr, p, 'frequency', -2)
            self.assertRaises(scip.PropagatorError, setattr, p, 'frequency', 'foo')
            self.assertRaises(scip.PropagatorError, setattr, p, 'priority', 'foo')

    def testNodeSelectorSettings(self):
        '''Sets node selector priorities'''
        solver = scip.solver()
        for n in solver.selectors.values():
            for a in ('memsavepriority', 'stdpriority'):
                x = getattr(n, a)
                setattr(n, a, x + 1)
                self.assertEqual(x+1, getattr(n, a))

    def testNodeSelectorInvalidSettings(self):
        '''Sets invalid node selector priorities'''
        solver = scip.solver()
        for n in solver.selectors.values():
            self.assertRaises(scip.SelectorError, setattr, n, 'memsavepriority', 'foo')
            self.assertRaises(scip.SelectorError, setattr, n, 'stdpriority', 'foo')

    def testSeparatorSettings(self):
        '''Sets separator priority'''
        solver = scip.solver()
        for s in solver.separators.values():
            for a in ('frequency', 'maxbounddist', 'priority'):
                x = getattr(s, a)
                setattr(s, a, x + 1)
                self.assertEqual(x+1, getattr(s, a))

    def testSeparatorInvalidSettings(self):
        '''Sets invalid separator priority'''
        solver = scip.solver()
        for s in solver.separators.values():
            self.assertRaises(scip.SeparatorError, setattr, s, 'maxbounddist', -5)
            self.assertRaises(scip.SeparatorError, setattr, s, 'frequency', -2)
            self.assertRaises(scip.SeparatorError, setattr, s, 'maxbounddist', 'foo')
            self.assertRaises(scip.SeparatorError, setattr, s, 'frequency', 'foo')
            self.assertRaises(scip.SeparatorError, setattr, s, 'priority', 'foo')

if __name__ == '__main__':
    unittest.main()

