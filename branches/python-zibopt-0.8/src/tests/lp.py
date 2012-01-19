from zibopt._lp import lp, MAXIMIZE, MINIMIZE
import unittest

class LPInterfaceTest(unittest.TestCase):
    def testSimpleLP(self):
        lp(MAXIMIZE)

if __name__ == '__main__':
    unittest.main()

