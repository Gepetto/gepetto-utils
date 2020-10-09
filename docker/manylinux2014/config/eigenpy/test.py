import unittest

import eigenpy


class TestEigenpy(unittest.TestCase):
    def test_trivial(self):
        self.assertLess(abs(eigenpy.Quaternion(1, 2, 3, 4).norm() - 5.47722557505), 1e-7)


if __name__ == '__main__':
    unittest.main()
