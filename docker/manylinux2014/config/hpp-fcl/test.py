import unittest

import hppfcl


class TestHPPFCL(unittest.TestCase):
    def test_trivial(self):
        self.assertLess(abs(hppfcl.Capsule(2, 3).computeVolume() - 71.2094334814), 1e-7)


if __name__ == "__main__":
    unittest.main()
