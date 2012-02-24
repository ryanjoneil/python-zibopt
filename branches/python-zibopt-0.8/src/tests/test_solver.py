from zibopt import scip
import unittest

class ScipTest(unittest.TestCase):
    def testLoadSolver(self):
        '''Try loading the SCIP solver'''
        solver = scip.solver()
        
if __name__ == '__main__':
    unittest.main()

