from zibopt import scip
import unittest

class ScipTest(unittest.TestCase):
    def setUp(self):
        pass
        
    def testLoadSolver(self):
        scip.solver()

if __name__ == '__main__':
    unittest.main()

